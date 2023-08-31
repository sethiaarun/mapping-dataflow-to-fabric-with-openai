"""create pyspark code in a py file"""
from mdftofabric.datamodel.model import SparkCode  # data classes
from mdftofabric.util import util  # util function


# pylint: disable=too-few-public-methods
class PySparkFileWriter:
    """
      PySpark file writer
    """

    @staticmethod
    def write_py_file(spark_code: SparkCode, file_name: str) -> str:
        """
        Write pyspark code to a file
        @param spark_code spark code
        @param file_name file name
        """
        file_name = f'{file_name}.py'
        try:
            with open(file_name, encoding="utf8", mode='w') as file_pointer:
                for line in spark_code.code_lines:
                    # write each item on a new line
                    file_pointer.write(f"{line}\n")
        except FileExistsError as ex:
            util.log_info("pyspark file already exist", file_name=file_name, exception=ex)
        return file_name
