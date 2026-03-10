import re
import os
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from google import genai


#Load .env variables
load_dotenv()
KEY = os.getenv("GEMINI_API_KEY")

# Page Config
st.set_page_config(page_title="DataLens", layout="wide",initial_sidebar_state="expanded" )

# State Management
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'code' not in st.session_state:
    st.session_state['code'] = None

# Header

st.title("Welcome to DataLens!")
st.write("Upload an Excel or CSV file and generate a comprehensive report with interactive charts and summaries.")  
st.divider()


# Sanitize Code
import re

def extract(code: str) -> str:
    blocks = re.findall(r"```(?:python)?\s*(.*?)```", code, re.DOTALL | re.IGNORECASE)
    if blocks:
        return "\n\n".join(block.strip() for block in blocks)
    return code.strip()

# File Upload

temp = st.file_uploader("Upload your dataset (Excel or CSV)", type=["csv", "xlsx", "xls"], key="file_uploader")
name = temp.name if temp else "No file uploaded"

if str(name).endswith('.csv'):
    df = pd.read_csv(temp,sep=None, engine="python")

elif str(name).endswith('.xlsx'):
    df = pd.read_excel(temp)  

elif str(name).endswith('.xls'):
    df = pd.read_excel(temp)

else:
    st.warning("Please upload a CSV or Excel file.")
    st.stop()

# Reset if new file uploaded
if temp and temp.name != st.session_state.get('filename'):
    st.session_state['filename'] = temp.name
    st.session_state['df'] = df
    st.session_state['code'] = None 

with open("prompts/system.md", "r", encoding="utf-8") as f:
    prompt= f.read()

st.session_state['df'] = df

# Obtaining data properties
info = {
        'Length':len(df),
        'Shape':df.shape,
        'Info':df.dtypes.to_dict(),
        'Columns':df.columns.tolist(),
        'Sample':df.sample(50)
       }


st.divider()


#Gemini API Call
if st.session_state['code'] is None:
    with st.spinner("Generating insights and code..."):
        if df is not None:
            client = genai.Client(api_key=KEY)
            response = client.models.generate_content(
                model="gemini-3-flash-preview", 
                contents=str(df) + prompt + str(info)+ "Using the attached prompt Perform an initial analysis and generate Python/Streamlit code for insights, KPIs, maximum of 3 charts, and dashboards.")
            code = (response.text)

    code = extract(code)
    st.session_state['code'] = code

# Execute the generated code
if st.session_state['code']:
    try:
        exec(st.session_state['code'])
    except Exception as e:
        st.error(f"Generated code failed to run: {e}")
