import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.title('VODAFONE CLASSIFICATION AND PREDICTING CUSTOMER CHURN')
if 'name' not in st.session_state:
    st.error("You need to log in to access this page.")

# Function to read CSV files from URL
def read_csv_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            csv_data = response.text
            df = pd.read_csv(StringIO(csv_data))
            return df
        else:
            st.error("Failed to download CSV file from the specified URL.")
            return None
    except Exception as e:
        st.error(f"Error occurred while downloading CSV file: {e}")
        return None

# Define the URL to the CSV file on GitHub
csv_url = 'https://github.com/Samidirbsa/P4-Embedding-Machine-Learning-Models-in-GUIs/raw/main/data/LP2_Telco-churn-second-2000.csv'

# Read the CSV file from the URL
data = read_csv_from_url(csv_url)

if data is not None:
    st.title("Data Page")
    st.write("This is the data page.")

    @st.cache_data()
    def select_all_features(df):
        return df

    @st.cache_data()
    def select_numeric_features(df):
        numeric_df = df.select_dtypes(include=['number'])
        return numeric_df

    col1, col2 = st.columns(2)

    with col1:
        selected_option = st.selectbox("Select type of features", options=['All features', 'Numeric features'], key="selected_columns")

    with col2:
        pass

    if selected_option == "All features":
        data_to_display = select_all_features(data)
    elif selected_option == "Numeric features":
        data_to_display = select_numeric_features(data)

    st.dataframe(data_to_display)
