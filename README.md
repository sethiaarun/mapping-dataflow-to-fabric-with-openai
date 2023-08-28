# Introduction

This tool uses OpenAI API to convert Azure Mapping Dataflow code to Microsoft Fabric PySpark code using OpenAI API. 

The tool will use ADF get REST API to get dataflow script code or File source and OpenAI to convert script code into PySpark Notebook. 
We need to pass a few input parameters based on the source of the Mapping Dataflow. 
We can also pass targeted Fabric resources like workspace ID, lakehouse name, and lakehouse ID to set these parameters into notebook metadata.

# Installation

- Python > 3.10.11
- ```pip install -r requirements.txt```

# Usages
Set following environment variables:
- OPENAI_API_KEY - Your openap api key
- LOG_LEVEL - Optional debug/info

## Get DataFlow Script Lines from API

```
python.exe main.py --kwargs source=api rg=<resource group> dataFlowName=<dataflow name> factoryName=<adf name> lakeHouseId=<fabric lakehouse id> lakeHouseName=<fabric lakehouse name> workSpaceId=<fabric workspace id> subscriptionId=<azure subscription id> 
```
## Get DataFlow Script Lines from local file

```
python.exe main.py --kwargs source=file sourceFile=<dataflow script code file path> dataFlowName=<dataflow name> lakeHouseId=<fabric lakehouse id> lakeHouseName=<fabric lakehouse name> workSpaceId=<fabric workspace id>
```
There are two output files will be generated:

1. Notebook with dataflow name
2. PySpark code in `.py` file