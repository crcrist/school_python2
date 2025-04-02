# streamlit run main.py

import streamlit as st
import sqlite3
import hashlib
from inventory import inventory_page
from login import login_page


st.set_page_config(page_title="Employee Login System", layout="centered")

def main():
    # initialize session state for login status if it doesn't exist
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # display appropriate page based on login status
    if st.session_state.logged_in:
        inventory_page()
    else:
        login_page()

if __name__ == "__main__":
    main()








