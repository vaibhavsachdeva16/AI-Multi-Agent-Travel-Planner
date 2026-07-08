from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

from utils.config import (
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    GROQ_API_KEY,
    LLM_PROVIDER,
    validate_config,
)


def get_llm(
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
):

    validate_config()

    if LLM_PROVIDER.lower() == "ollama":

        return ChatOllama(
            model=model,
            temperature=temperature,
        )

    return ChatGroq(
        model=model,
        temperature=temperature,
        api_key=GROQ_API_KEY,
    )


def get_structured_llm(schema):

    return get_llm().with_structured_output(schema)
