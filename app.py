import re
import streamlit as st

from graph.travel_graph import build_graph

# -------------------- PAGE CONFIG --------------------


st.set_page_config(
    page_title="AI Multi-Agent Travel Planner",
    page_icon="🌍",
    layout="wide",
)


# -------------------- GRAPH --------------------


@st.cache_resource
def load_graph():
    return build_graph()


travel_graph = load_graph()


# -------------------- HELPER FUNCTIONS --------------------


def extract_duration(query: str) -> int:
    """
    Extract trip duration from the user query.
    Default = 3 days.
    """

    match = re.search(
        r"(\d+)\s*[- ]?days?",
        query,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return 3


def extract_budget(query: str) -> int:
    """
    Extract budget from the user query.
    Examples:
    - under ₹40,000
    - budget 50000
    - ₹25000
    Default = 20000
    """

    # Priority 1: "under ₹40,000"
    match = re.search(
        r"under\s*₹?\s*([\d,]+)",
        query,
        re.IGNORECASE
    )

    if not match:
        # Priority 2: "budget ₹40,000"
        match = re.search(
            r"budget\s*₹?\s*([\d,]+)",
            query,
            re.IGNORECASE
        )

    if not match:
        # Priority 3: standalone ₹40,000
        match = re.search(
            r"₹\s*([\d,]+)",
            query
        )

    if match:
        return int(match.group(1).replace(",", ""))

    return 20000


def extract_travelers(query: str) -> int:
    """
    Extract number of travelers.
    Default = 2.
    """

    match = re.search(
        r"(\d+)\s*(people|person|traveler|travellers?)",
        query,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return 2


def split_itinerary_days(itinerary: str):
    """
    Split itinerary markdown into Day-wise sections.
    """

    pattern = r"(?=# Day \d+)"

    sections = re.split(pattern, itinerary)

    clean_sections = []

    for section in sections:

        section = section.strip()

        if section.startswith("# Day"):
            clean_sections.append(section)

    return clean_sections


# -------------------- SIDEBAR --------------------


st.sidebar.title("🌍 AI Travel Planner")

st.sidebar.markdown("## ⚙️ Tech Stack")

st.sidebar.success("✅ LangGraph")
st.sidebar.success("✅ Groq llama-3.3-70b-versatile")
st.sidebar.success("✅ Tavily Search")
st.sidebar.success("✅ Streamlit")

# -------------------- HEADER --------------------


st.title("🌍 AI Multi-Agent Travel Planner")

st.caption(
    "Plan personalized trips using AI-powered multi-agent collaboration with live search and real-time weather."
)

# -------------------- INPUTS --------------------


source = st.text_input(
    "Source City",
    value="Delhi"
)

query = st.text_area(
    "Trip Request",
    height=90,
    placeholder="Plan a 5-day trip to Goa under ₹40,000 for 2 people."
)

preferences = st.text_input(
    "Preferences",
    value="Beaches, Nightlife, Seafood"
)

# -------------------- BUTTON --------------------


st.caption(
    "🤖 Destination, duration, budget and travelers are automatically extracted from your trip request."
)

if st.button(
        "Generate Travel Plan",
        type="primary",
        use_container_width=True,
):

    if query.strip() == "":
        st.warning("Please enter your trip request.")
        st.stop()

    duration = extract_duration(query)
    budget = extract_budget(query)
    travelers = extract_travelers(query)

    # Initial state passed to LangGraph workflow

    initial_state = {

        "user_query": query,

        "source": source,

        "destination": "",

        "duration": duration,

        "budget": budget,

        "travelers": travelers,

        "preferences": preferences,

        "budget_plan": {},

        "weather": {},

        "hotels": [],

        "attractions": [],

        "transport": [],

        "itinerary": "",

        "final_response": ""

    }

    try:

        with st.spinner("🤖 AI agents are planning your trip..."):

            result = travel_graph.invoke(initial_state)

        # -------------------- RESULT TABS --------------------

        overview_tab, itinerary_tab, hotel_tab, attraction_tab, transport_tab = st.tabs(
            [
                "📋 Overview",
                "🗓 Itinerary",
                "🏨 Hotels",
                "📍 Attractions",
                "🚆 Transport",
            ]
        )

        with overview_tab:

            st.subheader("📋 Trip Summary")

            hotel = result["hotels"][0] if result["hotels"] else {}
            transport = result["transport"][0] if result["transport"] else {}
            weather = result["weather"]
            budget = result["budget_plan"]

            col1, col2 = st.columns(2)

            # ---------------- SELECTED HOTEL ----------------

            with col1:
                st.markdown(
                    f"""
        <div style="
        border:1px solid #2d2d2d;
        border-radius:12px;
        padding:20px;
        background:#1f1f1f;
        min-height:250px;
        display:flex;
        flex-direction:column;">

        <h3>🏨 Selected Hotel</h3>

        <h4>{hotel.get("name", "N/A")}</h4>

        <p>⭐ <b>{hotel.get("rating", "N/A")}</b></p>

        <p>💰 ₹{hotel.get("price_per_night", "N/A"):,} / night</p>

        <p>📍 {hotel.get("location", "N/A")}</p>

        </div>
        """,
                    unsafe_allow_html=True,
                )

            # ---------------- RECOMMENDED TRANSPORT ----------------

            with col2:
                st.markdown(
                    f"""
        <div style="
        border:1px solid #2d2d2d;
        border-radius:12px;
        padding:20px;
        background:#1f1f1f;
        min-height:250px;
        display:flex;
        flex-direction:column;">

        <h3>✈ Recommended Transport</h3>

        <h4>{transport.get("mode", "N/A").title()}</h4>

        <p>💰 ₹{transport.get("estimated_cost", "N/A")}</p>

        <p>⏱ {transport.get("estimated_time", "N/A")}</p>

        <p style="
            margin-top:12px;
            line-height:1.5;
            word-wrap:break-word;
            ">
            {transport.get("description", "")}
        </p>

        </div>
        """,
                    unsafe_allow_html=True,
                )

            st.write("")

            col3, col4 = st.columns(2)

            # ---------------- WEATHER ----------------

            with col3:
                st.markdown(
                    f"""
        <div style="
        border:1px solid #2d2d2d;
        border-radius:12px;
        padding:20px;
        background:#1f1f1f;
        min-height:250px;
        display:flex;
        flex-direction:column;">

        <h3>🌦 Weather</h3>

        <h1 style="margin-bottom:8px;">{weather.get("temperature", "N/A")}°C</h1>

        <p>{weather.get("condition", "N/A")}</p>

        <p>{weather.get("travel_advice", "")}</p>

        </div>
        """,
                    unsafe_allow_html=True,
                )

            # ---------------- BUDGET BREAKDOWN ----------------

            with col4:
                st.markdown(
                    f"""
        <div style="
        border:1px solid #2d2d2d;
        border-radius:12px;
        padding:20px;
        background:#1f1f1f;
        min-height:250px;
        display:flex;
        flex-direction:column;">

        <h3>💰 Budget Breakdown</h3>

        <p>🏨 Hotel : ₹{budget["hotel"]:,}</p>

        <p>🍽 Food : ₹{budget["food"]:,}</p>

        <p>🚗 Transport : ₹{budget["transport"]:,}</p>

        <p>🎟 Activities : ₹{budget["activities"]:,}</p>

        <div style="margin-top:auto;">

        <hr style="margin:14px 0;">

        <h3 style="margin:0;">
        Total : ₹{budget["total"]:,}
        </h3>

        </div>

        </div>
        """,
                    unsafe_allow_html=True,
                )

        with hotel_tab:

            st.subheader("🏨 Recommended Hotels")

            selected_hotel = (
                result["hotels"][0]["name"]
                if result["hotels"]
                else ""
            )

            cols = st.columns(3)

            for i, hotel in enumerate(result["hotels"]):

                with cols[i % 3]:

                    border_color = "#2d2d2d"
                    title = hotel["name"]

                    if hotel["name"] == selected_hotel:
                        border_color = "#22c55e"
                        title += " (⭐ Recommended)"

                    st.markdown(
                        f"""
        <div style="
        border:2px solid {border_color};
        border-radius:12px;
        padding:18px;
        background:#1f1f1f;
        height:250px;
        ">

        <h4 style="font-size:26px;">🏨 {title}</h4>

        <p>⭐ <b>{hotel.get("rating", "N/A")}</b></p>

        <p>💰 <b>₹{hotel.get("price_per_night", "N/A"):,}</b> / night</p>

        <p>📍 {hotel.get("location", "N/A")}</p>

        </div>
        """,
                        unsafe_allow_html=True,
                    )

        with attraction_tab:

            for attraction in result["attractions"]:
                with st.expander(attraction["name"]):
                    st.write(
                        attraction["description"]
                    )

        # ---------------- TRANSPORT ----------------

        with transport_tab:

            for transport in result["transport"]:
                with st.expander(transport["mode"].title(), expanded=True):
                    st.write(
                        f"💰 ₹{transport.get('estimated_cost', 'N/A')}"
                    )

                    st.write(
                        f"⏱ {transport.get('estimated_time', 'N/A')}"
                    )

                    st.write(
                        transport.get("description", "")
                    )

        with itinerary_tab:

            st.subheader("🗓 Complete Itinerary")

            days = split_itinerary_days(result["itinerary"])

            for i, day in enumerate(days):
                title = day.split("\n")[0].replace("#", "").strip()

                body = "\n".join(day.split("\n")[1:])

                with st.expander(
                        title,
                        expanded=(i == 0)
                ):
                    st.markdown(body)

    except Exception:
        st.error(
            "Something went wrong while generating your travel plan. Please try again."
        )
