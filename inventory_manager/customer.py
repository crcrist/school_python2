import streamlit as st
import sqlite3
import pandas as pd
import datetime
import uuid
from db_utils import get_inventory_data
from cart import (get_cart_items, add_to_cart, remove_from_cart, 
                 update_cart_quantity, clear_cart, process_transaction)

def customer_page():
    """Main customer shopping interface"""
    st.title("Welcome to the Beverage Store!")
    
    # Initialize session state for customer ID if it doesn't exist
    if 'customer_id' not in st.session_state:
        # Generate a unique customer ID for this session
        st.session_state.customer_id = f"guest_{uuid.uuid4().hex[:8]}"
    
    # Get tabs for the customer interface
    tab1, tab2, tab3 = st.tabs(["Shop", "Your Cart", "Order History"])
    
    # Get inventory data
    inventory_df = get_inventory_data()
    
    # Use the price from the database (no need to calculate)
    
    # Shop Tab
    with tab1:
        st.header("Available Beverages")
        st.write("Browse our selection and add items to your cart.")
        
        # Allow filtering by category
        categories = ["All"] + sorted(inventory_df['category'].unique().tolist())
        selected_category = st.selectbox("Filter by Category", categories)
        
        # Filter the dataframe based on selection
        if selected_category != "All":
            filtered_df = inventory_df[inventory_df['category'] == selected_category]
        else:
            filtered_df = inventory_df
        
        # Format the display dataframe
        display_df = filtered_df[['item_id', 'brand', 'flavor', 'size', 'category', 'description', 'price']]
        
        # Show the inventory in a nicer format
        st.dataframe(display_df, use_container_width=True)
        
        # Add to cart form
        with st.form("add_to_cart_form"):
            st.subheader("Add to Cart")
            col1, col2 = st.columns(2)
            
            with col1:
                item_to_add = st.selectbox(
                    "Select Item",
                    filtered_df["item_id"].tolist(),
                    format_func=lambda x: f"{filtered_df[filtered_df['item_id']==x]['brand'].iloc[0]} - {filtered_df[filtered_df['item_id']==x]['flavor'].iloc[0]} (${filtered_df[filtered_df['item_id']==x]['price'].iloc[0]:.2f})"
                )
            
            with col2:
                quantity = st.number_input("Quantity", min_value=1, value=1)
            
            add_button = st.form_submit_button("Add to Cart")
            
            if add_button:
                if add_to_cart(st.session_state.customer_id, item_to_add, quantity):
                    st.success(f"Added to cart: {filtered_df[filtered_df['item_id']==item_to_add]['brand'].iloc[0]} {filtered_df[filtered_df['item_id']==item_to_add]['flavor'].iloc[0]}")
    
    # Cart Tab
    with tab2:
        st.header("Your Shopping Cart")
        
        # Get cart items
        cart_df = get_cart_items(st.session_state.customer_id)
        
        if cart_df.empty:
            st.info("Your cart is empty. Add items from the Shop tab.")
        else:
            # Display cart items
            st.dataframe(cart_df[['brand', 'flavor', 'size', 'category', 'quantity', 'price']], use_container_width=True)
            
            # Calculate total
            total = (cart_df['price'] * cart_df['quantity']).sum()
            st.subheader(f"Total: ${total:.2f}")
            
            # Cart actions
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Empty Cart"):
                    clear_cart(st.session_state.customer_id)
                    st.success("Cart emptied!")
                    st.rerun()
            
            with col2:
                if st.button("Proceed to Checkout"):
                    st.session_state.checkout = True
                    st.rerun()
            
            # Edit quantities or remove items
            st.subheader("Edit Cart Items")
            for index, item in cart_df.iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"{item['brand']} {item['flavor']}")
                
                with col2:
                    new_qty = st.number_input(f"Qty", 
                                            min_value=0, 
                                            value=int(item['quantity']),
                                            key=f"qty_{item['cart_id']}")
                
                with col3:
                    if st.button("Update", key=f"update_{item['cart_id']}"):
                        update_cart_quantity(item['cart_id'], new_qty)
                        st.success("Cart updated!")
                        st.rerun()
            
            # Checkout section
            if 'checkout' in st.session_state and st.session_state.checkout:
                st.header("Checkout")
                st.write("Please provide your information to complete your purchase.")
                
                with st.form("checkout_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        first_name = st.text_input("First Name")
                        email = st.text_input("Email")
                        address = st.text_input("Address")
                        state = st.text_input("State")
                    
                    with col2:
                        last_name = st.text_input("Last Name")
                        phone = st.text_input("Phone")
                        city = st.text_input("City")
                        zip_code = st.text_input("ZIP Code")
                    
                    payment_method = st.selectbox("Payment Method", ["Credit Card", "PayPal", "Bank Transfer"])
                    
                    st.write(f"Total Amount: ${total:.2f}")
                    
                    purchase_button = st.form_submit_button("Complete Purchase")
                    
                    if purchase_button:
                        if not all([first_name, last_name, email, address, city, state, zip_code]):
                            st.error("Please fill out all required fields.")
                        else:
                            # Process the transaction
                            transaction_id = process_transaction(
                                st.session_state.customer_id, 
                                total, 
                                first_name, 
                                last_name, 
                                email, 
                                address, 
                                city, 
                                state, 
                                zip_code, 
                                payment_method
                            )
                            
                            st.success(f"Purchase completed! Transaction ID: {transaction_id}")
                            st.session_state.checkout = False
                            st.rerun()
    
    # Order History Tab
    with tab3:
        st.header("Your Recent Orders")
        
        # Notification that orders are session-based
        st.info("Order history is only available for the current session. For a full order history, please create an account in the future.")
        
        # Get transaction history for this session
        conn = sqlite3.connect('example.db')
        query = """
        SELECT transaction_id, total_amount, first_name, last_name, payment_method, timestamp
        FROM transactions
        WHERE username = ?
        ORDER BY timestamp DESC
        """
        
        transactions_df = pd.read_sql_query(query, conn, params=(st.session_state.customer_id,))
        conn.close()
        
        if transactions_df.empty:
            st.info("You haven't made any purchases in this session.")
        else:
            st.dataframe(transactions_df, use_container_width=True)
            
            # View transaction details
            transaction_to_view = st.selectbox(
                "Select transaction to view details",
                transactions_df["transaction_id"].tolist(),
                format_func=lambda x: f"Transaction {x} - ${transactions_df[transactions_df['transaction_id']==x]['total_amount'].iloc[0]:.2f} ({transactions_df[transactions_df['transaction_id']==x]['timestamp'].iloc[0]})"
            )
            
            if transaction_to_view:
                st.subheader(f"Items in Transaction #{transaction_to_view}")
                
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
                    st.dataframe(items_df[['brand', 'flavor', 'category', 'quantity', 'price_per_item']], use_container_width=True)
                    
                    total = (items_df['price_per_item'] * items_df['quantity']).sum()
                    st.write(f"Total: ${total:.2f}")
                else:
                    st.info("No items found for this transaction.")
