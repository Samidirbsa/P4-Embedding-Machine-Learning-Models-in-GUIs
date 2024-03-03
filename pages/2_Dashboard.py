import streamlit as st
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt

# Function to connect to the database
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

# Function to execute SQL query and return DataFrame
@st.cache_data()
def query_database(query):
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        df = pd.DataFrame.from_records(data=rows, columns=[column[0] for column in cur.description])
    return df

# Function to load dataset from file
def load_dataset(file_path):
    df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
    return df

# Function to display dataset overview
def display_dataset_overview(data):
    st.subheader('Dataset Overview')
    st.write(data)
# Summary statistics
    st.subheader('Summary Statistics')
    st.write(data.describe())

# Function to display visualizations for each feature
def display_visualizations(data):
    st.subheader('Visualizations')

    # Chart for Gender
    st.write("### Gender Distribution")
    gender_counts = data['gender'].value_counts()
    st.bar_chart(gender_counts)

    # Chart for Tenure
    st.write("### Tenure Distribution")
    fig, ax = plt.subplots()
    ax.hist(data['tenure'], bins=20)
    st.pyplot(fig)

    # Chart for Contract
    st.write("### Contract Distribution")
    contract_counts = data['Contract'].value_counts()
    st.bar_chart(contract_counts)

    # Chart for Payment Method
    st.write("### Payment Method Distribution")
    payment_counts = data['PaymentMethod'].value_counts()
    st.bar_chart(payment_counts)

    # Chart for Monthly Charges
    st.write("### Monthly Charges Distribution")
    fig, ax = plt.subplots()
    ax.hist(data['MonthlyCharges'], bins=20)
    st.pyplot(fig)
# Chart for Total Charges
    st.write("### Total Charges Distribution")
    total_charges_numeric = pd.to_numeric(data['TotalCharges'], errors='coerce')
    fig, ax = plt.subplots()
    ax.hist(total_charges_numeric.dropna(), bins=20)
    st.pyplot(fig)


# Load data from the database
conn = initialize_connection()

# Title of the dashboard
st.title('Telco Churn EDA')

# Add selectbox to choose dataset
selected_dataset = st.selectbox('Select Dataset', ['LP2_Telco_churn_first_3000', 'Telco-churn-last-2000.xlsx', 'LP2_Telco-churn-second-2000.csv'])

if selected_dataset == 'LP2_Telco_churn_first_3000':
    # Load data from the first dataset
    data = query_database("SELECT gender, tenure, Contract, PaymentMethod, MonthlyCharges, TotalCharges FROM LP2_Telco_churn_first_3000")
else:
    # Load data from the selected file
    file_path = f"data/{selected_dataset}"
    data = load_dataset(file_path)

# Display dataset overview and visualizations
display_dataset_overview(data)
display_visualizations(data)
