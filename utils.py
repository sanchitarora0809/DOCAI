from pathlib import Path
import pandas as pd
import streamlit as st
import snowflake.connector
import os
from dotenv import load_dotenv
import google.generativeai as genai
import tempfile
from connection_snowflake import get_snowflake_conn

load_dotenv()


def upload_file_to_stage(file):
    """
    Uploads a file to a Snowflake stage using the original file name.
    """
    stage_name = "RAW_FILES"
    try:
        # Connect to Snowflake
        conn = get_snowflake_conn()
        cursor = conn.cursor()

        # Ensure the stage exists
        # cursor.execute(f"CREATE STAGE IF NOT EXISTS {stage_name}")
        st.write(f"Using stage: {stage_name}")
        cursor.execute(f"USE SCHEMA DOCAI.RAW_DOCS")
        

        original_filename = file.name

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = os.path.join(tmp_dir, original_filename)

            # Save file with original name
            with open(tmp_path, "wb") as f:
                f.write(file.getvalue())

            # Upload inside the 'with' block to avoid file not found error
            formatted_path = tmp_path.replace("\\", "/")
            put_command = f"PUT 'file://{formatted_path}' @{stage_name} AUTO_COMPRESS=FALSE"
            cursor.execute(put_command)
            st.success(f"Uploaded: {original_filename}")

        cursor.close()
        conn.close()

    except snowflake.connector.errors.Error as e:
        st.error(f"Error uploading file to Snowflake stage: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

def fetch_table_as_text(table_name: str) -> str:
    """
    Fetches a table from Snowflake and returns it as CSV text.
    Includes error handling for database access issues.
    """
    try:
        conn = get_snowflake_conn()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
        cursor.close()
        conn.close()
        return df.to_csv(index=False)
    except snowflake.connector.errors.Error as e:
        st.error(f"Error fetching table from Snowflake: {e}")
        return ""
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return ""


import pandas as pd
import os
import tempfile

def fetch_file_from_stage_as_df(file_path_in_stage: str) -> pd.DataFrame:
    stage_name = "@raw_files"  # Replace with your stage name

    # Extract just the filename
    file_name = file_path_in_stage.split("/")[-1]

    conn = get_snowflake_conn()
    cursor = conn.cursor()

    # Create a safe temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    local_file_path = temp_dir / file_name

    # Escape Windows path for Snowflake GET command
    safe_path = str(temp_dir).replace("\\", "/")
    get_query = f"GET {stage_name}/{file_name} 'file://{safe_path}/'"
    cursor.execute(get_query)

    # Load file as DataFrame (assumes CSV)
    df = pd.read_csv(local_file_path)

    # Cleanup (optional)
    try:
        os.remove(local_file_path)
        os.rmdir(temp_dir)
    except Exception:
        pass

    return df

def get_gemini_response(prompt: str) -> str:
    """
    Uses Google's Gemini AI model to generate a response to the given prompt.
    """
    try:
        from google.generativeai import configure, GenerativeModel
        configure(api_key="AIzaSyD5avNnryzA6Y-sDTRS_vcj55O91Xlcq5o") 
        gemini_model = GenerativeModel("gemini-1.5-pro")
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error with Gemini AI: {e}")
        return ""
