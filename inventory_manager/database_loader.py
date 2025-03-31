import sqlite3 

conn = sqlite3.connect('example.db')


# Create a cursor object
cursor = conn.cursor()
 
# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    department TEXT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')

# Insert data into the table
cursor.execute('''INSERT INTO employees (name, age, department, username, password)
                  VALUES ('John Doe', 30, 'admin', 'username', 'password')''')

# Select and fetch data
cursor.execute('SELECT * FROM employees')
rows = cursor.fetchall()
 
for row in rows:
    print(row)
 
# Commit the transaction
conn.commit()
 
# Close the connection
conn.close()



