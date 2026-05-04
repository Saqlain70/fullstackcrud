import sqlite3

conn = sqlite3.connect('crud_app.db')
cursor = conn.cursor()

# Get all rows
cursor.execute('SELECT * FROM items')
rows = cursor.fetchall()

print("\n" + "="*60)
print("DATABASE CONTENTS")
print("="*60)

for row in rows:
    print(f"""
ID:          {row[0]}
Name:        {row[1]}
Description: {row[2] if row[2] else '(empty)'}
Price:       
Created:     {row[4]}
{'-'*60}""")

conn.close()
