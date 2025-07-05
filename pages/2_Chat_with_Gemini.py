import streamlit as st
from  utils import  get_gemini_response
from connection_snowflake import get_snowflake_conn


st.title("💬 Chat with Gemini on Extracted Document")

# Step 1: Get list of uploaded file names from the table
def get_uploaded_file_names():
    conn = get_snowflake_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT filename FROM DOCAI.RAW_DOCS.RAW_EXTRACTED_DATA")
    return [row[0] for row in cursor.fetchall()]

# Step 2: Let user select the file
file_names = get_uploaded_file_names()
selected_file = st.selectbox("📄 Select the uploaded file:", file_names)

# Step 3: User question
user_question = st.text_area("💡 Ask a question about the extracted content:")

if st.button("Ask Gemini"):
    try:
        # Step 4: Fetch extracted content from Snowflake
        conn = get_snowflake_conn()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT data FROM DOCAI.RAW_DOCS.RAW_EXTRACTED_DATA WHERE filename = %s LIMIT 1", 
            (selected_file,)
        )
        result = cursor.fetchone()
        if not result:
            st.warning("No extracted text found for the selected file.")
        else:
            extracted_text = result[0]
            prompt = f"""You are a helpful assistant. The user uploaded a file and below is the extracted content:

{extracted_text}

User's question: {user_question}

Please answer based only on the content above."""
            response = get_gemini_response(prompt)
            st.markdown("### 🧠 Gemini's Response:")
            st.write(response)
    except Exception as e:
        st.error(f"❌ Error: {e}")
