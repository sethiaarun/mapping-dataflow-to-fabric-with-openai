"""class implements Source to get dataflow script code from File"""

from mdftofabric.datamodel.model import FileSource, MappingDataFlowScriptCode
from mdftofabric.source.dataflowsource import DataFlowSource
from mdftofabric.util import util


# pylint: disable=too-few-public-methods
class ScriptCodeFileSource(DataFlowSource):
    """get script code from file source"""

    def get_script_code(self, data_flow_source: FileSource) -> MappingDataFlowScriptCode:
        """
          get script code from given file source
          @param data_flow_source file source
        """
        script_code = MappingDataFlowScriptCode("")
        try:
            file_path = data_flow_source.file_abs_path
            with open(file_path, encoding="utf8", mode='r') as script_code_file:
                script_code_lines = script_code_file.readlines()
                util.log_info("script lines from file", number_of_lines=len(script_code_lines))
                script_code.code_lines = script_code_lines
        except FileNotFoundError as ex:
            util.log_error("Error while reading script code file", error=ex)
            raise ex
        return script_code
