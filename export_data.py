import sqlite3
import csv

conn = sqlite3.connect('backend/crud_app.db')
cursor = conn.cursor()

cursor.execute('SELECT id, name, description, price, created_at FROM items')
rows = cursor.fetchall()

with open('database_export.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Name', 'Description', 'Price', 'Created At'])
    writer.writerows(rows)

print("\n✅ Exported " + str(len(rows)) + " items to database_export.csv")
print("📁 File location: C:\\crud-fullstack-app\\database_export.csv")
print("\nYou can now open this file in Excel or any text editor to see your data.\n")

conn.close()
