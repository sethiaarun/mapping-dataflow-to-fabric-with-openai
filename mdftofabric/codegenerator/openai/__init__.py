"""package functions for openai code generation"""

import tiktoken

# pylint: disable=too-few-public-methods
class OpenAI:
    """
    OpenAI functions for the code conversion
    """

    @staticmethod
    def num_tokens_from_prompt_content(string: str, encoding_name: str) -> int:
        """
        number of tokens from prompt content
        """
        encoding = tiktoken.encoding_for_model(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
