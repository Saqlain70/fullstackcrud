import sqlite3
import sys
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    db_path = 'backend/crud_app.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    while True:
        print("\n" + "=" * 60)
        print("🗄️  DATABASE MANAGEMENT SYSTEM")
        print("=" * 60)
        print("1. 📖 View all items")
        print("2. ➕ Add new item")
        print("3. ✏️ Update item")
        print("4. 🗑️ Delete item")
        print("5. 🧹 Delete all items")
        print("6. 📊 View statistics")
        print("7. 💾 Export to CSV")
        print("8. 🔍 Search items")
        print("0. 🚪 Exit")
        print("=" * 60)
        
        choice = input("\n👉 Choose option: ").strip()
        
        if choice == '1':
            cursor.execute("SELECT id, name, price, created_at FROM items ORDER BY id")
            rows = cursor.fetchall()
            if rows:
                print("\n📋 ALL ITEMS:")
                print("-" * 60)
                for row in rows:
                    print(f"ID: {row[0]} | {row[1]} |  | {row[3][:19]}")
            else:
                print("\n📭 No items in database")
        
        elif choice == '2':
            print("\n➕ ADD NEW ITEM")
            name = input("Item name: ").strip()
            if not name:
                print("❌ Name cannot be empty")
                continue
            
            try:
                price = float(input("Price: "))
            except ValueError:
                print("❌ Invalid price")
                continue
            
            desc = input("Description (optional): ").strip()
            
            cursor.execute(
                "INSERT INTO items (name, description, price, created_at) VALUES (?, ?, ?, datetime('now'))",
                (name, desc, price)
            )
            conn.commit()
            print(f"✅ Item '{name}' added successfully!")
        
        elif choice == '3':
            cursor.execute("SELECT id, name, price FROM items")
            items = cursor.fetchall()
            if not items:
                print("\n📭 No items to update")
                continue
            
            print("\n✏️ UPDATE ITEM")
            print("Available items:")
            for item in items:
                print(f"  [{item[0]}] {item[1]} - ")
            
            try:
                item_id = int(input("\nEnter item ID to update: "))
            except ValueError:
                print("❌ Invalid ID")
                continue
            
            cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
            item = cursor.fetchone()
            if not item:
                print("❌ Item not found")
                continue
            
            print(f"\nCurrent values: {item[1]} - ")
            new_name = input(f"New name (press Enter to keep '{item[1]}'): ").strip()
            new_price = input(f"New price (press Enter to keep ): ").strip()
            
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
                print("✅ Item updated successfully!")
            else:
                print("ℹ️ No changes made")
        
        elif choice == '4':
            cursor.execute("SELECT id, name FROM items")
            items = cursor.fetchall()
            if not items:
                print("\n📭 No items to delete")
                continue
            
            print("\n🗑️ DELETE ITEM")
            for item in items:
                print(f"  [{item[0]}] {item[1]}")
            
            try:
                item_id = int(input("\nEnter item ID to delete: "))
            except ValueError:
                print("❌ Invalid ID")
                continue
            
            confirm = input(f"Are you sure you want to delete item {item_id}? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
                conn.commit()
                print(f"✅ Item {item_id} deleted successfully!")
            else:
                print("❌ Deletion cancelled")
        
        elif choice == '5':
            confirm = input("\n⚠️  WARNING: Delete ALL items? Type 'DELETE ALL' to confirm: ")
            if confirm == 'DELETE ALL':
                cursor.execute("DELETE FROM items")
                conn.commit()
                print("✅ All items deleted!")
            else:
                print("❌ Deletion cancelled")
        
        elif choice == '6':
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
            
            print("\n📊 DATABASE STATISTICS")
            print("-" * 40)
            print(f"Total items: {stats[0]}")
            print(f"Average price: " if stats[1] else "Average price: N/A")
            print(f"Minimum price: " if stats[2] else "Minimum price: N/A")
            print(f"Maximum price: " if stats[3] else "Maximum price: N/A")
            print(f"Total value: " if stats[4] else "Total value: N/A")
        
        elif choice == '7':
            import csv
            cursor.execute("SELECT * FROM items")
            rows = cursor.fetchall()
            
            if rows:
                with open('database_export.csv', 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['ID', 'Name', 'Description', 'Price', 'Created At'])
                    writer.writerows(rows)
                print(f"✅ Exported {len(rows)} items to database_export.csv")
            else:
                print("📭 No items to export")
        
        elif choice == '8':
            search_term = input("\n🔍 Enter search term: ").strip()
            cursor.execute(
                "SELECT id, name, price, created_at FROM items WHERE name LIKE ? OR description LIKE ?",
                (f'%{search_term}%', f'%{search_term}%')
            )
            results = cursor.fetchall()
            
            if results:
                print(f"\nFound {len(results)} item(s):")
                for row in results:
                    print(f"  [{row[0]}] {row[1]} -  ({row[3][:19]})")
            else:
                print("📭 No matching items found")
        
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option")
    
    conn.close()

if __name__ == "__main__":
    main()
