from openai import OpenAI

from app.core.config import settings


def get_llm_client() -> OpenAI:
    if not settings.GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to your .env file."
        )

    return OpenAI(
        api_key=settings.GROQ_API_KEY,
        base_url=settings.LLM_BASE_URL,
    )


client = get_llm_client()