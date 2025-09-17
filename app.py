import streamlit as st
import pandas as pd
import regex as re
from google import genai
import re
import textwrap

def extract(code: str) -> str:
    if not isinstance(code, str):
        return ""
    blocks = re.findall(r"```(?:python)?\s*(.*?)```", code, re.DOTALL | re.IGNORECASE)
    if blocks:
        combined = "\n\n".join(blocks)
    else:
        combined = code
    m = re.search(r"\b(import|from)\b", combined)
    if m:
        combined = combined[m.start():]
    return textwrap.dedent(combined).strip()


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

#Title
st.markdown("""
    <h1 style="font-family: 'Lexend Deca', sans-serif; color:#ffffff;">DataLens!🔎</h1>
""", unsafe_allow_html=True)

st.write('Upload Your Data and Get Insights')
st.divider()

#State Management
if 'df' not in st.session_state:
    st.session_state['df'] = None

if 'df' not in st.session_state or st.session_state['df'] is None:
    # fallback df for testing
    st.session_state['df'] = pd.DataFrame({
        "Age": [25, 30, 45, 50, 60],
        "Name": ["Alice", "Bob", "Charlie", "David", "Eva"]
    })

df = st.session_state['df']
# Default
code = ""


#File Upload
data = st.file_uploader(label="Upload a csv file")

#Load System Prompt
with open("system.md", "r", encoding="utf-8") as f:
    system_prompt = f.read()

#Validation

if data is not None:
    df = pd.read_csv(data)
    if df.empty or len(df.columns) == 0:
        st.error("The DataFrame is empty or the columns don't have names")
    else:
        st.success("Upload complete. Preview the data and continue to insights.")
        st.session_state['df'] = df
        st.dataframe(df.sample(5))

        # ✅ Generate schema & sample rows
        schema_info = {col: str(df[col].dtype) for col in df.columns}
        sample_rows = df.sample(30).to_dict()


        # ✅ Build the LLM prompt here
        initial_prompt = system_prompt + "\n\nColumns and types:\n" + str(schema_info) + \
                         "\n\nSample data:\n" + str(sample_rows) + \
                         "\n\nTask: Perform an initial analysis and generate Python/Streamlit code for insights, KPIs, charts, and dashboards."





        with st.status("Processing and Analysing Data....",expanded=True) as status:

            # ✅ Send to LLM
            client = genai.Client(api_key="AIzaSyAcxN3_x3Dj6-R40xzNRVm09U2RHTNefmE")
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=initial_prompt
                )  
            status.update(label="Analysis Complete!", state="complete", expanded=False)
            st.subheader("Code (Preview)")
            code=extract(response.text)

        with st.expander("Show"):
            st.code(code, language="python")



namespace = {"st": st, "pd": pd, "df": df}
with st.container():
    exec(code, namespace)

