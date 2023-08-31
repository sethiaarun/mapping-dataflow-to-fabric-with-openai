""" Module to get data from dataflow api source"""
import time  # to record time

from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models._models_py3 import MappingDataFlow

from mdftofabric.datamodel.model import DataFlowResource, MappingDataFlowScriptCode  # data classes
from mdftofabric.source.dataflowsource import DataFlowSource
from mdftofabric.util import util  # util function


# pylint: disable=too-few-public-methods
class ADFRestGetSource(DataFlowSource):
    """class to use ADF REST API to get Script Code"""

    def get_script_code(self, data_flow_source: DataFlowResource) -> MappingDataFlowScriptCode:
        """
        This is going to invoke ADF dataflow Get API to get
        Mapping dataflow script lines
        @param data_flow_source data flow resources
        """
        script_code = MappingDataFlowScriptCode("")
        try:
            # record the time before the request is sent
            start_time = time.time()
            client = DataFactoryManagementClient(
                credential=DefaultAzureCredential(),
                subscription_id=data_flow_source.subscription_id,
            )
            try:
                response = client.data_flows.get(
                    resource_group_name=data_flow_source.resource_group,
                    factory_name=data_flow_source.factory_name,
                    data_flow_name=data_flow_source.data_flow_name,
                )
                response_time = round(time.time() - start_time, 2)
                util.log_info("ADF REST GET API response received (sec)", time_taken=response_time)
                if isinstance(response.properties, MappingDataFlow):
                    util.log_info("received dataflow api response")
                    script_lines = response.properties.script_lines
                    util.log_info("script lines from rest api", number_of_lines=len(script_lines))
                    script_str = '\n'.join([str(elem) for elem in script_lines])
                    script_code.code_lines = script_str
                else:
                    raise TypeError("invalid response type")
            finally:
                client.close()
        except Exception as ex:
            util.log_error("Error while calling dataflow get api", error=ex)
            raise ex
        return script_code
