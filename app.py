import streamlit as st
import pandas as pd
from google import genai

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
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

#Title
st.markdown("""
    <h1 style="font-family: 'Lexend Deca', sans-serif; color:#ffffff;">DataLens!🔎</h1>
""", unsafe_allow_html=True)

st.write('')
st.divider()

#State Management
if 'df' not in st.session_state:
    st.session_state['df'] = None


#File Upload
data = st.file_uploader(label="Upload a csv file")


#Validation

if data is not None:
    df=pd.read_csv(data)
    if df.empty == True or len(df.columns) == 0:
        st.error("The Dataframe is empty or the columns dont have names")
    else:
        st.success("Upload complete. Preview the data and continue to insights.")
        st.session_state['df'] = df
        st.dataframe(df.sample(10))

#Get Schema and Row Info
        if st.session_state['df'] is not None:
            df = st.session_state['df']
            schema_info = {col: str(df[col].dtype) for col in df.columns}
            sample_rows = df.sample(30).to_dict()

else:
    st.info("Please upload a CSV file to start.")


#Load System Prompt
with open("system.md", "r") as f:
    system_prompt = f.read()



#Append Data and Prompt
initial_prompt = system_prompt + "\n\nColumns and types:\n" + str(schema_info) + \
                 "\n\nSample data:\n" + str(sample_rows) + \
                 "\n\nTask: Perform an initial analysis and generate Python/Streamlit code for insights, KPIs, charts, and dashboards."



client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=initial_prompt
)

st.subheader("LLM Generated Code (Preview)")
st.code(response.text)