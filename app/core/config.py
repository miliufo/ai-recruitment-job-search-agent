import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    LLM_BASE_URL = "https://api.groq.com/openai/v1"
    LLM_MODEL = "openai/gpt-oss-20b"


settings = Settings()