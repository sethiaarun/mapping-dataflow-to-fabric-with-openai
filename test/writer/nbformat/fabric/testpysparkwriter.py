"""test cases for fabric notebook writer for pyspark"""
import os
import unittest

from mdftofabric.datamodel.model import FabricNoteBookMetaData, SparkCode
from mdftofabric.writer.nbformat.fabric.pysparkwriter import PySparkNotebookWriter


class TestPySparkNotebookWriter(unittest.TestCase):
    """Test cases for Fabric Notebook PySpark"""

    def test_write_note_book(self):
        """test notebook write function"""
        note_book_metadata = FabricNoteBookMetaData(workspace_id="test_workspace_id",
                                                    lakehouse_id="test_lakehouse_id",
                                                    lake_house_name="test_lakehouse_name")
        notebook_writer = PySparkNotebookWriter(note_book_metadata)
        spark_code = SparkCode(code_lines=["import pyspark.sql.functions as F",
                                           "srcTriggerMaster = spark.read.parquet(\"aarquet\")"]
                               )
        out_put_file = notebook_writer.write_note_book(spark_code, "testfabricnotebook")
        self.assertTrue(os.path.isfile(out_put_file))


if __name__ == '__main__':
    unittest.main()
