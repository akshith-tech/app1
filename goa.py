import streamlit as st
from openai import OpenAI

# ---------------------------------------------------------
# 1. API Configuration & LLM Setup (OpenRouter)
# ---------------------------------------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="ENTER_YOUR_OPENAI_KEY",
)

def generate_itinerary(user_query):
    """Calls OpenRouter API to generate a structured travel itinerary."""

    system_prompt = """
    You are an expert AI Travel Planner. Your job is to create detailed, practical, and personalized travel itineraries.

    When a user provides a query, generate a plan with these exact sections:
    1. 📍 Trip Overview
    2. 🗓️ Day-wise Itinerary
    3. 💰 Budget Estimate in INR
    4. 🍽️ Food Recommendations
    5. 🏨 Accommodation Suggestions
    6. 🚗 Transportation Guide
    7. ⚠️ Tips & Hacks

    Output Rules:
    - Use clear headings and bullet points.
    - Keep a helpful, practical, and enthusiastic tone.
    """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",  # IMPORTANT for OpenRouter
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"An error occurred: {str(e)}"


# ---------------------------------------------------------
# 2. Streamlit UI & Frontend Setup
# ---------------------------------------------------------

st.set_page_config(
    page_title="Roamio - AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS
st.markdown(
    """
    <style>
    .main-title {
        font-family: 'Helvetica Neue', Helvetica, sans-serif;
        color: #1E3A8A;
        font-weight: bold;
        text-align: center;
        margin-top: -80px;
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 8px;
        width: 100%;
        height: 50px;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Banner
st.image(
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
    use_container_width=True,
)

st.markdown(
    "<div class='main-title'><h1>🌍 Roamio: Your AI Travel Expert</h1></div>",
    unsafe_allow_html=True
)

st.write("---")

col1, col2 = st.columns([1, 2])

with col1:
    destination = st.text_input("Where to GO?")
    days = st.number_input("NO.OF.Days", 1, 15, 3)
    budget = st.selectbox("Budget", ["Budget", "Mid-range", "Luxury"])

    vibe = st.selectbox(
        "Vibe",
        [
            "Balanced",
            "Adventure",
            "Romantic",
            "Solo",
            "Family",
        ],
    )

    query = f"{days}-day trip to {destination}, vibe: {vibe}, budget: {budget}"

    if st.button("Generate"):
        if destination:
            result = generate_itinerary(query)
            with col2:
                st.markdown(result)
        else:
            st.warning("Enter destination")
