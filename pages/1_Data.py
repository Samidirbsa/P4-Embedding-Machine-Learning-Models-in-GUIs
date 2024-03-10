import streamlit as st
import pyodbc
import pandas as pd

st.title('VODAFONE CLASSIFICATION AND PREDICTING CUSTOMER CHURN')

# Function to initialize database connection
def initialize_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};SERVER="
            + st.secrets["SERVER"]
            + ";DATABASE="
            + st.secrets["DATABASE"]
            + ";UID="
            + st.secrets["UID"]
            + ";PWD="
            + st.secrets["PWD"]
        )
        return conn
    except pyodbc.Error as e:
        st.error(f"Error connecting to SQL Server: {e}")
        return None

# Function to query database
def query_database(query, conn):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            df = pd.DataFrame.from_records(data=rows, columns=[column[0] for column in cur.description])
        return df
    except pyodbc.Error as e:
        st.error(f"Error querying database: {e}")
        return None

# Establish database connection
conn = initialize_connection()
if conn:
    with st.sidebar:
        st.title("Logout")
        if st.button("Logout"):
            del st.session_state["name"]

    st.title("Data Page")
    st.write("This is the data page.")

    @st.cache_data()
    def select_all_features():
        query = "SELECT * FROM LP2_Telco_churn_first_3000"
        df = query_database(query, conn)
        return df

    @st.cache_data()
    def select_numeric_features():
        query = "SELECT * FROM LP2_Telco_churn_first_3000"
        df = query_database(query, conn)
        numeric_df = df.select_dtypes(include=['number'])
        return numeric_df

    col1, col2 = st.columns(2)

    with col1:
        selected_option = st.selectbox("Select type of features", options=['All features', 'Numeric features'], key="selected_columns")

    with col2:
        pass

    if selected_option == "All features":
        data = select_all_features()
    elif selected_option == "Numeric features":
        data = select_numeric_features()

    if data is not None:
        st.dataframe(data)
