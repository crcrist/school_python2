import streamlit as st
import sqlite3
import hashlib

st.set_page_config(page_title="Employee Login System", layout="centered")

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
                print("login worked")
                # set a session state to remember the user is logged in
                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()
            else:
                st.error("Invalid username or password.")

def inventory_page():
    st.title(f"Welcome, {st.session_state.username}!")
    st.write("This is where inventory")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

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








