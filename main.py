import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

# Load YAML configuration
with open(r'C:/Users/Sami/OneDrive/GitHUB/P4-Embedding-Machine-Learning-Models-in-GUIs/config.yaml') as file:
    config = yaml.safe_load(file)
# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
# Perform authentication
authenticator.login()
if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
