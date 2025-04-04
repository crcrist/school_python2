import streamlit as st
import sqlite3
import pandas as pd
import datetime
from db_utils import get_inventory_data

def get_cart_items(username):
    """Get all items in the user's cart with item details"""
    conn = sqlite3.connect('example.db')
    
    # Join cart with catalog to get item details
    query = """
    SELECT c.cart_id, c.username, c.item_id, c.quantity, c.timestamp,
           cat.brand, cat.flavor, cat.size, cat.category, cat.description,
           cat.price  -- Use actual price from database
    FROM cart c
    JOIN catalog cat ON c.item_id = cat.item_id
    WHERE c.username = ?
    """
    
    try:
        cart_df = pd.read_sql_query(query, conn, params=(username,))
    except:
        # If there's an error (e.g., table doesn't exist yet), return an empty DataFrame
        cart_df = pd.DataFrame(columns=['cart_id', 'username', 'item_id', 'quantity', 'timestamp', 
                                        'brand', 'flavor', 'size', 'category', 'description', 'price'])
    
    conn.close()
    
    return cart_df

def add_to_cart(username, item_id, quantity=1):
    """Add an item to the user's cart"""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # Check if item already in cart
    cursor.execute("SELECT cart_id, quantity FROM cart WHERE username = ? AND item_id = ?", 
                  (username, item_id))
    existing = cursor.fetchone()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if existing:
        # Update quantity if already in cart
        cart_id, current_qty = existing
        new_qty = current_qty + quantity
        cursor.execute("UPDATE cart SET quantity = ?, timestamp = ? WHERE cart_id = ?", 
                      (new_qty, timestamp, cart_id))
    else:
        # Add new item to cart
        cursor.execute("INSERT INTO cart (username, item_id, quantity, timestamp) VALUES (?, ?, ?, ?)",
                      (username, item_id, quantity, timestamp))
    
    conn.commit()
    conn.close()
    return True

def remove_from_cart(cart_id):
    """Remove an item from the cart"""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM cart WHERE cart_id = ?", (cart_id,))
    
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def update_cart_quantity(cart_id, quantity):
    """Update the quantity of an item in the cart"""
    if quantity <= 0:
        return remove_from_cart(cart_id)
    
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    cursor.execute("UPDATE cart SET quantity = ? WHERE cart_id = ?", (quantity, cart_id))
    
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def clear_cart(username):
    """Remove all items from the user's cart"""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM cart WHERE username = ?", (username,))
    
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def process_transaction(username, total_amount, first_name, last_name, email, 
                        address, city, state, zip_code, payment_method):
    """Process the transaction and save to the database"""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Insert into transactions table
    cursor.execute("""
    INSERT INTO transactions 
    (username, total_amount, first_name, last_name, email, address, city, state, zip_code, payment_method, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, total_amount, first_name, last_name, email, address, city, state, zip_code, payment_method, timestamp))
    
    # Get the transaction_id
    transaction_id = cursor.lastrowid
    
    # Get cart items
    cart_df = get_cart_items(username)
    
    # Insert each cart item into transaction_items
    for index, item in cart_df.iterrows():
        price_per_item = item['price']
        cursor.execute("""
        INSERT INTO transaction_items 
        (transaction_id, item_id, quantity, price_per_item)
        VALUES (?, ?, ?, ?)
        """, (transaction_id, item['item_id'], item['quantity'], price_per_item))
    
    # Clear the cart
    cursor.execute("DELETE FROM cart WHERE username = ?", (username,))
    
    conn.commit()
    conn.close()
    
    return transaction_id

def get_transaction_history(username):
    """Get transaction history for a user"""
    conn = sqlite3.connect('example.db')
    
    query = """
    SELECT transaction_id, total_amount, first_name, last_name, payment_method, timestamp
    FROM transactions
    WHERE username = ?
    ORDER BY timestamp DESC
    """
    
    transactions_df = pd.read_sql_query(query, conn, params=(username,))
    conn.close()
    
    return transactions_df

def get_transaction_items(transaction_id):
    """Get items for a specific transaction"""
    conn = sqlite3.connect('example.db')
    
    query = """
    SELECT ti.transaction_id, ti.item_id, ti.quantity, ti.price_per_item,
           c.brand, c.flavor, c.size, c.category, c.description
    FROM transaction_items ti
    JOIN catalog c ON ti.item_id = c.item_id
    WHERE ti.transaction_id = ?
    """
    
    items_df = pd.read_sql_query(query, conn, params=(transaction_id,))
    conn.close()
    
    return items_df
