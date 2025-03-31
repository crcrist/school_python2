import sqlite3 

conn = sqlite3.connect('example.db')

# Create a cursor object
cursor = conn.cursor()
 
# Select and fetch data
cursor.execute('drop table employees')
rows = cursor.fetchall()
 
 
# Commit the transaction
conn.commit()
 
# Close the connection
conn.close()


