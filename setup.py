from setuptools import setup

setup(
    name='mapping_dataflow_to_fabric_with_openai',
    version='0.01',
    packages=['test', 'test.writer', 'test.writer.nbformat', 'test.writer.nbformat.fabric', 'mdftofabric',
              'mdftofabric.app', 'mdftofabric.util', 'mdftofabric.source', 'mdftofabric.source.rest',
              'mdftofabric.writer', 'mdftofabric.writer.nbformat', 'mdftofabric.writer.nbformat.fabric',
              'mdftofabric.datamodel', 'mdftofabric.codegenerator', 'mdftofabric.codegenerator.azure',
              'mdftofabric.codegenerator.azure.openai', 'mdftofabric.codegenerator.openai'],
    url='',
    license='',
    author='arunsethia',
    author_email='',
    description='Convert Mapping dataflow to PySpark Notebook using OpenAI'
)
