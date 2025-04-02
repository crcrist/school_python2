import sqlite3 

conn = sqlite3.connect('example.db')


# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS catalog (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT NOT NULL,
                    size INTEGER,
                    flavor TEXT,
                    category TEXT,
                    description TEXT,
                    username TEXT,
                    timestamp TEXT
                )''')

# Insert data into the table
# Energy Drinks
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Monster', 16, 'Original', 'Energy', '160mg caffeine, zero sugar', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Red Bull', 12, 'Original', 'Energy', '114mg caffeine, vitamin B', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Red Bull', 8.4, 'Sugar Free', 'Energy', '80mg caffeine, zero sugar', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Celsius', 12, 'Wild Berry', 'Energy', '200mg caffeine, essential energy', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Celsius', 12, 'Orange', 'Energy', '200mg caffeine, essential energy', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Bang', 16, 'Cotton Candy', 'Energy', '300mg caffeine, zero sugar', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Reign', 16, 'Melon Mania', 'Energy', '300mg caffeine, BCAA amino acids', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('C4', 16, 'Frozen Bombsicle', 'Energy', '200mg caffeine, performance energy', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Rockstar', 16, 'Punched', 'Energy', '240mg caffeine, fruit punch flavor', NULL, NULL)''')

# Sodas
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Coca-Cola', 20, 'Original', 'Soda', 'Classic cola taste', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Coca-Cola', 12, 'Diet', 'Soda', 'Zero calories', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Pepsi', 20, 'Original', 'Soda', 'Bold cola flavor', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Mountain Dew', 20, 'Original', 'Soda', 'Citrus soda, high caffeine', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Dr Pepper', 20, 'Original', 'Soda', '23 flavors blend', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Sprite', 20, 'Lemon-Lime', 'Soda', 'Crisp lemon-lime taste', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Fanta', 20, 'Orange', 'Soda', 'Orange flavor soda', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('A&W', 20, 'Root Beer', 'Soda', 'Creamy root beer', NULL, NULL)''')

# Waters
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Dasani', 20, 'Plain', 'Water', 'Purified water', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Smartwater', 20, 'Plain', 'Water', 'Vapor distilled water with electrolytes', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('LIFEWTR', 20, 'Plain', 'Water', 'pH balanced purified water', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Aquafina', 20, 'Plain', 'Water', 'Purified drinking water', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Fiji', 16.9, 'Plain', 'Water', 'Natural artesian water', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Core', 30, 'Plain', 'Water', 'Perfect pH balanced water', NULL, NULL)''')

# Sports Drinks
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Gatorade', 28, 'Cool Blue', 'Sports', 'Electrolytes and carbs', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Gatorade', 28, 'Fruit Punch', 'Sports', 'Electrolytes and carbs', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Gatorade', 28, 'Lemon-Lime', 'Sports', 'Electrolytes and carbs', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Powerade', 28, 'Mountain Berry Blast', 'Sports', 'ION4 advanced electrolyte system', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Body Armor', 28, 'Strawberry Banana', 'Sports', 'Coconut water electrolytes', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Propel', 20, 'Berry', 'Sports', 'Electrolyte water, vitamin enhanced', NULL, NULL)''')

# Flavored/Enhanced Waters
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Vitaminwater', 20, 'XXX (Acai-Blueberry-Pomegranate)', 'Enhanced Water', 'Vitamins B5, B6, B12', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Vitaminwater', 20, 'Power-C (Dragonfruit)', 'Enhanced Water', 'Vitamin C and B vitamins', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Bai', 18, 'Cocofusion', 'Enhanced Water', '5 calories, antioxidants, infused with coconut', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Hint', 16, 'Watermelon', 'Flavored Water', 'Zero sweeteners, zero calories', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Sparkling Ice', 17, 'Black Raspberry', 'Sparkling Water', 'Zero sugar, vitamins and antioxidants', NULL, NULL)''')

# Cold Coffee Drinks
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Starbucks', 13.7, 'Vanilla Frappuccino', 'Coffee', 'Chilled coffee drink', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Starbucks', 13.7, 'Mocha Frappuccino', 'Coffee', 'Chilled coffee drink', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Dunkin', 13.7, 'Original', 'Coffee', 'Cold brew coffee', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Monster Java', 15, 'Mean Bean', 'Coffee', 'Coffee + energy blend', NULL, NULL)''')

# Juices
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Simply', 52, 'Orange', 'Juice', '100% pure-squeezed orange juice', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Ocean Spray', 64, 'Cranberry', 'Juice', 'Cranberry juice cocktail', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Minute Maid', 12, 'Orange', 'Juice', 'From concentrate', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Snapple', 16, 'Peach Tea', 'Tea', 'Real brewed tea', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Arizona', 23, 'Green Tea with Honey', 'Tea', 'Ginseng and honey', NULL, NULL)''')

# Dairy/Alternative
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Fairlife', 14, 'Chocolate', 'Milk', 'Ultra-filtered, high protein milk', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Muscle Milk', 14, 'Vanilla', 'Protein', '25g protein, workout recovery', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Core Power', 14, 'Chocolate', 'Protein', '26g protein, athletic recovery', NULL, NULL)''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description, username, timestamp)
                  VALUES ('Silk', 32, 'Original', 'Alternative Milk', 'Almond milk', NULL, NULL)''')
# Select and fetch data
cursor.execute('SELECT * FROM catalog')
rows = cursor.fetchall()
 
for row in rows:
    print(row)
 
# Commit the transaction
conn.commit()
 
# Close the connection
conn.close()



