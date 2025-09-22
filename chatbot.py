import streamlit as st
import os
from dotenv import load_dotenv
from google.generativeai import GenerativeModel, configure

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
configure(api_key=api_key)

# Load Gemini model
model = GenerativeModel("gemini-2.5-flash")

# Streamlit UI setup
st.set_page_config(page_title="CodeYogi - Your AI Companion", layout="centered")
st.title("🧘 CodeYogi - Your AI Companion")
st.markdown("🙏Namaste!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input field with callback
def submit():
    st.session_state.messages.append(st.session_state.temp_input)
    st.session_state.temp_input = ""  # Clear input

# Temporary input field
st.text_input(
    label="",
    key="temp_input",
    placeholder="Ask me anything",
    on_change=submit
)

# Handle latest message
if st.session_state.messages:
    user_input = st.session_state.messages[-1]
    with st.spinner("Thinking..."):
        response = model.generate_content(user_input)
        output = response.text

        # Detect and display code block
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