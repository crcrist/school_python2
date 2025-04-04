import sqlite3

def create_cart_transaction_tables():
    # Connect to the database
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # Create cart table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        timestamp TEXT,
        FOREIGN KEY (item_id) REFERENCES catalog(item_id)
    )
    ''')
    
    # Create transactions table (fact table)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
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
    )
    ''')
    
    # Create transaction_items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transaction_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price_per_item REAL NOT NULL,
        FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
        FOREIGN KEY (item_id) REFERENCES catalog(item_id)
    )
    ''')
    
    # Commit and close
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_cart_transaction_tables()
    print("Cart and transaction tables created successfully!")
