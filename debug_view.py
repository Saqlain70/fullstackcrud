import sqlite3
import os

db_path = 'backend/crud_app.db'

print("=" * 70)
print("SQLITE DATABASE VIEWER (DEBUG VERSION)")
print("=" * 70)

if not os.path.exists(db_path):
    print(f"❌ Database not found")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get column info
cursor.execute("PRAGMA table_info(items)")
columns = cursor.fetchall()
print("\n📋 Table Structure:")
for col in columns:
    print(f"   Column: {col[1]}, Type: {col[2]}, Not Null: {col[3]}, Default: {col[4]}")

# Get all data with raw output
cursor.execute("SELECT * FROM items")
rows = cursor.fetchall()

print(f"\n📝 Raw Database Content ({len(rows)} items):")
print("-" * 70)

for i, row in enumerate(rows, 1):
    print(f"\nItem {i}:")
    print(f"  ID: {row[0]}")
    print(f"  Name: '{row[1]}'")
    print(f"  Description: '{row[2]}'")
    print(f"  Price RAW: {row[3]}")
    print(f"  Price Type: {type(row[3])}")
    print(f"  Created: {row[4]}")

# Try to display with proper formatting
print("\n" + "=" * 70)
print("📊 Formatted View:")
print("=" * 70)

cursor.execute("SELECT id, name, description, price, created_at FROM items")
items = cursor.fetchall()

print(f"\n{'ID':<5} {'Name':<20} {'Price':<12} {'Created At':<25}")
print("-" * 70)

for item in items:
    # Handle different price formats
    price_value = item[3]
    if price_value is None:
        price_display = "N/A"
    elif isinstance(price_value, (int, float)):
        price_display = f""
    else:
        price_display = f""
    
    print(f"{item[0]:<5} {item[1]:<20} {price_display:<12} {item[4][:19]:<25}")

conn.close()
print("\n" + "=" * 70)
