"""Data class used for data communication between layers"""
from abc import ABC
from dataclasses import dataclass  # adding decorator and functions for data classes


@dataclass
class Source(ABC):
    """abstract dataflow source data class"""


@dataclass
class DataFlowResource(Source):
    """Class defines required arguments to call DataFlow REST API"""
    resource_group: str
    factory_name: str
    data_flow_name: str
    subscription_id: str


@dataclass
class FileSource(Source):
    """file source"""
    # file absolute path where we can find the script code
    file_abs_path: str


@dataclass
class SparkCode:
    """encapsulate spark code as string"""
    code_lines: list[str]


@dataclass
class MappingDataFlowScriptCode:
    """list of mapping script code lines"""
    code_lines: str


@dataclass
class NoteBookMetaData(ABC):
    """abstract notebook metadata data class"""


@dataclass
class FabricNoteBookMetaData(NoteBookMetaData):
    """Fabric Notebook Metadata"""
    workspace_id: str
    lakehouse_id: str
    lakeHouse_name: str
