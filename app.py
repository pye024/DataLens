import streamlit as st
import pandas as pd


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
else:
    st.info("Please upload a CSV file to start.")

