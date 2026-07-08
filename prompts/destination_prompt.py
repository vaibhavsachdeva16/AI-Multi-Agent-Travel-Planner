from langchain_core.prompts import ChatPromptTemplate


destination_prompt = ChatPromptTemplate.from_template(
    """
    You are an AI travel assistant.

    Your task is to extract only the travel destination from the user's request.

    User Request:
    {user_query}

    Rules:
    - Return only the destination name.
    - Do not include explanations.
    - Do not include punctuation.
    - If no destination is found, return "Unknown".
    """
)