import sqlite3

conn = sqlite3.connect('backend/crud_app.db')
cursor = conn.cursor()

print("\n" + "="*60)
print("DATABASE CONTENTS")
print("="*60)

# Use explicit column selection instead of SELECT *
cursor.execute("SELECT id, name, price, created_at FROM items")
items = cursor.fetchall()

for item in items:
    print(f"\nID: {item[0]}")
    print(f"Name: {item[1]}")
    print(f"Price: ")
    print(f"Created: {item[3]}")
    print("-"*40)

# Calculate total
total = sum(item[2] for item in items)
print(f"\n📊 TOTAL: {len(items)} items | Total Value: ")
print("="*60)

conn.close()
