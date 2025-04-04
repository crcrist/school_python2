import sqlite3 

# Connect to database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Check if catalog table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='catalog'")
table_exists = cursor.fetchone()

# If table exists, drop it to recreate with price
if table_exists:
    cursor.execute("DROP TABLE catalog")

# Create catalog table with price field
cursor.execute('''CREATE TABLE IF NOT EXISTS catalog (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT NOT NULL,
                    size INTEGER,
                    flavor TEXT,
                    category TEXT,
                    description TEXT,
                    price REAL NOT NULL,
                    username TEXT,
                    timestamp TEXT
                )''')

# Insert data into the table with prices
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
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Bang', 16, 'Cotton Candy', 'Energy', '300mg caffeine, zero sugar', 3.29, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Reign', 16, 'Melon Mania', 'Energy', '300mg caffeine, BCAA amino acids', 3.29, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('C4', 16, 'Frozen Bombsicle', 'Energy', '200mg caffeine, performance energy', 3.19, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Rockstar', 16, 'Punched', 'Energy', '240mg caffeine, fruit punch flavor', 2.99, NULL, NULL)''')

# Sodas
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Coca-Cola', 20, 'Original', 'Soda', 'Classic cola taste', 1.99, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Coca-Cola', 12, 'Diet', 'Soda', 'Zero calories', 1.59, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Pepsi', 20, 'Original', 'Soda', 'Bold cola flavor', 1.99, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Mountain Dew', 20, 'Original', 'Soda', 'Citrus soda, high caffeine', 1.99, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Dr Pepper', 20, 'Original', 'Soda', '23 flavors blend', 1.99, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Sprite', 20, 'Lemon-Lime', 'Soda', 'Crisp lemon-lime taste', 1.99, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Fanta', 20, 'Orange', 'Soda', 'Orange flavor soda', 1.99, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('A&W', 20, 'Root Beer', 'Soda', 'Creamy root beer', 1.99, NULL, NULL)''')

# Waters
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Dasani', 20, 'Plain', 'Water', 'Purified water', 1.29, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Smartwater', 20, 'Plain', 'Water', 'Vapor distilled water with electrolytes', 2.19, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('LIFEWTR', 20, 'Plain', 'Water', 'pH balanced purified water', 2.19, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Aquafina', 20, 'Plain', 'Water', 'Purified drinking water', 1.29, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Fiji', 16.9, 'Plain', 'Water', 'Natural artesian water', 2.59, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Core', 30, 'Plain', 'Water', 'Perfect pH balanced water', 2.79, NULL, NULL)''')

# Sports Drinks
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Gatorade', 28, 'Cool Blue', 'Sports', 'Electrolytes and carbs', 2.49, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Gatorade', 28, 'Fruit Punch', 'Sports', 'Electrolytes and carbs', 2.49, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Gatorade', 28, 'Lemon-Lime', 'Sports', 'Electrolytes and carbs', 2.49, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Powerade', 28, 'Mountain Berry Blast', 'Sports', 'ION4 advanced electrolyte system', 2.29, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Body Armor', 28, 'Strawberry Banana', 'Sports', 'Coconut water electrolytes', 2.79, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Propel', 20, 'Berry', 'Sports', 'Electrolyte water, vitamin enhanced', 1.99, NULL, NULL)''')

# Flavored/Enhanced Waters
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Vitaminwater', 20, 'XXX (Acai-Blueberry-Pomegranate)', 'Enhanced Water', 'Vitamins B5, B6, B12', 2.29, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Vitaminwater', 20, 'Power-C (Dragonfruit)', 'Enhanced Water', 'Vitamin C and B vitamins', 2.29, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Bai', 18, 'Cocofusion', 'Enhanced Water', '5 calories, antioxidants, infused with coconut', 2.49, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Hint', 16, 'Watermelon', 'Flavored Water', 'Zero sweeteners, zero calories', 2.19, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Sparkling Ice', 17, 'Black Raspberry', 'Sparkling Water', 'Zero sugar, vitamins and antioxidants', 1.69, NULL, NULL)''')

# Cold Coffee Drinks
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Starbucks', 13.7, 'Vanilla Frappuccino', 'Coffee', 'Chilled coffee drink', 3.99, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Starbucks', 13.7, 'Mocha Frappuccino', 'Coffee', 'Chilled coffee drink', 3.99, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Dunkin', 13.7, 'Original', 'Coffee', 'Cold brew coffee', 3.79, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Monster Java', 15, 'Mean Bean', 'Coffee', 'Coffee + energy blend', 3.49, NULL, NULL)''')

# Juices
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Simply', 52, 'Orange', 'Juice', '100% pure-squeezed orange juice', 4.99, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Ocean Spray', 64, 'Cranberry', 'Juice', 'Cranberry juice cocktail', 3.99, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Minute Maid', 12, 'Orange', 'Juice', 'From concentrate', 1.49, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Snapple', 16, 'Peach Tea', 'Tea', 'Real brewed tea', 2.19, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Arizona', 23, 'Green Tea with Honey', 'Tea', 'Ginseng and honey', 1.29, NULL, NULL)''')

# Dairy/Alternative
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Fairlife', 14, 'Chocolate', 'Milk', 'Ultra-filtered, high protein milk', 2.99, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Muscle Milk', 14, 'Vanilla', 'Protein', '25g protein, workout recovery', 3.79, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Core Power', 14, 'Chocolate', 'Protein', '26g protein, athletic recovery', 3.99, NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, price, username, timestamp)
                  VALUES ('Silk', 32, 'Original', 'Alternative Milk', 'Almond milk', 3.49, NULL, NULL)''')

# Select and fetch data
cursor.execute('SELECT * FROM catalog')
rows = cursor.fetchall()
 
print("Catalog table updated with price field. Sample data:")
for i, row in enumerate(rows):
    if i < 5:  # Print just the first 5 rows as a sample
        print(row)
    else:
        break
 
print(f"Total items in catalog: {len(rows)}")

# Commit the transaction
conn.commit()
 
# Close the connection
conn.close()
