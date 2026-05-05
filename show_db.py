import sqlite3

conn = sqlite3.connect('backend/crud_app.db')
cursor = conn.cursor()

print("\n" + "="*70)
print("YOUR CRUD APPLICATION DATABASE")
print("="*70)

cursor.execute("SELECT id, name, description, price, created_at FROM items ORDER BY id")
items = cursor.fetchall()

for item in items:
    print(f"""
┌─────────────────────────────────────────────────┐
│ ITEM #{item[0]}                                 │
├─────────────────────────────────────────────────┤
│ Name:        {item[1]}                              │
│ Description: {item[2] if item[2] else '(empty)'}      │
│ Price:                                 │
│ Created:     {item[4]}                      │
└─────────────────────────────────────────────────┘""")

# Summary
cursor.execute("SELECT COUNT(*), AVG(price), MIN(price), MAX(price), SUM(price) FROM items")
count, avg, min_p, max_p, total = cursor.fetchone()

print("\n" + "="*70)
print("📊 DATABASE SUMMARY")
print("="*70)
print(f"Total Items:     {count}")
print(f"Average Price:   ")
print(f"Minimum Price:   ")
print(f"Maximum Price:   ")
print(f"Total Value:     ")
print("="*70)

conn.close()
