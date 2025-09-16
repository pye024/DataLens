import streamlit as st
import pandas as pd
#Title
st.title("DataLens!🔎")
st.write('')
st.divider()



#File Upload
data = st.file_uploader(label="Upload a csv file")
df=pd.read_csv(data)


#Validation
if df.empty == True or len(df.columns) == 0:
    st.error("The Dataframe is empty or the columns dont have names")
else:
    st.success("Upload complete. Preview the data and continue to insights.")
    st.dataframe(df.head(10))