import streamlit as st
import pandas as pd

st.set_page_config(
    page_title='View Data',
    page_icon='',
    layout='wide',
)

st.title('Proprietary Data from Vodafone')

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
