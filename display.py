import sqlite3

conn = sqlite3.connect('backend/crud_app.db')
cursor = conn.cursor()

cursor.execute('SELECT id, name, price FROM items')
rows = cursor.fetchall()

print('\n' + '='*60)
print('ITEMS IN DATABASE')
print('='*60)

for row in rows:
    # Use string concatenation instead of f-strings
    output = 'ID: ' + str(row[0]) + ' | Name: ' + row[1] + ' | Price: $' + str(row[2])
    print(output)

print('='*60)
print('Total items: ' + str(len(rows)))
conn.close()
