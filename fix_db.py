import os
import sqlite3

print("Starting database forced upgrade...")

# 1. Destroy the old database
try:
    if os.path.exists('furniture.db'):
        os.remove('furniture.db')
        print("✅ Old database successfully deleted!")
    else:
        print("✅ No old database found. Ready to build.")
except PermissionError:
    print("❌ ERROR: Windows says the file is locked! You MUST stop Uvicorn (press Ctrl+C in the terminal) before running this script.")
    exit()

# 2. Build the brand new database
conn = sqlite3.connect('furniture.db')
cursor = conn.cursor()

# Users Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")

# Suppliers Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    contact_person TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT
)
''')

# Items Table (NOW WITH supplier_id!)
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock_level INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id)
)
''')

# Purchase Orders Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS purchase_orders (
    po_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    status TEXT DEFAULT 'Received',
    FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id),
    FOREIGN KEY (item_id) REFERENCES items (item_id)
)
''')

# Sales Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items (item_id)
)
''')

conn.commit()
conn.close()
print("✅ SUCCESS: Database rebuilt with the new supplier_id column!")