import sqlite3
import os

# Get the correct database path
db_path = os.path.join('backend', 'crud_app.db')

if not os.path.exists(db_path):
    print("❌ Database not found at:", db_path)
    print("Make sure you're in the crud-fullstack-app directory")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('SELECT id, name, price FROM items')
rows = cursor.fetchall()

print("\n" + "="*60)
print("ITEMS IN DATABASE")
print("="*60)

for row in rows:
    print("ID:", row[0], "| Name:", row[1], "| Price: $", row[2])

print("="*60)
print("Total items:", len(rows))
conn.close()
