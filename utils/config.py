import os

from dotenv import load_dotenv

# load environment variables
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# LLM Configuration
LLM_PROVIDER = "groq"

DEFAULT_MODEL = "llama-3.3-70b-versatile"
DEFAULT_TEMPERATURE = 0

# Local testing
# LLM_PROVIDER = "ollama"
# DEFAULT_MODEL = "llama3.2:1b"


def validate_config() -> None:
    """
    Validate required configuration based on selected provider.
    """

    missing = []

    if LLM_PROVIDER.lower() == "groq" and not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")

    if not TAVILY_API_KEY:
        missing.append("TAVILY_API_KEY")

    if missing:
        raise ValueError(
            f"Missing environment variables: {', '.join(missing)}"
        )
