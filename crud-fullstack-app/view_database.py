import sqlite3
import os

db_path = 'backend/crud_app.db'

print("=" * 70)
print("SQLITE DATABASE VIEWER")
print("=" * 70)

if not os.path.exists(db_path):
    print(f"❌ Database not found at: {db_path}")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("\n📋 Tables in database:", [t[0] for t in tables])

# Show items table schema
cursor.execute("PRAGMA table_info(items);")
columns = cursor.fetchall()
print("\n📊 Items table structure:")
for col in columns:
    print(f"   • {col[1]} ({col[2]})")

# Show all data
cursor.execute("SELECT * FROM items")
rows = cursor.fetchall()

print(f"\n📝 All items (Total: {len(rows)}):")
print("-" * 70)
if rows:
    for row in rows:
        # FIXED: Added price display
        print(f"ID: {row[0]} | Name: {row[1]} | Price:  | Created: {row[4]}")
        if row[2]:
            print(f"    Description: {row[2]}")
        print("-" * 70)
else:
    print("No items found in database")

conn.close()
print("\n✅ Done!")
