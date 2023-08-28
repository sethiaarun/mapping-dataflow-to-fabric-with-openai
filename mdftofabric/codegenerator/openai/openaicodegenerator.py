"""This module is responsabile for generating PySpark code using openai"""
import os  # for get environment variables
import time  # for measuring time duration of API calls

import openai  # for OpenAI API calls

from mdftofabric.codegenerator.codegenerator import SparkCodeGenerator
from mdftofabric.datamodel.model import MappingDataFlowScriptCode, SparkCode  # data classes
from mdftofabric.util import util  # util function


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
        else:
            openai.api_key = api_key
            util.log_info("chat completion request started")
            openai_request_args = self._openai_request(script_code)
            response = openai.ChatCompletion.create(**openai_request_args)
            # create variables to collect the stream messages
            util.log_info("processing openai response")
            if openai_request_args.get('stream'):
                spark_code.code_lines = self._stream_response_processing(response)
            else:
                spark_code.code_lines = self._non_stream_response_processing(response)
            # calculate the time it took to receive the response
            response_time = round(time.time() - start_time, 2)
            util.log_info("Full response received from openai", time_taken=str(response_time))
        return spark_code

    @classmethod
    def _openai_request(cls, script_code: MappingDataFlowScriptCode):
        """create openai request arguments"""
        return {
            'model': "gpt-4",
            'messages': [{
                "role": "user",
                "content": f"Convert Azure mapping data flow code to PySpark code \n ${script_code.code_lines}"
            }],
            'stream': False,
            'temperature': 1,
            'top_p': 1,
            'frequency_penalty': 0,
            'presence_penalty': 0,
            'max_tokens': 7134
        }

    @classmethod
    def _stream_response_processing(cls, response) -> list[str]:
        """
            response processing when stream is true
            @param cls class type
            @param response OpenAI API response in stream format
        """
        collected_messages = []
        for chunk in response:
            choice = chunk['choices'][0]
            if 'delta' in choice and 'content' in choice['delta']:
                chunk_message = choice['delta']
                content = chunk_message['content']
                collected_messages.append(content)  # save the message
        return collected_messages

    @classmethod
    def _non_stream_response_processing(cls, response) -> list[str]:
        """
            response processing when stream is false
            @param cls class type
            @param response OpenAI API response
        """
        collected_messages = []
        if 'choices' in response and len(response['choices']) > 0:
            if 'message' in response['choices'][0] and 'content' in response['choices'][0]['message']:
                collected_messages = response['choices'][0]['message']['content'].split('\n\n')
        return collected_messages
