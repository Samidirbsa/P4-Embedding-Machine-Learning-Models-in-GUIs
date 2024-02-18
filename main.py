import streamlit as st

# Define username and password
USERNAME = 'your_username'
PASSWORD = 'your_password'

def main():
    st.title('VODAFONE CLASSIFICATION AND PREDICTING CUSTOMER CHURN')

    # Add login section
    username_input = st.text_input('Username')
    password_input = st.text_input('Password', type='password')

    if st.button('Login'):
        if username_input == USERNAME and password_input == PASSWORD:
            st.success('Logged in as {}'.format(username_input))
            # Display the main app content here
        else:
            st.error('Invalid username or password. Please try again.')

if __name__ == '__main__':
    main()
