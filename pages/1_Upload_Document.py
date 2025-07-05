import streamlit as st
from utils import upload_file_to_stage
st.title("📤 Upload Any File to Snowflake Stage")

uploaded_file = st.file_uploader("Choose a file of any type")

if uploaded_file:
    if st.button("Upload to Snowflake Stage"):
        try:
            upload_file_to_stage(uploaded_file)
            st.success("Successfully uploaded file to the configured Snowflake stage.")
        except Exception as e:
            st.error(f"Upload failed: {e}")
