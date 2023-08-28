"""Interface to define source of dataflow script code - implemented by REST GET and File"""
from abc import ABC, abstractmethod

from mdftofabric.datamodel.model import Source, MappingDataFlowScriptCode


class DataFlowSource(ABC):
    """Data flow source interface"""

    @abstractmethod
    def get_script_code(self, source: Source) -> MappingDataFlowScriptCode:
        """
        get script code
        @param source source contains how to get script code
        """
        pass
