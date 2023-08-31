"""This module is responsabile for generating PySpark code using openai"""
import os  # for get environment variables
import time  # for measuring time duration of API calls

import openai  # for OpenAI API calls
from openai import OpenAIError

import mdftofabric
from mdftofabric.codegenerator.codegenerator import SparkCodeGenerator
from mdftofabric.codegenerator.openai import OpenAI
from mdftofabric.datamodel.model import MappingDataFlowScriptCode, SparkCode  # data classes
from mdftofabric.util import util  # util function

# get openai model from environment if not present consider default value from global variable
open_ai_model = os.getenv("OPENAI_MODEL", mdftofabric.OPENAI_MODEL)
if mdftofabric.OPENAI_MODEL_MAX_TOKEN.get(open_ai_model) is None:
    raise KeyError("given openai model is not tested or defined")
# get openai max token based on model name, default value from global variable
openai_model_token = (mdftofabric.OPENAI_MODEL_MAX_TOKEN
                      .get(open_ai_model, mdftofabric.OPENAI_MAX_TOKEN_DEFAULT)
                      )


# pylint: disable=too-few-public-methods
class OpenAISparkCodeGenerator(SparkCodeGenerator):
    """subclass specialized for openai connection to generate spark code"""

    def generate_spark_code(self, script_code: MappingDataFlowScriptCode) -> SparkCode:
        """
        function to generate spark code using openai ChatCompletion
        @param script_code
        """
        spark_code = SparkCode(code_lines=[])
        api_key = os.getenv("OPENAI_API_KEY")
        # record the time before the request is sent
        start_time = time.time()
        if api_key is None:
            raise KeyError("OpenAI API Key is missing")
        openai.api_key = api_key
        util.log_info("chat completion request started")
        # calculate right number of tokens can be used for the request
        # with script code and get the prompt content
        openai_request_content = self._openai_prompt_content(script_code)
        # create openai request payload
        openai_request_dict = self._openai_request_pay_load(openai_request_content)
        try:
            response = openai.ChatCompletion.create(**openai_request_dict)
            # create variables to collect the stream messages
            util.log_info("processing openai response")
            spark_code.code_lines = self._response_processing(response)
            # calculate the time it took to receive the response
            response_time = round(time.time() - start_time, 2)
            util.log_info("Full response received from openai", time_taken=str(response_time))
        except OpenAIError as api_error:
            util.log_error(api_error)
        return spark_code

    @classmethod
    def _openai_prompt_content(cls, script_code: MappingDataFlowScriptCode) -> str:
        """
         @param script_code mapping dataflow script code
        """
        prompt_content = (f"Convert Azure mapping data flow code to "
                          f"PySpark code \n ${script_code.code_lines}")
        return prompt_content

    @classmethod
    def _openai_request_pay_load(cls, prompt_content: str) -> dict:
        """
          create openai request arguments
          @param prompt_content OpenAI request content
        """
        request_message_token = OpenAI.num_tokens_from_prompt_content(prompt_content, open_ai_model)
        max_model_tokens = openai_model_token.get("max_token")
        model_system_tokens = openai_model_token.get("system_token")
        requested_token = max_model_tokens - model_system_tokens - request_message_token
        request_pay_load = {
            'model': open_ai_model,
            'messages': [{
                "role": "user",
                "content": prompt_content
            }],
            'temperature': 1,
            'top_p': 1,
            'frequency_penalty': 0,
            'presence_penalty': 0,
            'max_tokens': requested_token
        }
        util.log_info("tokens", max_model_tokens=max_model_tokens,
                      request_message_token=request_message_token, requested_token=requested_token)
        util.log_info(f"code generation limited to {requested_token} tokens, "
                      f"you need to change your model to avoid response being cut off abruptly")
        return request_pay_load

    @classmethod
    def _response_processing(cls, response) -> list[str]:
        """
            OpenAI API response processing
            @param cls class type
            @param response OpenAI API response
        """
        collected_messages = []
        if 'choices' in response and len(response['choices']) > 0:
            if ('message' in response['choices'][0] and
                    'content' in response['choices'][0]['message']):
                response_content = response['choices'][0]['message']['content']
                collected_messages = response_content.split('\n\n')
        return collected_messages
