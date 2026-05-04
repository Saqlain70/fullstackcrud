import sqlite3

# Connect to database
conn = sqlite3.connect('backend/crud_app.db')
cursor = conn.cursor()

# Get all items
cursor.execute('SELECT id, name, description, price, created_at FROM items')
rows = cursor.fetchall()

print("\n" + "="*70)
print("DATABASE CONTENTS")
print("="*70)

# Variable to calculate total
total_value = 0

for row in rows:
    # Extract values
    item_id = row[0]
    name = row[1]
    description = row[2]
    price = row[3]  # Price is at index 3
    created = row[4]
    
    # Add to total
    if price is not None:
        total_value += float(price)
    
    # Print each item
    print(f"\nID: {item_id}")
    print(f"Name: {name}")
    print(f"Description: {description if description else '(No description)'}")
    print(f"Price: " if price else "Price: .00")
    print(f"Created: {created}")
    print("-"*50)

# Print summary
print(f"\n📊 SUMMARY:")
print(f"   Total Items: {len(rows)}")
print(f"   Total Value: ")
print(f"   Average Price: " if len(rows) > 0 else "   Average Price: .00")
print("="*70)

conn.close()
