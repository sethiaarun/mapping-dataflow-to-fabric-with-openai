"""notebook writer ineterface"""

from abc import ABC, abstractmethod

from mdftofabric.datamodel.model import SparkCode, NoteBookMetaData  # data classes


# pylint: disable=too-few-public-methods
class NoteBookWriter(ABC):
    """interface for notebook writing"""

    def __init__(self, notebook_meta_data: NoteBookMetaData):
        self.notebook_meta_data = notebook_meta_data
        super().__init__()

    @abstractmethod
    def write_note_book(self, spark_code: SparkCode, file_name: str) -> str:
        """
        notebook writer returns the output file name
        @param spark_code
        @param file_name
        """
