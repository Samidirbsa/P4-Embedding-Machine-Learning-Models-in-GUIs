import streamlit as st
import pandas as pd

st.title('VODAFONE CLASSIFICATION AND PREDICTING CUSTOMER CHURN')
if 'name' not in st.session_state:
    st.error("You need to log in to access this page.")

# Function to read CSV files
def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("CSV file not found at the specified location.")
        return None

# Define the path to the new CSV file
csv_file_path = r'C:\Users\Sami\OneDrive\GitHUB\P4-Embedding-Machine-Learning-Models-in-GUIs\data\LP2_Telco-churn-second-2000.csv'

# Read the new CSV file
@st.cache_data()
def get_data(file_path):
    return read_csv(file_path)

data = get_data(csv_file_path)

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
