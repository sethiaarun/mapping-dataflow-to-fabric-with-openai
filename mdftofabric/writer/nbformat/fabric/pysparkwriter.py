"""PySpark Notebook Writer"""
import json

import nbformat
from nbformat.v4 import new_notebook, new_code_cell  # nbformat

from mdftofabric.datamodel.model import SparkCode, FabricNoteBookMetaData  # data classes
from mdftofabric.util import util  # util function
from mdftofabric.writer.nbformat.fabric import FABRIC_PY_SPARK_META_DATA  # Fabric metadata
from mdftofabric.writer.nbformat.notebookwriter import NoteBookWriter  # Notebook writer interface


# pylint: disable=too-few-public-methods
class PySparkNotebookWriter(NoteBookWriter):
    """interface for notebook writing"""

    def __init__(self, notebook_meta_data: FabricNoteBookMetaData):
        super().__init__(notebook_meta_data)
        self.notebook_meta_data = notebook_meta_data

    def write_note_book(self, spark_code: SparkCode, file_name: str) -> str:
        """
        notebook writer returns the output file name
        @param spark_code
        @param file_name
        """
        file_name = f'{file_name}.ipynb'
        util.log_info("writing notebook", file_name=file_name)
        meta_data = self._parse_meta_data().replace("\n", "")
        note_book = new_notebook(metadata=json.loads(meta_data))
        util.log_info("created notebook metadata")
        for value in spark_code.code_lines:
            note_book['cells'].append(new_code_cell(value))
        with open(file_name, encoding="utf8", mode='w') as file_pointer:
            nbformat.write(note_book, file_pointer)
        return file_name

    def _parse_meta_data(self) -> str:
        """read metadata and parse them with notebookMetaData"""
        lake_house_name = self.notebook_meta_data.lake_house_name
        workspace_id = self.notebook_meta_data.workspace_id
        lake_house_id = self.notebook_meta_data.lakehouse_id
        return FABRIC_PY_SPARK_META_DATA.format(lakeHouseName=lake_house_name,
                                                workSpaceId=workspace_id,
                                                lakeHouseId=lake_house_id)
