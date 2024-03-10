import streamlit as st
import pandas as pd
import os

def load_history():
    if os.path.exists('data/history.csv'):
        history_df = pd.read_csv('data/history.csv')
    else:
        history_df = pd.DataFrame()  # Create an empty DataFrame if the file doesn't exist
    return history_df

def clear_history():
    if os.path.exists('data/history.csv'):
        os.remove('data/history.csv')
        st.success("History cleared successfully.")
    else:
        st.warning("History is already empty.")

def main():
    # Check if the user is logged in
    if 'name' not in st.session_state:
        st.error("You need to log in to access this page.")
    else:
        st.title('History Page')
        
        # Load history data
        history_df = load_history()
        
        # Display history data if available
        if not history_df.empty:
            st.write(history_df)
        else:
            st.warning("History is empty.")
        
        # Add a clear button
        if st.button('Clear History'):
            clear_history()
        
        # Add logout button
        else:
            with st.sidebar:
                st.title("Logout")
                if st.button("Logout"):
                    del st.session_state["name"]
                    st.success('You have been logged out successfully.')

if __name__ == '__main__':
    main()
