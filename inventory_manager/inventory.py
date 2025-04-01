import streamlit as st
import sqlite3
import pandas as pd

def get_inventory_data():
    conn = sqlite3.connect('example.db')
    df = pd.read_sql_query("SELECT * FROM inventory", conn)
    conn.close()
    return df

def inventory_page():
    st.title(f"Welcome, {st.session_state.username}!")
    
    tab1, tab2, tab3 = st.tabs(["View Catalog", "Add Item", "Edit/Delete Item"])
    
    inventory_df = get_inventory_data()
    
    with tab1:
        st.write("This is where inventory")
        st.dataframe(inventory_df, use_container_width=True)
        
        st.button("button1", 
                help="here is example of help", 
                on_click=lambda: print("this would do the thing in sql"),
                type="primary",
                icon="🚨")
        
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()
    
    with tab2:
        with st.form("add_item_form"):
            brand = st.text_input("Brand")
            size = st.number_input("Size", min_value=0)
            flavor = st.text_input("Flavor")
            category = st.text_input("Category")
            description = st.text_input("Description")
            
            if st.form_submit_button("Add Item"):
                st.success("item added!")
                st.rerun()  # refresh to show data
    
    with tab3:
        item_to_edit = st.selectbox("Select item to edit",
                                    inventory_df["item_id"].tolist(),
                                    format_func=lambda x: f"ID: {x} - {inventory_df[inventory_df['item_id']==x]['brand'].iloc[0]}")
