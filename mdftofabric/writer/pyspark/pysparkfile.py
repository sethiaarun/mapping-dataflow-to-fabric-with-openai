"""create pyspark code in a py file"""
from mdftofabric.datamodel.model import SparkCode  # data classes
from mdftofabric.util import util  # util function


class PySparkFileWriter:

    @staticmethod
    def write_py_file(spark_code: SparkCode, file_name: str) -> str:
        """
        Write pyspark code to a file
        @param spark_code spark code
        @param file_name file name
        """
        file_name = f'{file_name}.py'
        try:
            with open(file_name, 'w') as fp:
                for line in spark_code.code_lines:
                    # write each item on a new line
                    fp.write("%s\n" % line)
        except FileExistsError as e:
            util.log_info("pyspark file already exist", file_name=file_name)
        return file_name
