"""module constants and functions"""
FABRIC_PY_SPARK_META_DATA = """
{{
    "language_info": {{
        "name": "python"
    }},
    "kernelspec": {{
        "name": "synapse_pyspark",
        "display_name": "python"
    }},
    "microsoft": {{
        "language": "python",
        "ms_spell_check": {{
            "ms_spell_check_language": "en"
        }},
        "host": {{
            "trident": {{
                "lakehouse": {{
                    "known_lakehouses": "[{{'id':'{lakeHouseId}'}}]",
                    "default_lakehouse": "{lakeHouseId}"
                }}
            }}
        }}
    }},
    "widgets": {{}},
    "nteract": {{
        "version": "nteract-front-end@1.0.0"
    }},
    "save_output": "true",
    "spark_compute": {{
        "compute_id": "/trident/default",
        "session_options": {{
            "enableDebugMode": "false",
            "conf": {{}}
        }}
    }},
    "notebook_environment": {{}},
    "synapse_widget": {{
        "version": "0.1",
        "state": {{}}
    }},
    "trident": {{
        "lakehouse": {{
            "default_lakehouse": "{lakeHouseId}",
            "known_lakehouses": [
                {{
                    "id": "{lakeHouseId}"
                }}
            ],
            "default_lakehouse_name": "{lakeHouseName}",
            "default_lakehouse_workspace_id": "{workSpaceId}"
        }}
    }}
}}
"""
