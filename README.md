# Introduction

This tool uses OpenAI API to convert [Azure Mapping Dataflow](https://learn.microsoft.com/en-us/azure/data-factory/concepts-data-flow-overview) code to (Microsoft Fabric PySpark)[https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook) code using OpenAI API. 

The tool will use [ADF get REST API](https://learn.microsoft.com/en-us/rest/api/datafactory/pipelines/get?tabs=HTTP) to get dataflow script code or File source and OpenAI to convert script code into PySpark Notebook. 
We need to pass a few input parameters based on the source of the Mapping Dataflow. 
We can also pass targeted Fabric resources like workspace ID, lakehouse name, and lakehouse ID to set these parameters into notebook metadata.

**The tool is not tested with all transformations supported by Azure Mapping dataflow.**


[OpenAI Privacy](https://openai.com/enterprise-privacy).

[Similar Project - Using Scala Combinator Library](https://github.com/sethiaarun/mapping-data-flow-to-spark)

# Installation

- Python > 3.10.11
- ```pip install -r requirements.txt```

# Usages
Set following environment variables:
- OPENAI_API_KEY - Your openap api key
- LOG_LEVEL - Optional debug/info

## Get DataFlow Script Lines from API

You need to pass following parameters:
- source=api
- rg - resource group name
- dataFlowName - data flow name
- factoryName - Azure data factory name
- lakeHouseId - Existing target Microsoft Fabric lakehouse Id
- lakeHouseName - Existing target Microsoft Fabric lakehouse name
- workSpaceId - Existing target Microsoft Fabric workspace Id
- subscriptionId - subscription id

```
python.exe main.py --kwargs source=api rg=<resource group> dataFlowName=<dataflow name> factoryName=<adf name> \
lakeHouseId=<fabric lakehouse id> lakeHouseName=<fabric lakehouse name> workSpaceId=<fabric workspace id> \
subscriptionId=<azure subscription id> 
```
## Get DataFlow Script Lines from local file

You need to pass following parameters:
- source=file
- dataFlowName - data flow name
- lakeHouseId - Existing target Microsoft Fabric lakehouse Id
- lakeHouseName - Existing target Microsoft Fabric lakehouse name
- workSpaceId - Existing target Microsoft Fabric workspace Id


```
python.exe main.py --kwargs source=file sourceFile=<dataflow script code file path> dataFlowName=<dataflow name>\
lakeHouseId=<fabric lakehouse id> lakeHouseName=<fabric lakehouse name> workSpaceId=<fabric workspace id>
```
There are two output files will be generated:

1. Notebook with dataflow name
2. PySpark code in `.py` file
