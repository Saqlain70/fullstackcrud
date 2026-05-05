import sqlite3
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def view_items(cursor):
    cursor.execute("SELECT id, name, price, created_at FROM items ORDER BY id")
    items = cursor.fetchall()
    
    if items:
        print("\n" + "=" * 70)
        print(f"{'ID':<5} {'Name':<25} {'Price':<12} {'Created At':<25}")
        print("-" * 70)
        for item in items:
            print(f"{item[0]:<5} {item[1]:<25}  {item[3][:19]}")
        print("=" * 70)
    else:
        print("\n📭 No items found")
    
    return len(items)

def add_item(conn, cursor):
    print("\n" + "=" * 50)
    print("➕ ADD NEW ITEM")
    print("=" * 50)
    
    name = input("Item name: ").strip()
    if not name:
        print("❌ Name required")
        return
    
    try:
        price = float(input("Price: $"))
    except ValueError:
        print("❌ Invalid price")
        return
    
    desc = input("Description (optional): ").strip()
    
    from datetime import datetime
    cursor.execute(
        "INSERT INTO items (name, description, price, created_at) VALUES (?, ?, ?, ?)",
        (name, desc, price, datetime.now().isoformat())
    )
    conn.commit()
    print(f"\n✅ '{name}' added successfully!")

def update_item(conn, cursor):
    print("\n" + "=" * 50)
    print("✏️ UPDATE ITEM")
    print("=" * 50)
    
    # Show existing items
    cursor.execute("SELECT id, name, price FROM items")
    items = cursor.fetchall()
    
    if not items:
        print("📭 No items to update")
        return
    
    print("\nExisting items:")
    for item in items:
        print(f"  [{item[0]}] {item[1]} - ")
    
    try:
        item_id = int(input("\nEnter item ID to update: "))
    except ValueError:
        print("❌ Invalid ID")
        return
    
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    
    if not item:
        print("❌ Item not found")
        return
    
    print(f"\nCurrent: {item[1]} - ")
    new_name = input(f"New name (Enter to keep '{item[1]}'): ").strip()
    new_price = input(f"New price (Enter to keep ): ").strip()
    
    updates = []
    values = []
    
    if new_name:
        updates.append("name = ?")
        values.append(new_name)
    if new_price:
        try:
            values.append(float(new_price))
            updates.append("price = ?")
        except ValueError:
            print("❌ Invalid price, keeping original")
    
    if updates:
        values.append(item_id)
        cursor.execute(f"UPDATE items SET {', '.join(updates)} WHERE id = ?", values)
        conn.commit()
        print("\n✅ Item updated!")
    else:
        print("\nℹ️ No changes made")

def delete_item(conn, cursor):
    print("\n" + "=" * 50)
    print("🗑️ DELETE ITEM")
    print("=" * 50)
    
    cursor.execute("SELECT id, name, price FROM items")
    items = cursor.fetchall()
    
    if not items:
        print("📭 No items to delete")
        return
    
    print("\nExisting items:")
    for item in items:
        print(f"  [{item[0]}] {item[1]} - ")
    
    try:
        item_id = int(input("\nEnter item ID to delete: "))
    except ValueError:
        print("❌ Invalid ID")
        return
    
    confirm = input(f"Delete item {item_id}? (yes/no): ")
    if confirm.lower() == 'yes':
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        print("\n✅ Item deleted!")
    else:
        print("\n❌ Cancelled")

def show_stats(cursor):
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            AVG(price) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price,
            SUM(price) as total_value
        FROM items
    """)
    stats = cursor.fetchone()
    
    print("\n" + "=" * 50)
    print("📊 DATABASE STATISTICS")
    print("=" * 50)
    print(f"Total Items:     {stats[0]}")
    print(f"Average Price:   ")
    print(f"Minimum Price:   ")
    print(f"Maximum Price:   ")
    print(f"Total Value:     ")
    print("=" * 50)

def search_items(cursor):
    print("\n" + "=" * 50)
    print("🔍 SEARCH ITEMS")
    print("=" * 50)
    
    search = input("Enter search term: ").strip()
    if not search:
        return
    
    cursor.execute(
        "SELECT id, name, price, created_at FROM items WHERE name LIKE ? OR description LIKE ?",
        (f'%{search}%', f'%{search}%')
    )
    results = cursor.fetchall()
    
    if results:
        print(f"\nFound {len(results)} item(s):")
        print("-" * 70)
        for item in results:
            print(f"  [{item[0]}] {item[1]} -  ({item[3][:19]})")
    else:
        print("\n📭 No matching items")

def main():
    try:
        conn = sqlite3.connect('backend/crud_app.db')
        cursor = conn.cursor()
        
        while True:
            print("\n" + "=" * 50)
            print("🗄️  DATABASE MANAGEMENT SYSTEM")
            print("=" * 50)
            print("1. 📖 View all items")
            print("2. ➕ Add new item")
            print("3. ✏️ Update item")
            print("4. 🗑️ Delete item")
            print("5. 📊 View statistics")
            print("6. 🔍 Search items")
            print("0. 🚪 Exit")
            print("=" * 50)
            
            choice = input("\nChoose option: ").strip()
            
            if choice == '1':
                view_items(cursor)
            elif choice == '2':
                add_item(conn, cursor)
            elif choice == '3':
                update_item(conn, cursor)
            elif choice == '4':
                delete_item(conn, cursor)
            elif choice == '5':
                show_stats(cursor)
            elif choice == '6':
                search_items(cursor)
            elif choice == '0':
                print("\n👋 Goodbye!")
                break
            else:
                print("\n❌ Invalid option")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
