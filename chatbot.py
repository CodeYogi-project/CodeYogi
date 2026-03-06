import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo  # ✅ Modern timezone support
import requests
from google.generativeai import GenerativeModel, configure

# 🔐 Load API keys from Streamlit Secrets
gemini_api_key = st.secrets["GEMINI_API_KEY"]
weather_api_key = st.secrets["OPENWEATHER_API_KEY"]
configure(api_key=gemini_api_key)

# 🤖 Load Gemini model
model = GenerativeModel("gemini-2.5-flash")

# 🕒 Real-time date & time (India Standard Time)
def get_now():
    india_time = datetime.now(ZoneInfo("Asia/Kolkata"))
    return india_time.strftime("%A, %d %B %Y, %I:%M %p")

# 🌦️ Real-time weather in Delhi
def get_weather(city="Delhi"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        weather_response = requests.get(url).json()
        temp = weather_response["main"]["temp"]
        desc = weather_response["weather"][0]["description"]
        return f"The weather in {city} is {temp}°C with {desc}."
    except requests.exceptions.RequestException:
        return "Weather data is currently unavailable."

# 🧠 Dynamic system prompt
def build_system_prompt():
    return f"""
You are CodeYogi, an AI assistant. The current date and time is: {get_now()}.
{get_weather("Delhi")}
You must always respond based on the current moment. Do not use outdated or generic information.
Your answers should reflect the present time, current weather, and real-world context.
Be clear, helpful, and grounded in the now.
"""

# 🎨 Streamlit UI setup
st.set_page_config(page_title="CodeYogi - Your AI Companion", layout="centered")
st.title("🧘 CodeYogi - Your AI Companion")
st.markdown("🙏Namaste!")

# 💬 Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✍️ Input field with callback
def submit():
    st.session_state.messages.append(st.session_state.temp_input)
    st.session_state.temp_input = ""  # Clear input

# 📥 Temporary input field
st.text_input(
    label="",
    key="temp_input",
    placeholder="Ask me anything",
    on_change=submit
)

# 🧠 Handle latest message
if st.session_state.messages:
    user_input = st.session_state.messages[-1]
    system_prompt = build_system_prompt()  # ✅ Rebuilt fresh every time

    with st.spinner("Thinking..."):
        # ✅ Correct structured format for Gemini
        gemini_response = model.generate_content(
            contents=[
                {"role": "user", "parts": [system_prompt]},  # system prompt must be sent as user context
                {"role": "user", "parts": [user_input]}
            ]
        )
        output = gemini_response.text

        # 🧾 Detect and display code block
        if "```" in output:
            parts = output.split("```")
            if len(parts) >= 2:
                code_header = parts[1].strip().split("\n", 1)
                lang = code_header[0].strip().lower()
                code = code_header[1] if len(code_header) > 1 else ""
                st.code(code.strip(), language=lang)
            else:
                st.markdown(output)
        else:
            st.markdown(output)
