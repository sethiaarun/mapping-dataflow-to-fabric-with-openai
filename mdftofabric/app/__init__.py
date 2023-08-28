"""app module functions - It provides list of functions for the consumption"""
import os

from mdftofabric.app.appargkeyvalue import KwargsAction
from mdftofabric.codegenerator.openai.openaicodegenerator import OpenAISparkCodeGenerator
from mdftofabric.datamodel.model import DataFlowResource, FileSource, MappingDataFlowScriptCode, SparkCode
from mdftofabric.datamodel.model import FabricNoteBookMetaData
from mdftofabric.source.file.filedataflowsource import ScriptCodeFileSource
from mdftofabric.source.rest.adfrestdataflowsource import ADFRestGetSource
from mdftofabric.writer.nbformat.fabric.pysparkwriter import PySparkNotebookWriter
from mdftofabric.writer.pyspark.pysparkfile import PySparkFileWriter


class MappingDataFlowToFabricNoteBook:
    """
    class has list of functions to generate PySpark code from Mapping dataflow Script code
    These functions are for the end user consumptions
    """

    @staticmethod
    def get_spark_code(script_code: MappingDataFlowScriptCode) -> SparkCode:
        """
        get spark code from given script code
        @param script_code dataflow script code
        """
        spark_code = OpenAISparkCodeGenerator().generate_spark_code(script_code)
        return spark_code

    @staticmethod
    def write_py_spark_file(spark_code: SparkCode, data_flow_name: str) -> str:
        """
         Write given spark code to python file
         @param spark_code spark code
         @param data_flow_name used as file name
        """
        file_name = PySparkFileWriter.write_py_file(spark_code=spark_code, file_name=data_flow_name)
        return file_name

    @staticmethod
    def write_spark_notebook(spark_code: SparkCode,
                             data_flow_name: str, workspace_id: str,
                             lakehouse_id: str, lakehouse_name: str
                             ) -> str:
        """
        function to invoke OpenAI to generate spark code and write into notebook
        @param spark_code spark code generated from dataflow script code
        @param data_flow_name data flow name , this is used for notebook output file name
        @param workspace_id fabric workspace id
        @param lakehouse_id lakehouse id
        @param lakehouse_name lakehouse name
        """
        note_book_metadata = FabricNoteBookMetaData(workspace_id, lakehouse_id, lakehouse_name)
        # PySpark Notebook Writer
        notebook_writer = PySparkNotebookWriter(note_book_metadata)
        # create notebook
        output_file_name = notebook_writer.write_note_book(spark_code, data_flow_name)
        return output_file_name

    @classmethod
    def _validate_required_env(cls):
        """
        validate all required environment variables are present
        @param cls class type
        """
        if os.getenv("OPENAI_API_KEY") is not None:
            pass
        else:
            raise KeyError("OpenAI API Key is missing, please set OPENAI_API_KEY")

    @staticmethod
    def rest_source_generate_spark_code(subscription_id: str, rg: str, factory_name: str,
                                        data_flow_name: str) -> SparkCode:
        """
        generate spark code for where script code is provided by REST API
        @param subscription_id subscription id
        @param rg resource group where factory and data flow exists
        @param factory_name data factory name
        @param data_flow_name data flow name
        """
        # check all require environment variables are present if not this function will throw the exception
        MappingDataFlowToFabricNoteBook._validate_required_env()
        data_flow_resource = DataFlowResource(resource_group=rg, factory_name=factory_name,
                                              data_flow_name=data_flow_name, subscription_id=subscription_id)
        # get script code using ADF REST GET API
        script_code = ADFRestGetSource().get_script_code(data_flow_resource)
        # get spark code from dataflow script code
        spark_code = MappingDataFlowToFabricNoteBook.get_spark_code(script_code)
        return spark_code

    @staticmethod
    def file_source_generate_spark_code(source_file_path: str, data_flow_name: str) -> SparkCode:
        """
        generate spark code where script code is provided by file
        @param source_file_path script code file path
        @param data_flow_name data flow name , this is used for notebook output file name
        """
        # check all require environment variables are present if not this function will throw the exception
        MappingDataFlowToFabricNoteBook._validate_required_env()
        file_source = FileSource(file_abs_path=source_file_path)
        # get script code using ADF REST GET API
        script_code = ScriptCodeFileSource().get_script_code(file_source)
        # get spark code from dataflow script code
        spark_code = MappingDataFlowToFabricNoteBook.get_spark_code(script_code)
        return spark_code
