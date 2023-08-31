"""global constant"""
LOG_DEFAULT = "debug"
# default openai model
OPENAI_MODEL = "gpt-4"
OPENAI_MAX_TOKEN_DEFAULT = {  # default based on GPT-4
    "max_token": 8192,
    "system_token": 7
}
OPENAI_MODEL_MAX_TOKEN = {
    "gpt-4": {
        "max_token": 8192,
        "system_token": 8
        # every message follows <im_start>{role/name}\n{content}<im_end>\n
        # and every reply is primed with <im_start>assistant
    }
}
