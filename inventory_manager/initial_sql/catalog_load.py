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
                    description TEXT
                )''')

# Insert data into the table
# Energy Drinks
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Monster', 16, 'Original', 'Energy', '160mg caffeine, zero sugar')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Red Bull', 12, 'Original', 'Energy', '114mg caffeine, vitamin B')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Red Bull', 8.4, 'Sugar Free', 'Energy', '80mg caffeine, zero sugar')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Celsius', 12, 'Wild Berry', 'Energy', '200mg caffeine, essential energy')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Celsius', 12, 'Orange', 'Energy', '200mg caffeine, essential energy')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Bang', 16, 'Cotton Candy', 'Energy', '300mg caffeine, zero sugar')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Reign', 16, 'Melon Mania', 'Energy', '300mg caffeine, BCAA amino acids')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('C4', 16, 'Frozen Bombsicle', 'Energy', '200mg caffeine, performance energy')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Rockstar', 16, 'Punched', 'Energy', '240mg caffeine, fruit punch flavor')''')

# Sodas
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Coca-Cola', 20, 'Original', 'Soda', 'Classic cola taste')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Coca-Cola', 12, 'Diet', 'Soda', 'Zero calories')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Pepsi', 20, 'Original', 'Soda', 'Bold cola flavor')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Mountain Dew', 20, 'Original', 'Soda', 'Citrus soda, high caffeine')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Dr Pepper', 20, 'Original', 'Soda', '23 flavors blend')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Sprite', 20, 'Lemon-Lime', 'Soda', 'Crisp lemon-lime taste')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Fanta', 20, 'Orange', 'Soda', 'Orange flavor soda')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('A&W', 20, 'Root Beer', 'Soda', 'Creamy root beer')''')

# Waters
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Dasani', 20, 'Plain', 'Water', 'Purified water')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Smartwater', 20, 'Plain', 'Water', 'Vapor distilled water with electrolytes')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('LIFEWTR', 20, 'Plain', 'Water', 'pH balanced purified water')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Aquafina', 20, 'Plain', 'Water', 'Purified drinking water')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Fiji', 16.9, 'Plain', 'Water', 'Natural artesian water')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Core', 30, 'Plain', 'Water', 'Perfect pH balanced water')''')

# Sports Drinks
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Gatorade', 28, 'Cool Blue', 'Sports', 'Electrolytes and carbs')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Gatorade', 28, 'Fruit Punch', 'Sports', 'Electrolytes and carbs')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Gatorade', 28, 'Lemon-Lime', 'Sports', 'Electrolytes and carbs')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Powerade', 28, 'Mountain Berry Blast', 'Sports', 'ION4 advanced electrolyte system')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Body Armor', 28, 'Strawberry Banana', 'Sports', 'Coconut water electrolytes')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Propel', 20, 'Berry', 'Sports', 'Electrolyte water, vitamin enhanced')''')

# Flavored/Enhanced Waters
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Vitaminwater', 20, 'XXX (Acai-Blueberry-Pomegranate)', 'Enhanced Water', 'Vitamins B5, B6, B12')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Vitaminwater', 20, 'Power-C (Dragonfruit)', 'Enhanced Water', 'Vitamin C and B vitamins')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Bai', 18, 'Cocofusion', 'Enhanced Water', '5 calories, antioxidants, infused with coconut')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Hint', 16, 'Watermelon', 'Flavored Water', 'Zero sweeteners, zero calories')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Sparkling Ice', 17, 'Black Raspberry', 'Sparkling Water', 'Zero sugar, vitamins and antioxidants')''')

# Cold Coffee Drinks
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Starbucks', 13.7, 'Vanilla Frappuccino', 'Coffee', 'Chilled coffee drink')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Starbucks', 13.7, 'Mocha Frappuccino', 'Coffee', 'Chilled coffee drink')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Dunkin', 13.7, 'Original', 'Coffee', 'Cold brew coffee')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Monster Java', 15, 'Mean Bean', 'Coffee', 'Coffee + energy blend')''')

# Juices
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Simply', 52, 'Orange', 'Juice', '100% pure-squeezed orange juice')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Ocean Spray', 64, 'Cranberry', 'Juice', 'Cranberry juice cocktail')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Minute Maid', 12, 'Orange', 'Juice', 'From concentrate')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Snapple', 16, 'Peach Tea', 'Tea', 'Real brewed tea')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Arizona', 23, 'Green Tea with Honey', 'Tea', 'Ginseng and honey')''')

# Dairy/Alternative
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Fairlife', 14, 'Chocolate', 'Milk', 'Ultra-filtered, high protein milk')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Muscle Milk', 14, 'Vanilla', 'Protein', '25g protein, workout recovery')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Core Power', 14, 'Chocolate', 'Protein', '26g protein, athletic recovery')''')
cursor.execute('''INSERT INTO catalog (brand, size, flavor, category, description)
                  VALUES ('Silk', 32, 'Original', 'Alternative Milk', 'Almond milk')''')

# Select and fetch data
cursor.execute('SELECT * FROM catalog')
rows = cursor.fetchall()
 
for row in rows:
    print(row)
 
# Commit the transaction
conn.commit()
 
# Close the connection
conn.close()



