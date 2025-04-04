# streamlit run main.py

import streamlit as st
import sqlite3
from cart_transaction_load import create_cart_transaction_tables
from customer import customer_page
from employee import employee_login, employee_dashboard

st.set_page_config(page_title="Beverage Store", layout="wide")

def main():
    # Create tables if they don't exist
    create_cart_transaction_tables()
    
    # Initialize session states
    if 'employee_logged_in' not in st.session_state:
        st.session_state.employee_logged_in = False
    
    if 'active_view' not in st.session_state:
        st.session_state.active_view = "customer"
    
    # Main navigation
    if st.session_state.active_view == "customer" and not st.session_state.employee_logged_in:
        # Show a small button in the sidebar for employee login
        with st.sidebar:
            st.write("## Employee Access")
            if st.button("Employee Login"):
                st.session_state.active_view = "employee_login"
                st.rerun()
        
        # Show the customer shopping interface
        customer_page()
        
    elif st.session_state.active_view == "employee_login" and not st.session_state.employee_logged_in:
        # Show employee login page
        if employee_login():
            st.session_state.employee_logged_in = True
            st.session_state.active_view = "employee_dashboard"
            st.rerun()
        
        # Back button to return to customer view
        if st.button("Back to Store"):
            st.session_state.active_view = "customer"
            st.rerun()
            
    elif st.session_state.employee_logged_in:
        # Show employee dashboard
        employee_dashboard()
        
        # Logout button
        with st.sidebar:
            if st.button("Logout"):
                st.session_state.employee_logged_in = False
                st.session_state.active_view = "customer"
                st.rerun()

if __name__ == "__main__":
    main()
