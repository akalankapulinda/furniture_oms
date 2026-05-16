import sqlite3

def reset_entire_database():
    conn = sqlite3.connect('furniture.db')
    cursor = conn.cursor()

    print("Starting full database wipe...")

    # 1. Delete all data from ALL tables
    cursor.execute("DELETE FROM sales")
    cursor.execute("DELETE FROM purchase_orders")
    cursor.execute("DELETE FROM items")
    cursor.execute("DELETE FROM suppliers")

    # 2. Reset ALL auto-increment ID counters back to 0
    # By deleting everything in sqlite_sequence, every table's ID will start at 1 again!
    cursor.execute("DELETE FROM sqlite_sequence")

    conn.commit()
    conn.close()

    print("--------------------------------------------------")
    print("✅ SUCCESS: Entire database completely wiped clean!")
    print("✅ All Items, Suppliers, POs, and Sales have been deleted.")
    print("✅ All ID numbers have been reset and will start at #1.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    # Ask for confirmation just to be safe!
    confirm = input("⚠️ WARNING: This will delete EVERYTHING in your system. Type 'YES' to continue: ")
    if confirm == 'YES':
        reset_entire_database()
    else:
        print("Database wipe cancelled.")