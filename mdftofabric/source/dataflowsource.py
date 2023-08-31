"""Interface to define source of dataflow script code - implemented by REST GET and File"""
from abc import ABC, abstractmethod

from mdftofabric.datamodel.model import Source, MappingDataFlowScriptCode


# pylint: disable=too-few-public-methods
class DataFlowSource(ABC):
    """Data flow source interface"""

    @abstractmethod
    def get_script_code(self, data_flow_source: Source) -> MappingDataFlowScriptCode:
        """
        get script code
        @param data_flow_source source contains how to get script code
        """
