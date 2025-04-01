import streamlit as st
import sqlite3

# connect to database
def get_connection():
    return sqlite3.connect('example.db')

# verify login credentials
def verify_credentials(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM employees WHERE username = ? AND password = ?" 
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.close()

    return result is not None

# function to create login UI
def login_page():
    st.title("Employee Login")

    # add space and a divider 
    st.markdown("---")

    # create login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if username.strip() == "" or password.strip() == "":
                st.error("Please enter both username and password.")
            elif verify_credentials(username, password):
                st.success("Login successful!")
                # set a session state to remember the user is logged in
                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()
            else:
                st.error("Invalid username or password.")
