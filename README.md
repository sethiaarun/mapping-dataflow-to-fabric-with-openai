# Introduction

This tool uses OpenAI API to
convert [Azure Mapping Dataflow](https://learn.microsoft.com/en-us/azure/data-factory/concepts-data-flow-overview) code
to (Microsoft Fabric PySpark)[https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook) code using
OpenAI API.

The tool will use [ADF get REST API](https://learn.microsoft.com/en-us/rest/api/datafactory/pipelines/get?tabs=HTTP) to
get dataflow script code or File source and OpenAI to convert script code into PySpark Notebook.
We need to pass a few input parameters based on the source of the Mapping Dataflow.
We can also pass targeted Fabric resources like workspace ID, lakehouse name, and lakehouse ID to set these parameters
into notebook metadata.

**The tool is not tested with all transformations supported by Azure Mapping dataflow.**

[OpenAI Privacy](https://openai.com/enterprise-privacy).

[Similar Project - Using Scala Combinator Library](https://github.com/sethiaarun/mapping-data-flow-to-spark)

## Installation

- Python > 3.10.11
- ```pip install -r requirements.txt```

## Usages

Set following environment variables:

### Mandatory

- OPENAI_API_KEY - Your openap api key

### Optional

- LOG_LEVEL - Optional debug/info, default value from the application is `info`
- OPENAI_MODEL - [OpenAI model name](https://platform.openai.com/docs/models), default value from the application
  is `gpt-4`

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

# Limitation

Since we use ChatCompletion API from OpenAI with the `gpt-4` model, the max_tokens is limited to 8,192 tokens.

The max_tokens parameter in the ChatCompletion API allows you to limit the length of the response generated by
the model to a specified number of tokens. Tokens are chunks of text that language models read,
and they can be as short as one character or as long as one word, depending on the language and context.

Setting a very low value for max_tokens can result in the response being cut off abruptly, potentially leading to
an output that doesn't make sense or lacks context. The max_tokens parameter is a useful tool to control response
length, but setting it too low can negatively impact the quality and coherence of the responses.

**What does it mean to the user**? It means if your generated code length is > 8k, It will be truncated, and the result
will not be complete code.

OpenAI is [gpt-4-32k](https://help.openai.com/en/articles/7102672-how-can-i-access-gpt-4) has been around for a while,
but extremely limited rollout.

# Future Scope of work

1. Integration with [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service-b)

# References

1. [OpenAI API](https://platform.openai.com/docs/introduction)
2. [How to count
   tokens?](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb)


