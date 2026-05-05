import sqlite3

conn = sqlite3.connect('backend/crud_app.db')
cursor = conn.cursor()

print("\nSQLite Query Tool (type 'exit' to quit)")
print("Example queries:")
print("  SELECT * FROM items;")
print("  SELECT name, price FROM items WHERE price > 10;")
print("=" * 50)

while True:
    query = input("\nSQL> ").strip()
    if query.lower() == 'exit':
        break
    if not query:
        continue
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            for row in results:
                print(row)
            print(f"\n{len(results)} row(s) returned")
        else:
            print("Query executed successfully (0 rows affected)")
            
        if query.upper().startswith('INSERT') or query.upper().startswith('UPDATE') or query.upper().startswith('DELETE'):
            conn.commit()
            print("Changes committed")
            
    except Exception as e:
        print(f"Error: {e}")

conn.close()
