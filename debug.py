import sqlite3

conn = sqlite3.connect('backend/crud_app.db')
cursor = conn.cursor()

# Get first row to examine structure
cursor.execute('SELECT * FROM items LIMIT 1')
sample = cursor.fetchone()

print("\n" + "="*60)
print("DEBUG INFORMATION")
print("="*60)

# Show column names
print("\nColumn names and their indexes:")
for idx, desc in enumerate(cursor.description):
    print(f"  Index {idx}: '{desc[0]}'")

# Show sample data
print(f"\nSample row data: {sample}")
print(f"Sample row length: {len(sample)}")

print("\nIndividual fields:")
for i in range(len(sample)):
    print(f"  Index {i}: {sample[i]} (type: {type(sample[i])})")

# Now show all data properly
print("\n" + "="*60)
print("ALL DATA")
print("="*60)

cursor.execute('SELECT * FROM items')
all_rows = cursor.fetchall()

for row in all_rows:
    print(f"\nID: {row[0]}")
    print(f"Name: {row[1]}")
    print(f"Price (raw): {row[3]}")
    print(f"Price (formatted): ")
    print(f"Created: {row[4]}")
    print("-"*40)

conn.close()
