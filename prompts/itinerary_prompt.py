from langchain_core.prompts import ChatPromptTemplate


itinerary_prompt = ChatPromptTemplate.from_template(
    """
You are an expert travel planner.

Create a detailed, realistic and practical day-wise travel itinerary.

Trip Details

Destination:
{destination}

Duration:
{duration} days

Travelers:
{travelers}

User Preferences:
{preferences}

Budget Breakdown:
{budget_plan}

Current Weather:
{weather}

Recommended Hotels:
{hotels}

Recommended Attractions:
{attractions}

Recommended Transport:
{transport}

Rules:

- Create exactly {duration} days.
- Select ONLY ONE hotel from the recommended hotels for the entire stay.
- Select ONLY ONE transport option from the recommended transport options.
- Use ONLY the recommended attractions.
- Never invent hotels, attractions or transport.
- Do not repeat attractions unless necessary.
- Keep travel practical and geographically sensible.
- Mention hotel check-in on Day 1.
- Mention hotel check-out and return journey on the last day.
- Use Morning, Afternoon and Evening sections for every day.
- Adapt outdoor activities according to the weather.
- If rain is expected, prioritize indoor or flexible attractions.
- Mention local food experiences whenever appropriate based on user preferences.
- Do NOT calculate budgets yourself.
- Use the Budget Breakdown exactly as provided.
- Do NOT modify any budget values.
- Keep the itinerary within the provided budget.
- Keep descriptions concise and practical.

Format the itinerary in Markdown exactly like this:

# Day 1

## Morning
...

## Afternoon
...

## Evening
...

Repeat for every day.

Finish with:

# Trip Summary

Include ONLY:

- Selected Hotel
- Selected Transport
- Weather Summary
- Budget Breakdown
- Important Travel Tips

Use the provided budget values exactly without recalculating them.
"""
)
