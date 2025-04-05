import sqlite3
import streamlit as st
import pandas as pd

def get_inventory_data(item_id=None):
    """Get inventory data from the catalog table"""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    if item_id is not None:
        query = "SELECT * FROM catalog WHERE item_id = ?"
        df = pd.read_sql_query(query, conn, params=(item_id,))
    else:
        df = pd.read_sql_query("SELECT * FROM catalog", conn)

    conn.close()
    return df

def is_database_initialized():
    """Check if the database has already been initialized by checking for tables
        Adding this logic as initially the print statement for initialization was being reprinted 
        everytime the app was refreshed on rerun()"""
    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        
        # Check if all required tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name='catalog' OR name='employees' OR name='cart' OR name='transactions' OR name='transaction_items')")
        tables = cursor.fetchall()
        
        conn.close()
        
        # Return True if all 5 required tables exist
        return len(tables) == 5
    except:
        return False

def initialize_database():
    """Create all necessary tables and populate with initial data"""
    # Check if database is already initialized
    if 'db_initialized' in st.session_state and st.session_state.db_initialized:
        return
    
    # Check if the database has tables already
    if is_database_initialized():
        # Just set the flag and return without printing
        st.session_state.db_initialized = True
        return
    
    # Connect to the database
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # Create catalog table
    cursor.execute('''CREATE TABLE IF NOT EXISTS catalog (
                        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        brand TEXT NOT NULL,
                        size REAL,
                        flavor TEXT,
                        category TEXT,
                        description TEXT,
                        price REAL NOT NULL,
                        username TEXT,
                        timestamp TEXT
                    )''')
    
    # Create cart table
    cursor.execute('''CREATE TABLE IF NOT EXISTS cart (
                        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        item_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL DEFAULT 1,
                        timestamp TEXT,
                        FOREIGN KEY (item_id) REFERENCES catalog(item_id)
                    )''')
    
    # Create transactions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        total_amount REAL NOT NULL,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        address TEXT NOT NULL,
                        city TEXT NOT NULL,
                        state TEXT NOT NULL,
                        zip_code TEXT NOT NULL,
                        payment_method TEXT NOT NULL,
                        timestamp TEXT NOT NULL
                    )''')
    
    # Create transaction_items table
    cursor.execute('''CREATE TABLE IF NOT EXISTS transaction_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        transaction_id INTEGER NOT NULL,
                        item_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        price_per_item REAL NOT NULL,
                        FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
                        FOREIGN KEY (item_id) REFERENCES catalog(item_id)
                    )''')
    
    # Create employees table
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER,
                        department TEXT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )''')
    
    # Check if catalog already has data to avoid duplicating entries
    cursor.execute("SELECT COUNT(*) FROM catalog")
    catalog_count = cursor.fetchone()[0]
    
    # Check if employees table already has data
    cursor.execute("SELECT COUNT(*) FROM employees")
    employee_count = cursor.fetchone()[0]
    
    # Populate catalog data if empty
    if catalog_count == 0:
        # Energy Drinks
        cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                        VALUES ('Monster', 16, 'Original', 'Energy', '160mg caffeine, zero sugar', 3.49, NULL, NULL)''')
        cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                        VALUES ('Red Bull', 12, 'Original', 'Energy', '114mg caffeine, vitamin B', 2.99, NULL, NULL)''')
        cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                        VALUES ('Red Bull', 8.4, 'Sugar Free', 'Energy', '80mg caffeine, zero sugar', 2.49, NULL, NULL)''')
        cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                        VALUES ('Celsius', 12, 'Wild Berry', 'Energy', '200mg caffeine, essential energy', 2.79, NULL, NULL)''')
        cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                        VALUES ('Celsius', 12, 'Orange', 'Energy', '200mg caffeine, essential energy', 2.79, NULL, NULL)''')
        
        # Sodas
        cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                        VALUES ('Coca-Cola', 20, 'Original', 'Soda', 'Classic cola taste', 1.99, NULL, NULL)''')
        cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                        VALUES ('Coca-Cola', 12, 'Diet', 'Soda', 'Zero calories', 1.59, NULL, NULL)''')
        cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                        VALUES ('Pepsi', 20, 'Original', 'Soda', 'Bold cola flavor', 1.99, NULL, NULL)''')
        
        # Waters
        cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                        VALUES ('Dasani', 20, 'Plain', 'Water', 'Purified water', 1.29, NULL, NULL)''')
        cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                        VALUES ('Smartwater', 20, 'Plain', 'Water', 'Vapor distilled water with electrolytes', 2.19, NULL, NULL)''')
        
        # Sports Drinks
        cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                        VALUES ('Gatorade', 28, 'Cool Blue', 'Sports', 'Electrolytes and carbs', 2.49, NULL, NULL)''')
        cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                        VALUES ('Gatorade', 28, 'Fruit Punch', 'Sports', 'Electrolytes and carbs', 2.49, NULL, NULL)''')
    
    # Populate employee data if empty
    if employee_count == 0:
        cursor.execute('''INSERT INTO employees (name, age, department, username, password)
                        VALUES ('John Doe', 30, 'admin', 'username', 'password')''')
        cursor.execute('''INSERT INTO employees (name, age, department, username, password)
                        VALUES ('Jane Smith', 28, 'manager', 'jane', 'password123')''')
    
    # Commit and close
    conn.commit()
    conn.close()
    
    # Print only on the first initialization
    print("Database initialized with tables and sample data!")
    
    # Set session state flag to indicate initialization is done
    st.session_state.db_initialized = True
