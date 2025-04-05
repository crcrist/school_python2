import streamlit as st
import sqlite3
import pandas as pd
import datetime
from db_setup import get_inventory_data

def update_catalog_data(brand, size, flavor, category, description, price, username, timestamp):
    """Add a new item to the catalog"""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    sql = "INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, (brand, size, flavor, category, description, price, username, timestamp))
    conn.commit()
    conn.close()
    return True
   
def update_item(item_id, brand, size, flavor, category, description, price):
    """Update an existing item in the catalog"""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    sql = "UPDATE catalog SET brand = ?, size = ?, flavor = ?, category = ?, description = ?, price = ? WHERE item_id = ?"
    cursor.execute(sql, (brand, size, flavor, category, description, price, item_id))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_item(item_id):
    """Delete an item from the catalog"""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    sql = "DELETE FROM catalog WHERE item_id = ?"
    cursor.execute(sql, (item_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def get_all_transactions():
    """Get all transactions for reporting"""
    conn = sqlite3.connect('example.db')
    query = """
    SELECT t.transaction_id, t.username, t.total_amount, 
           t.first_name, t.last_name, t.email, 
           t.payment_method, t.timestamp
    FROM transactions t
    ORDER BY t.timestamp DESC
    """
    transactions_df = pd.read_sql_query(query, conn)
    conn.close()
    return transactions_df

def employee_login():
    """Handle employee login"""
    st.title("Employee Login")
    
    with st.form("employee_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username.strip() == "" or password.strip() == "":
                st.error("Please enter both username and password.")
                return False
                
            # Connect to database
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()
            
            # Verify credentials
            query = "SELECT * FROM employees WHERE username = ? AND password = ?"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                st.success("Login successful!")
                st.session_state.username = username
                return True
            else:
                st.error("Invalid username or password.")
                return False
    
    return False

def employee_dashboard():
    """Employee dashboard for inventory management"""
    st.title(f"Employee Dashboard - Welcome, {st.session_state.username}!")
    
    # Create tabs for different management functions
    tab1, tab2, tab3, tab4 = st.tabs(["Inventory", "Add Item", "Edit/Delete Item", "Sales Reports"])
    
    inventory_df = get_inventory_data()
    
    # Inventory Tab
    with tab1:
        st.header("Current Inventory")
        st.dataframe(inventory_df, use_container_width=True)
        
        # Export data option
        # two separate buttons because the df must be converted to csv then downloadable
        if st.button("Export Inventory CSV"):
            # Convert DataFrame to CSV
            csv = inventory_df.to_csv(index=False)
            
            # Create a download button
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="inventory_export.csv",
                mime="text/csv"
            )
    
    # Add Item Tab
    with tab2:
        st.header("Add New Item to Catalog")
        
        with st.form("add_item_form"):
            brand = st.text_input("Brand")
            size = st.number_input("Size (oz)", min_value=0.0, value=12.0, step=0.1, format="%.1f")
            flavor = st.text_input("Flavor")
            category = st.selectbox("Category", 
                                   ["Energy", "Soda", "Water", "Sports", "Enhanced Water", 
                                    "Coffee", "Juice", "Tea", "Milk", "Protein", "Alternative Milk"])
            description = st.text_area("Description")
            price = st.number_input("Price ($)", min_value=0.01, value=1.99, step=0.10, format="%.2f")
            username = st.session_state.username
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if st.form_submit_button("Add Item"):
                # make sure form is filled out, if not retry
                if not all([brand, size > 0, flavor, category, price > 0]):
                    st.error("Please fill out all required fields.")
                else:
                    # tracking username and timestamp to see who makes inventory changes and when
                    if update_catalog_data(brand, size, flavor, category, description, price, username, timestamp):
                        st.success("Item added successfully!")
                        st.rerun()
    
    # Edit/Delete Item Tab
    with tab3:
        st.header("Edit or Delete Items")
        
        # Initialize session state for the delete confirmation if it doesn't exist
        # user should only be able to delete an item after checking the confirmation checkbox, that is why we initialize earlier
        if 'delete_confirmed' not in st.session_state:
            st.session_state.delete_confirmed = False
        
        # Select an item to edit/delete
        item_to_edit = st.selectbox("Select item to edit",
                                  inventory_df["item_id"].tolist(),
                                  # format the list to look nice
                                  format_func=lambda x: f"ID: {x} - {inventory_df[inventory_df['item_id']==x]['brand'].iloc[0]} ({inventory_df[inventory_df['item_id']==x]['flavor'].iloc[0]})",
                                  key="edit_select")
        
        # Get the specific item data
        selected_item_df = get_inventory_data(item_to_edit)
        
        if not selected_item_df.empty:
            # Get item data
            item = selected_item_df.iloc[0]
            
            # Create the form with both update and delete functionality
            with st.form("update_item_form"):
                st.subheader(f"Editing: {item['brand']} {item['flavor']}")
                
                edit_brand = st.text_input("Brand", value=item["brand"])
                # Convert size to float to avoid type mismatch
                size_value = float(item["size"])
                edit_size = st.number_input("Size (oz)", value=size_value, min_value=0.0, step=0.1, format="%.1f")
                edit_flavor = st.text_input("Flavor", value=item["flavor"])
                edit_category = st.selectbox("Category", 
                                           ["Energy", "Soda", "Water", "Sports", "Enhanced Water", 
                                            "Coffee", "Juice", "Tea", "Milk", "Protein", "Alternative Milk"],
                                           index=["Energy", "Soda", "Water", "Sports", "Enhanced Water", 
                                                 "Coffee", "Juice", "Tea", "Milk", "Protein", "Alternative Milk"].index(item["category"]) 
                                           if item["category"] in ["Energy", "Soda", "Water", "Sports", "Enhanced Water", 
                                                                 "Coffee", "Juice", "Tea", "Milk", "Protein", "Alternative Milk"] else 0)
                edit_description = st.text_area("Description", value=item["description"])
                price_value = float(item["price"])
                edit_price = st.number_input("Price ($)", value=price_value, min_value=0.01, step=0.10, format="%.2f")
                
                # Delete confirmation checkbox
                delete_confirmation = st.checkbox("I confirm I want to delete this item", 
                                                value=st.session_state.delete_confirmed,
                                                key="delete_confirm")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    update_button = st.form_submit_button("Update Item")
                
                with col2:
                    delete_button = st.form_submit_button("Delete Item")
            
            # Handle form submission
            if update_button:
                if not all([edit_brand, edit_size > 0, edit_flavor, edit_category, edit_price > 0]):
                    st.error("Please fill out all required fields.")
                else:
                    if update_item(item_to_edit, edit_brand, edit_size, edit_flavor, edit_category, edit_description, edit_price):
                        st.success("Item updated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to update item.")
            
            if delete_button:
                # checks to see if the deletion confirmation checkbox is clicked
                if delete_confirmation:
                    if delete_item(item_to_edit):
                        # set the delete_confirmed back to false to ensure checkbox must be clicked again to delete
                        st.session_state.delete_confirmed = False
                        st.success("Item deleted successfully!")
                        st.rerun()
                        # tried to make it so that the checkbox gets set back to default but there is an issue currently with that, need to fix
                    else:
                        st.error("Failed to delete item.")
                else:
                    st.warning("Please confirm deletion by checking the confirmation box.")
                    st.session_state.delete_confirmed = delete_confirmation
    
    # Sales Reports Tab
    with tab4:
        st.header("Sales Reports")
        
        # Get all transactions
        transactions_df = get_all_transactions()
        
        if transactions_df.empty:
            st.info("No sales transactions have been recorded yet.")
        else:
            # Show summary stats
            total_sales = transactions_df['total_amount'].sum()
            num_transactions = len(transactions_df)
            avg_order_value = total_sales / num_transactions if num_transactions > 0 else 0
            
            # Create metrics display
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Sales", f"${total_sales:.2f}")
            col2.metric("Transactions", num_transactions)
            col3.metric("Average Order", f"${avg_order_value:.2f}")
            
            # Transaction list
            st.subheader("Recent Transactions")
            st.dataframe(transactions_df, use_container_width=True)
            
            # Export option
            if st.button("Export Transactions CSV"):
                csv = transactions_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="transactions_export.csv",
                    mime="text/csv"
                )
            
            # View transaction details
            if not transactions_df.empty:
                transaction_to_view = st.selectbox(
                    "Select transaction to view details",
                    transactions_df["transaction_id"].tolist(),
                    # format transactions in dropbox to look nice
                    format_func=lambda x: f"ID: {x} - ${transactions_df[transactions_df['transaction_id']==x]['total_amount'].iloc[0]:.2f} ({transactions_df[transactions_df['transaction_id']==x]['timestamp'].iloc[0]})"
                )
                
                if transaction_to_view:
                    # Get transaction items
                    conn = sqlite3.connect('example.db')
                    items_query = """
                    SELECT ti.transaction_id, ti.item_id, ti.quantity, ti.price_per_item,
                        c.brand, c.flavor, c.size, c.category, c.description
                    FROM transaction_items ti
                    JOIN catalog c ON ti.item_id = c.item_id
                    WHERE ti.transaction_id = ?
                    """
                    
                    items_df = pd.read_sql_query(items_query, conn, params=(transaction_to_view,))
                    conn.close()
                    
                    if not items_df.empty:
                        st.subheader("Items Purchased")
                        st.dataframe(items_df[['brand', 'flavor', 'category', 'quantity', 'price_per_item']], use_container_width=True)
                        
                        total = (items_df['price_per_item'] * items_df['quantity']).sum()
                        st.write(f"Total: ${total:.2f}")
                    else:
                        st.info("No items found for this transaction.")
