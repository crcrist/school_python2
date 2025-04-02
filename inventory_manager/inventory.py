import streamlit as st
import sqlite3
import pandas as pd
import datetime

def get_inventory_data(item_id=None):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    if item_id is not None:
        query = "SELECT * FROM catalog WHERE item_id = ?"
        df = pd.read_sql_query(query, conn, params=(item_id,))
    else:
        df = pd.read_sql_query("select * from catalog", conn)

    conn.close()
    return df

def update_catalog_data(brand, size, flavor, category, description, username, timestamp):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    sql = f"INSERT INTO catalog (brand, size, flavor, category, description = ?  VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, (brand, size, flavor, category, description, username, timestamp))
    conn.commit()
    st.write("inserted successfully")
    conn.close()
   
def update_item(item_id, brand, size, flavor, category, description):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    sql = "UPDATE catalog SET brand = ?, size = ?, flavor = ?, category = ?, description = ? where item_id = ?"
    cursor.execute(sql, (brand, size, flavor, category, description, item_id))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_item(item_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    sql = "DELETE from catalog where item_id = ?"
    cursor.execute(sql, (item_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def inventory_page():
    st.title(f"Welcome, {st.session_state.username}!")
    
    tab1, tab2, tab3 = st.tabs(["View Catalog", "Add Item", "Edit/Delete Item"])
    
    inventory_df = get_inventory_data()
    
    with tab1:
        st.write("This is where inventory")
        st.dataframe(inventory_df, use_container_width=True)
        
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
            username = st.session_state.username
            timestamp = datetime.datetime.now()
            
            if st.form_submit_button("Add Item"):
                update_catalog_data(brand, size, flavor, category, description, username, timestamp) 
                st.success("item added!")
                st.rerun()  # refresh to show data
    
    with tab3:
        # Initialize session state for the delete confirmation if it doesn't exist
        if 'delete_confirmed' not in st.session_state:
            st.session_state.delete_confirmed = False
        
        # Select an item to edit/delete
        item_to_edit = st.selectbox("Select item",
                                  inventory_df["item_id"].tolist(),
                                  format_func=lambda x: f"ID: {x} - {inventory_df[inventory_df['item_id']==x]['brand'].iloc[0]} ({inventory_df[inventory_df['item_id']==x]['flavor'].iloc[0]})")
        
        # Get the specific item data using the secure method
        selected_item_df = get_inventory_data(item_to_edit)
        
        if not selected_item_df.empty:
            # Only show the update form
            st.write("### Update Item")
            
            # Get item data
            item = selected_item_df.iloc[0]
            
            # Create the form with both update and delete functionality
            with st.form("update_form"):
                edit_brand = st.text_input("Brand", value=item["brand"])
                edit_size = st.number_input("Size", value=item["size"], min_value=0)
                edit_flavor = st.text_input("Flavor", value=item["flavor"])
                edit_category = st.text_input("Category", value=item["category"])
                edit_description = st.text_input("Description", value=item["description"])
                
                # Delete confirmation checkbox - using the session state to control its value
                delete_confirmation = st.checkbox("I confirm I want to delete this item", 
                                                value=st.session_state.delete_confirmed,
                                                key="delete_confirmation_checkbox")
                
                # Create columns for the buttons side by side
                col1, col2 = st.columns(2)
                
                with col1:
                    update_button = st.form_submit_button("Update Item")
                
                with col2:
                    delete_button = st.form_submit_button("Delete Item")
                
            # Handle form submission (outside the form)
            if update_button:
                if update_item(item_to_edit, edit_brand, edit_size, edit_flavor, edit_category, edit_description):
                    st.success("Item updated successfully!")
                    st.rerun()  # Refresh to show updated data
                else:
                    st.error("Failed to update item.")
            
            if delete_button:
                if delete_confirmation:
                    if delete_item(item_to_edit):
                        # Reset the confirmation checkbox state
                        st.session_state.delete_confirmed = False
                        st.success("Item deleted successfully!")
                        st.rerun()  # Refresh to show updated data
                    else:
                        st.error("Failed to delete item.")
                else:
                    st.warning("Please confirm deletion by checking the confirmation box.")
                    # Optionally capture the current state
                    st.session_state.delete_confirmed = delete_confirmation
