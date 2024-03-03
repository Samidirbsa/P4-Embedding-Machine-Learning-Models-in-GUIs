import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

# Load YAML configuration
with open('config.yaml') as file:
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
authentication_status = authenticator.login()

if authentication_status:
    # Display welcome message or other content
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
else:
    # Authentication failed or not attempted
    st.error('Authentication failed. Please check your credentials.')
