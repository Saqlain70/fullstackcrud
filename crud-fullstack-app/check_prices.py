import sqlite3

conn = sqlite3.connect('backend/crud_app.db')
cursor = conn.cursor()

cursor.execute('SELECT id, name, price FROM items')
rows = cursor.fetchall()

print("\n" + "="*50)
print("ITEMS IN DATABASE")
print("="*50)

for row in rows:
    id_val = row[0]
    name_val = row[1]
    price_val = row[2]
    
    # Print without formatting first
    print(f"ID: {id_val}")
    print(f"Name: {name_val}")
    print(f"Price (raw): {price_val}")
    print(f"Price type: {type(price_val)}")
    
    # Try different formatting methods
    try:
        print(f"Price formatted: ")
    except:
        print(f"Price as is: {price_val}")
    
    print("-"*30)

conn.close()
