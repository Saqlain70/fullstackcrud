import sqlite3

conn = sqlite3.connect('backend/crud_app.db')
cursor = conn.cursor()

print("\n" + "="*70)
print("YOUR DATABASE CONTENTS")
print("="*70)

cursor.execute("SELECT id, name, price, created_at FROM items")
items = cursor.fetchall()

if items:
    for item in items:
        print(f"\nID: {item[0]}")
        print(f"Name: {item[1]}")
        # FIXED: Access price at index 2 and format it
        price_value = item[2]
        print(f"Price: ")
        print(f"Created: {item[3]}")
        print("-"*40)
    
    # Calculate total
    total_value = sum(float(item[2]) for item in items)
    print(f"\n📊 TOTAL: {len(items)} items | Total Value: ")
else:
    print("\nNo items found")

conn.close()
