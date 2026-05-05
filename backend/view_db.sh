#!/bin/bash
cd /workspaces/fullstackcrud/crud-fullstack-app/backend
python3 << PYTHON
import sqlite3
conn = sqlite3.connect('crud_app.db')
cursor = conn.cursor()
cursor.execute("SELECT id, name, price, created_at FROM items ORDER BY id")
rows = cursor.fetchall()
print("\n" + "="*60)
print("ID | Name | Price | Created")
print("="*60)
for row in rows:
    price = float(row[2])
    print(f"{row[0]} | {row[1]} | ${price:.2f} | {row[3][:19]}")
print("="*60)
print(f"Total Items: {len(rows)}")
conn.close()
PYTHON
