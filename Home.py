import streamlit as st
import yaml

# Load YAML configuration
try:
    with open('config.yaml') as file:
        config = yaml.safe_load(file)
        print("Config loaded successfully:", config)  # Add this line to check if config is loaded correctly
except FileNotFoundError:
    st.error("Config file not found. Please make sure 'config.yaml' exists.")
    st.stop()
except yaml.YAMLError:
    st.error("Error loading config file. Please check the format and content.")
    st.stop()

# Define functions
def layout_for_logged_in_users(username):
    st.title(f'Welcome to the Dashboard, {username}')
    # Add content for logged-in users here

    # Display Attrition Insight content
    st.markdown("""
    Attrition Insight is a Machine Learning application that predicts the likelihood of an employee to leave the company based on various demographic and job-related factors.

    **Key Features**
    - View Data: Access proprietary data from IBM.
    - Dashboard: Explore interactive data visualizations for insights.
    - Real-time Prediction: Instantly see predictions for employee attrition.
    - History: See past predictions made.

    **User Benefits**
    - Data-driven Decisions: Make informed decisions backed by data analytics.
    - Easy Machine Learning: Utilize powerful machine learning algorithms effortlessly.
    - Live Demo: Watch a demo video to see the app in action.

    **How to run application**
    ```
    # activate virtual environment
    env/scripts/activate
    streamlit run 1_Home.py
    ```

    **Machine Learning Integration**
    - Model Selection: Choose between two advanced models for accurate predictions.
    - Seamless Integration: Integrate predictions into your workflow with a user-friendly interface.
    - Probability Estimates: Gain insights into the likelihood of predicted outcomes.

    **Need Help?**
    For collaborations contact me at samuel47dribsa@gmail.com.
    """)
def authenticate(username, password):
    if username in config['credentials']['usernames']:
        stored_password = config['credentials']['usernames'][username]['password']
        if password == stored_password:
            return True
    return False

# Initialize Streamlit
st.set_page_config(page_title="Vodafone Dashboard", page_icon=":chart_with_upwards_trend:")

# Main content area
if 'name' not in st.session_state:
    with st.sidebar:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state["name"] = username
            else:
                st.error("Invalid username or password. Please try again.")
else:
    with st.sidebar:
        st.title("Logout")
        if st.button("Logout"):
            del st.session_state["name"]

# Main content area
if 'name' in st.session_state:
    layout_for_logged_in_users(st.session_state['name'])
else:
    st.success("Enter username and password to use the app.")
    st.write("Test Accounts:")
    for username in config['credentials']['usernames']:
        st.write(f"Username: {username}, Password: {config['credentials']['usernames'][username]['password']}")
