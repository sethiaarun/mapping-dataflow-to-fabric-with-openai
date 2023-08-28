# assert value for TestPySparkNotebookWriter.test_write_note_book
fabric_pyspark_notebook_assert="""
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7d61f4c7",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pyspark.sql.functions as F"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d2a314c6",
   "metadata": {},
   "outputs": [],
   "source": [
    "srcTriggerMaster = spark.read.parquet(\"aarquet\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "python",
   "name": "synapse_pyspark"
  },
  "language_info": {
   "name": "python"
  },
  "microsoft": {
   "host": {
    "trident": {
     "lakehouse": {
      "default_lakehouse": "test_lakehouse_id",
      "known_lakehouses": "[{'id':'test_lakehouse_id'}]"
     }
    }
   },
   "language": "python",
   "ms_spell_check": {
    "ms_spell_check_language": "en"
   }
  },
  "notebook_environment": {},
  "nteract": {
   "version": "nteract-front-end@1.0.0"
  },
  "save_output": "true",
  "spark_compute": {
   "compute_id": "/trident/default",
   "session_options": {
    "conf": {},
    "enableDebugMode": "false"
   }
  },
  "synapse_widget": {
   "state": {},
   "version": "0.1"
  },
  "trident": {
   "lakehouse": {
    "default_lakehouse": "test_lakehouse_id",
    "default_lakehouse_name": "test_lakehouse_name",
    "default_lakehouse_workspace_id": "test_workspace_id",
    "known_lakehouses": [
     {
      "id": "test_lakehouse_id"
     }
    ]
   }
  },
  "widgets": {}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
"""