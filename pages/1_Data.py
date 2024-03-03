import streamlit as st
import os
import pyodbc
import pandas as pd

st.title('VODAFONE CLASSIFICATION AND PREDICTING CUSTOMER CHURN')

@st.cache_resource(show_spinner='Connecting to Database......')
def initialize_connection():
    connection = pyodbc.connect(
        "DRIVER={SQL Server};SERVER="
        + st.secrets["SERVER"]
        +";DATABASE="
        + st.secrets["DATABASE"]
        +";UID="
        + st.secrets["UID"]
        +";PWD="
        + st.secrets["PWD"]
    )
    return connection
    
conn = initialize_connection()

def query_database(query):
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        df = pd.DataFrame. from_records(data=rows, columns=[ column[0] for column in cur.description])
    return df

@st.cache_data()
def select_all_features():
    query = "SELECT * FROM LP2_Telco_churn_first_3000"
    df = query_database(query)
    return df

@st.cache_data()
def select_numeric_features():
    query = "SELECT * FROM LP2_Telco_churn_first_3000"
    df = query_database(query)
    numeric_df = df.select_dtypes(include=['number'])
    return numeric_df

if __name__ == "__main__":
    col1, col2 = st.columns(2)

    with col1:
        selected_option = st.selectbox("Select type of features", options=['All features', 'Numeric features'], key="selected_columns")

    with col2:
        pass

    if selected_option == "All features":
        data = select_all_features()
    elif selected_option == "Numeric features":
        data = select_numeric_features()

    st.dataframe(data)
