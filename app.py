import os
import streamlit as st
import pandas as pd
import regex as re
from google import genai
import textwrap
import traceback
from dotenv import load_dotenv

# Set wide layout
st.set_page_config(
    page_title="DataLens!🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Lexend+Deca&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Lexend Deca', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 2rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

# Title
st.markdown("""
    <h1 style="font-family: 'Lexend Deca', sans-serif; color:#ffffff;">DataLens!🔎</h1>
""", unsafe_allow_html=True)

st.write('Upload Your Data and Get Insights')
st.divider()

# State Management
if 'df' not in st.session_state:
    st.session_state['df'] = None

if 'df' not in st.session_state or st.session_state['df'] is None:
    st.session_state['df'] = pd.DataFrame({
        "Age": [25, 30, 45, 50, 60],
        "Name": ["Alice", "Bob", "Charlie", "David", "Eva"]
    })

df = st.session_state['df']

# Store generated/fixed code in session state
if "code" not in st.session_state:
    st.session_state["code"] = ""


def extract(code: str) -> str:
    """Extracts Python code from a string containing markdown code blocks."""
    if not isinstance(code, str):
        return ""
    blocks = re.findall(r"```(?:python)?\s*(.*?)```", code, re.DOTALL | re.IGNORECASE)
    if blocks:
        return "\n\n".join(textwrap.dedent(block).strip() for block in blocks)
    return ""


@st.cache_data
def load_dataframe(data):
    """Reads an uploaded CSV file with multiple encodings and returns a DataFrame."""
    encodings = [
        "utf-8", "utf-8-sig", "latin1", "cp1252", "utf-16",
        "utf-32", "iso-8859-2", "iso-8859-15", "shift_jis", "gbk", "big5", "koi8-r"
    ]
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(data, sep=None, engine="python", encoding=enc)
            break
        except Exception:
            continue
    return df


@st.cache_data
def generate_initial_code(df, system_prompt, api_key):
    """Generates initial Python/Streamlit code using the LLM."""
    schema_info = {col: str(df[col].dtype) for col in df.columns}
    sample_rows = df.sample(min(50, len(df))).to_dict()

    initial_prompt = system_prompt + "\\n\\nColumns and types:\\n" + str(schema_info) + \
                     "\\n\\nSample data:\\n" + str(sample_rows) + \
                     "\\n\\nTask: Perform an initial analysis and generate Python/Streamlit code for insights, KPIs, charts, and dashboards."

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=initial_prompt
    )
    return extract(response.text)



# File Upload
data = st.file_uploader(label="Upload a csv file")

# Load System Prompt
with open("prompts/system.md", "r", encoding="utf-8") as f:
    system_prompt = f.read()


load_dotenv()
key = os.getenv("GEMINI_API_KEY")

if not key:
    st.error("⚠️ GEMINI_API_KEY is missing. Please add it to your .env file.")
    st.stop()
    
# Validation
if data is not None:
    df = load_dataframe(data)

    if df is None:
        st.error("Could not read the CSV file. Try re-saving it with UTF-8 encoding.")
    elif df.empty or len(df.columns) == 0:
        st.error("The DataFrame is empty or the columns don't have names")
    else:
        st.success("Upload complete. Preview the data and continue to insights.")
        st.session_state['df'] = df
        st.dataframe(df.sample(5))

        st.session_state["code"] = generate_initial_code(df, system_prompt, key)

        with st.expander("Preview Code"):
            st.code(st.session_state["code"], language="python")


# Execution block
namespace = {"st": st, "pd": pd, "df": df}

with st.container():
    error_text = None
    code = st.session_state["code"]  

    if code:  
        try:
            exec(code, namespace)
        except Exception:
            error_text = traceback.format_exc()
            st.error(f"⚠️ Error while running code:\n\n{error_text}")

        # Only show "Fix Errors" button if there is code
        if st.button("Fix Errors"):
            if error_text:
                with st.spinner("Trying to fix errors..."):
                    client = genai.Client(api_key=key)
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"{system_prompt}\n\n"
                                 f"The following code threw an error:\n\n{error_text}\n\n"
                                 f"Here is the code that caused the error:\n\n{code}\n\n"
                                 "Please fix the code while adhering to the rules above and only change what is necessary to correct the error."
                    )
                    fixed_code = extract(response.text)

                    try:
                        exec(fixed_code, namespace)
                        st.session_state["code"] = fixed_code
                    except Exception:
                        error_text = traceback.format_exc()
                        st.error(f"⚠️ Still broken:\n\n{error_text}")
            else:
                st.info("No errors detected in the last run.")

        if st.button("Regenerate Analysis"):
            generate_initial_code.clear()
            st.success("Cache cleared! Rerunning analysis...")
