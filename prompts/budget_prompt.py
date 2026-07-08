from langchain_core.prompts import ChatPromptTemplate


budget_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert travel budget planner.

    Estimate the actual cost of the trip.

    Trip Details:
    Destination: {destination}
    Duration: {duration} days
    Number of Travelers: {travelers}

    User's Maximum Budget:
    ₹{budget}

    Rules:
    - Return ONLY integer values.
    - Do NOT include the ₹ symbol.
    - Do NOT include commas.
    - Estimate realistic expenses.
    - Never exceed the user's maximum budget.
    - The total field can be estimated but it will be validated separately.

    Estimate:

    - Hotel
    - Food
    - Transport
    - Activities
    - Total
    """
)
