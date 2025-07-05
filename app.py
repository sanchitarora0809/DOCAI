import streamlit as st

st.set_page_config(page_title="Gemini Snowflake Chatbot", layout="wide")

st.sidebar.title("Navigation")
st.sidebar.page_link("pages/1_Upload_Document.py", label="📤 Upload Document")
st.sidebar.page_link("pages/2_Chat_with_Gemini.py", label="💬 Chat with Gemini")

st.title("🧠 Gemini-Powered Snowflake Chatbot")
st.markdown("Welcome! Use the sidebar to upload data or chat with Gemini.")
