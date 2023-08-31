"""Interface for code generation, openai and azure openai are few implementation"""
from abc import ABC, abstractmethod

from mdftofabric.datamodel.model import MappingDataFlowScriptCode, SparkCode  # data classes


# pylint: disable=too-few-public-methods
class SparkCodeGenerator(ABC):
    """abstract class for Spark Code Generation"""

    @abstractmethod
    def generate_spark_code(self, script_code: MappingDataFlowScriptCode) -> SparkCode:
        """
        generate spark code from given script code
        the implementation can be OpenAI, Azure OpenAI, etc.
        """
