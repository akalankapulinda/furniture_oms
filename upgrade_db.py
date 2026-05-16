import sqlite3

print("Starting database upgrade...")

conn = sqlite3.connect('furniture.db')
cursor = conn.cursor()

try:
    # Safely add the new column with an automatic timestamp
    cursor.execute("ALTER TABLE purchase_orders ADD COLUMN order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    print("✅ SUCCESS: Added 'order_date' column to purchase_orders!")
except sqlite3.OperationalError as e:
    # If you run this twice by accident, it will catch the error gracefully
    print(f"⚠️ Notice: {e} (The column might already exist!)")

conn.commit()
conn.close()