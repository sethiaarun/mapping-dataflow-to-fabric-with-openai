"""PySpark Notebook Writer"""
import json

import nbformat
from nbformat.v4 import new_notebook, new_code_cell  # nbformat

from mdftofabric.datamodel.model import SparkCode, FabricNoteBookMetaData  # data classes
from mdftofabric.util import util  # util function
from mdftofabric.writer.nbformat.fabric import fabric_py_spark_metaddata  # Fabric metadata
from mdftofabric.writer.nbformat.notebookwriter import NoteBookWriter  # Notebook writer interface


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
        nb = new_notebook(metadata=json.loads(meta_data))
        util.log_info("created notebook metadata")
        for index, value in enumerate(spark_code.code_lines):
            nb['cells'].append(new_code_cell(value))
        with open(file_name, 'w') as f:
            nbformat.write(nb, f)
        f.close()
        return file_name

    def _parse_meta_data(self) -> str:
        """read metadata and parse them with notebookMetaData"""
        return fabric_py_spark_metaddata.format(lakeHouseName=self.notebook_meta_data.lakeHouse_name,
                                                workSpaceId=self.notebook_meta_data.workspace_id,
                                                lakeHouseId=self.notebook_meta_data.lakehouse_id)
