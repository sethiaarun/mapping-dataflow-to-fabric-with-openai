"""Main program for the conversion tool"""
import argparse
from typing import Tuple

from mdftofabric.app import MappingDataFlowToFabricNoteBook
from mdftofabric.app.appargkeyvalue import KwargsAction
from mdftofabric.datamodel.model import SparkCode
from mdftofabric.util import util


def fabric_required_arguments() -> Tuple[str, ...]:
    """required list of arguments for Microsoft Fabric to set metadata"""
    return ('lakeHouseId', 'lakeHouseName',
            'workSpaceId', 'source')


def api_required_arguments() -> Tuple[str, ...]:
    """required list of arguments for rest api source """
    return ('rg', 'dataFlowName', 'factoryName', 'subscriptionId') + fabric_required_arguments()


def file_required_arguments() -> Tuple[str, ...]:
    """required list of arguments for file source"""
    return ('sourceFile', 'dataFlowName') + fabric_required_arguments()


def log_missing_arguments(parsed_args: dict, required_args: Tuple[str, ...]):
    """
    log missing arguments from parsed arguments
    @param parsed_args input arguments parsed dictionary
    @param required_args required list of arguments in tuples
    """
    error_missing_args = ",".join(arg for arg in (parsed_args.keys() ^ required_args))
    util.log_error(f"missing required arguments:{error_missing_args}")


def write_to_notebook(converted_spark_code: SparkCode, parsed_args: dict) -> str:
    """
    write given spark code to a notebook
    @param converted_spark_code spark code converted from data flow script
    @param parsed_args input arguments parsed dictionary
    """
    notebook_file_name = (MappingDataFlowToFabricNoteBook
                          .write_spark_notebook(spark_code=converted_spark_code,
                                                data_flow_name=parsed_args.get('dataFlowName'),
                                                lakehouse_id=parsed_args.get('lakeHouseId'),
                                                lakehouse_name=parsed_args.get('lakeHouseName'),
                                                workspace_id=parsed_args.get('workSpaceId')
                                                ))
    util.log_info("Notebook generated", file_name=notebook_file_name)
    return notebook_file_name


if __name__ == "__main__":
    file_source = ('file', 'FILE')
    api_source = ('api', 'API')
    valid_source = file_source + api_source
    parser = argparse.ArgumentParser()
    # adding an arguments
    parser.add_argument('--kwargs', nargs='*', action=KwargsAction)
    # parsing arguments
    args = parser.parse_args()
    parsed_arg_dict = args.kwargs
    # get source from where we are going to get script code
    source = parsed_arg_dict.get('source')
    if source in valid_source:
        if all(key in parsed_arg_dict for key in fabric_required_arguments()):
            if source in api_source:
                if all(key in parsed_arg_dict for key in api_required_arguments()):
                    # if API source and has valid required arguments
                    data_flow_name = parsed_arg_dict.get('dataFlowName')
                    subscription_id = parsed_arg_dict.get('subscriptionId')
                    factory_name = parsed_arg_dict.get('factoryName')
                    resource_group = parsed_arg_dict.get('rg')
                    spark_code = MappingDataFlowToFabricNoteBook.rest_source_generate_spark_code(
                        subscription_id=subscription_id,
                        data_flow_name=data_flow_name,
                        factory_name=factory_name,
                        rg=resource_group
                    )
                    # write notebook
                    file_name = write_to_notebook(spark_code, parsed_arg_dict)
                    py_spark_file = (MappingDataFlowToFabricNoteBook
                                     .write_py_spark_file(spark_code=spark_code,
                                                          data_flow_name=data_flow_name))
                    util.log_info("PySpark File generated", file_name=py_spark_file)
                else:
                    log_missing_arguments(parsed_arg_dict, api_required_arguments())
            elif source in file_source:
                if all(key in parsed_arg_dict for key in file_required_arguments()):
                    # if File source and has valid required arguments
                    data_flow_name = parsed_arg_dict.get('dataFlowName')
                    source_file_path = parsed_arg_dict.get('sourceFile')
                    spark_code = MappingDataFlowToFabricNoteBook().file_source_generate_spark_code(
                        source_file_path=source_file_path,
                        data_flow_name=data_flow_name)
                    file_name = write_to_notebook(spark_code, parsed_arg_dict)
                    py_spark_file = (MappingDataFlowToFabricNoteBook
                                     .write_py_spark_file(spark_code=spark_code,
                                                          data_flow_name=data_flow_name))
                    util.log_info("PySpark File generated", file_name=py_spark_file)
                else:
                    log_missing_arguments(parsed_arg_dict, file_required_arguments())

        else:
            util.log_error(f"provide valid source: File/file or API/api")
    else:
        log_missing_arguments(parsed_arg_dict, fabric_required_arguments())
else:
    util.log_error(f"provide valid source: File/file or API/api")
