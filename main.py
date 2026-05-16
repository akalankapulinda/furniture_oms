from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3
import json
from datetime import datetime, timedelta
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Furniture Shop OMS")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Define the data structure
class Item(BaseModel):
    item_id: int
    name: str
    category: str
    price: float
    stock_level: int

# Helper function to open a database connection
def get_db_connection():
    conn = sqlite3.connect('furniture.db')
    conn.row_factory = sqlite3.Row  # This lets us output the data cleanly as JSON later
    return conn

# ==========================================
# AUTHENTICATION HELPER (MOVED TO TOP)
# ==========================================
# 1. The Security Guard - Must be defined before the routes use it!
def check_login(request: Request):
    if request.cookies.get("session_token") != "authenticated_user":
        return False
    return True

# ==========================================
# AUTHENTICATION ROUTES
# ==========================================
# 2. Show the Login Page
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 3. Process the Password
@app.post("/login")
def process_login(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Give them the secure cookie and send them to the Home Page
        redirect = RedirectResponse(url="/", status_code=303)
        redirect.set_cookie(key="session_token", value="authenticated_user", httponly=True)
        return redirect
    else:
        # Send them back to the login page with an error
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})

# 4. Log Out
@app.get("/logout")
def logout():
    # Delete the cookie
    redirect = RedirectResponse(url="/login", status_code=303)
    redirect.delete_cookie("session_token")
    return redirect

# ==========================================
# CORE PAGES
# ==========================================

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)
        
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Total Inventory Value (Stock Level * Price for all items)
    cursor.execute("SELECT SUM(stock_level * price) as total_value FROM items")
    inventory_value = cursor.fetchone()['total_value'] or 0

    # 2. Total Revenue (This Month)
    cursor.execute('''
        SELECT SUM(s.quantity * i.price) as monthly_revenue 
        FROM sales s 
        JOIN items i ON s.item_id = i.item_id 
        WHERE strftime('%Y-%m', s.sale_date) = strftime('%Y-%m', 'now', 'localtime')
    ''')
    monthly_revenue = cursor.fetchone()['monthly_revenue'] or 0

    # 3. Total Spend (This Month) 
    # Note: Using the selling price for the prototype.
    cursor.execute('''
        SELECT SUM(po.quantity * i.price) as monthly_spend 
        FROM purchase_orders po 
        JOIN items i ON po.item_id = i.item_id 
        WHERE strftime('%Y-%m', po.order_date) = strftime('%Y-%m', 'now', 'localtime')
    ''')
    monthly_spend = cursor.fetchone()['monthly_spend'] or 0

    # 4. Total Items Sold (This Month)
    cursor.execute('''
        SELECT SUM(quantity) as items_sold 
        FROM sales 
        WHERE strftime('%Y-%m', sale_date) = strftime('%Y-%m', 'now', 'localtime')
    ''')
    items_sold = cursor.fetchone()['items_sold'] or 0

    conn.close()
        
    return templates.TemplateResponse("index.html", {
        "request": request,
        "inventory_value": inventory_value,
        "monthly_revenue": monthly_revenue,
        "monthly_spend": monthly_spend,
        "items_sold": items_sold
    })

# Route to display the Inventory Web Page
# Route to display the Inventory Web Page
@app.get("/inventory", response_class=HTMLResponse)
def view_inventory(request: Request, search: str = None):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Send the list of suppliers to the HTML so they appear in the dropdown menu
    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()
    
    # ENHANCED SEARCH: Now checks Item Name, Category, OR Supplier Company Name!
    if search:
        search_term = f"%{search}%"
        cursor.execute('''
            SELECT i.*, s.company_name 
            FROM items i 
            LEFT JOIN suppliers s ON i.supplier_id = s.supplier_id 
            WHERE i.name LIKE ? 
               OR i.category LIKE ? 
               OR s.company_name LIKE ?
        ''', (search_term, search_term, search_term))
    else:
        cursor.execute('''
            SELECT i.*, s.company_name 
            FROM items i 
            LEFT JOIN suppliers s ON i.supplier_id = s.supplier_id
        ''')
        
    items = cursor.fetchall()
    conn.close()
    
    return templates.TemplateResponse("inventory.html", {"request": request, "items": items, "suppliers": suppliers, "search": search})

# Route to handle the HTML Form submission
@app.post("/add_item_form")
def add_item_from_web(
    request: Request,
    name: str = Form(...), 
    category: str = Form(...), 
    price: float = Form(...), 
    stock_level: int = Form(...),
    supplier_id: int = Form(...)
):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, category, price, stock_level, supplier_id) VALUES (?, ?, ?, ?, ?)",
        (name, category, price, stock_level, supplier_id)
    )
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/inventory", status_code=303)


# ==========================================
# SUPPLIER ROUTES
# ==========================================

@app.get("/suppliers", response_class=HTMLResponse)
def view_suppliers(request: Request):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()
    conn.close()
    
    return templates.TemplateResponse("suppliers.html", {"request": request, "suppliers": suppliers})

@app.post("/add_supplier_form")
def add_supplier_from_web(
    request: Request,
    company_name: str = Form(...), 
    contact_person: str = Form(...), 
    phone: str = Form(...), 
    email: str = Form(None)
):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO suppliers (company_name, contact_person, phone, email) VALUES (?, ?, ?, ?)",
        (company_name, contact_person, phone, email)
    )
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/suppliers", status_code=303)

# ==========================================
# PURCHASE ORDER ROUTES
# ==========================================

@app.get("/purchase_orders", response_class=HTMLResponse)
def view_purchase_orders(request: Request, search: str = None, item_id: int = None):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()
    
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    
    # ENHANCED SEARCH: Check Supplier, Item Name, Status, OR Date
    if search:
        search_term = f"%{search}%"
        cursor.execute('''
            SELECT po.po_id, s.company_name, i.name as item_name, po.quantity, po.status, po.order_date 
            FROM purchase_orders po
            JOIN suppliers s ON po.supplier_id = s.supplier_id
            JOIN items i ON po.item_id = i.item_id
            WHERE s.company_name LIKE ? 
               OR i.name LIKE ? 
               OR po.order_date LIKE ?
               OR po.status LIKE ?
            ORDER BY po.po_id DESC
        ''', (search_term, search_term, search_term, search_term))
    else:
        cursor.execute('''
            SELECT po.po_id, s.company_name, i.name as item_name, po.quantity, po.status, po.order_date 
            FROM purchase_orders po
            JOIN suppliers s ON po.supplier_id = s.supplier_id
            JOIN items i ON po.item_id = i.item_id
            ORDER BY po.po_id DESC
        ''')
        
    purchase_orders = cursor.fetchall()
    
    # Logic to auto-select supplier and item if arriving from the Inventory page
    selected_item_id = item_id
    selected_supplier_id = None
    
    if selected_item_id:
        cursor.execute("SELECT supplier_id FROM items WHERE item_id = ?", (selected_item_id,))
        result = cursor.fetchone()
        if result:
            selected_supplier_id = result['supplier_id']
            
    conn.close()
    
    return templates.TemplateResponse(
        "purchase_orders.html", 
        {
            "request": request, 
            "suppliers": suppliers, 
            "items": items, 
            "purchase_orders": purchase_orders,
            "search": search,
            "selected_item_id": selected_item_id,
            "selected_supplier_id": selected_supplier_id
        }
    )
    

@app.post("/add_po_form")
def add_po_from_web(
    request: Request,
    supplier_id: int = Form(...), 
    item_id: int = Form(...), 
    quantity: int = Form(...)
):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO purchase_orders (supplier_id, item_id, quantity) VALUES (?, ?, ?)",
        (supplier_id, item_id, quantity)
    )
    
    cursor.execute(
        "UPDATE items SET stock_level = stock_level + ? WHERE item_id = ?",
        (quantity, item_id)
    )
    
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/purchase_orders", status_code=303)

# ==========================================
# SALES / OUTBOUND ROUTES
# ==========================================

@app.get("/sales", response_class=HTMLResponse)
def view_sales(request: Request, search: str = None, item_id: int = None):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get items for the dropdown menu
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    
    # ENHANCED SEARCH: Check Customer Name, Item Name, OR the Date/Time
    if search:
        search_term = f"%{search}%"
        cursor.execute('''
            SELECT s.sale_id, s.customer_name, i.name as item_name, s.quantity, s.sale_date 
            FROM sales s
            JOIN items i ON s.item_id = i.item_id
            WHERE s.customer_name LIKE ? 
               OR i.name LIKE ? 
               OR s.sale_date LIKE ?
            ORDER BY s.sale_id DESC
        ''', (search_term, search_term, search_term))
    else:
        cursor.execute('''
            SELECT s.sale_id, s.customer_name, i.name as item_name, s.quantity, s.sale_date 
            FROM sales s
            JOIN items i ON s.item_id = i.item_id
            ORDER BY s.sale_id DESC
        ''')
        
    sales = cursor.fetchall()
    conn.close()
    
    return templates.TemplateResponse(
        "sales.html", 
        {
            "request": request, 
            "items": items, 
            "sales": sales,
            "search": search,
            "selected_item_id": item_id
        }
    )

@app.post("/add_sale_form")
def add_sale_from_web(
    request: Request,
    customer_name: str = Form(...), 
    item_id: int = Form(...), 
    quantity: int = Form(...)
):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO sales (customer_name, item_id, quantity) VALUES (?, ?, ?)",
        (customer_name, item_id, quantity)
    )
    
    cursor.execute(
        "UPDATE items SET stock_level = stock_level - ? WHERE item_id = ?",
        (quantity, item_id)
    )
    
    conn.commit()
    conn.close()
    
    return RedirectResponse(url="/sales", status_code=303)

# ==========================================
# EDIT & UPDATE ROUTES
# ==========================================

@app.get("/edit_item/{item_id}", response_class=HTMLResponse)
def edit_item_page(request: Request, item_id: int):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE item_id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    return templates.TemplateResponse("edit_item.html", {"request": request, "item": item})

@app.post("/update_item/{item_id}")
def update_item_in_db(
    request: Request,
    item_id: int,
    name: str = Form(...), 
    category: str = Form(...), 
    price: float = Form(...), 
    stock_level: int = Form(...)
):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE items 
        SET name = ?, category = ?, price = ?, stock_level = ? 
        WHERE item_id = ?
    ''', (name, category, price, stock_level, item_id))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/inventory", status_code=303)

@app.get("/edit_supplier/{supplier_id}", response_class=HTMLResponse)
def edit_supplier_page(request: Request, supplier_id: int):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM suppliers WHERE supplier_id = ?", (supplier_id,))
    supplier = cursor.fetchone()
    conn.close()
    return templates.TemplateResponse("edit_supplier.html", {"request": request, "supplier": supplier})

@app.post("/update_supplier/{supplier_id}")
def update_supplier_in_db(
    request: Request,
    supplier_id: int,
    company_name: str = Form(...), 
    contact_person: str = Form(...), 
    phone: str = Form(...), 
    email: str = Form(None)
):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE suppliers 
        SET company_name = ?, contact_person = ?, phone = ?, email = ? 
        WHERE supplier_id = ?
    ''', (company_name, contact_person, phone, email, supplier_id))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/suppliers", status_code=303)

# ==========================================
# DELETE ROUTES
# ==========================================

@app.get("/delete_item/{item_id}")
def delete_item(request: Request, item_id: int):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/inventory", status_code=303)

@app.get("/delete_supplier/{supplier_id}")
def delete_supplier(request: Request, supplier_id: int):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM suppliers WHERE supplier_id = ?", (supplier_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/suppliers", status_code=303)

@app.get("/delete_po/{po_id}")
def delete_po(request: Request, po_id: int):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT item_id, quantity FROM purchase_orders WHERE po_id = ?", (po_id,))
    po = cursor.fetchone()
    
    if po:
        cursor.execute("UPDATE items SET stock_level = stock_level - ? WHERE item_id = ?", (po['quantity'], po['item_id']))
        cursor.execute("DELETE FROM purchase_orders WHERE po_id = ?", (po_id,))
        
    conn.commit()
    conn.close()
    return RedirectResponse(url="/purchase_orders", status_code=303)

@app.get("/delete_sale/{sale_id}")
def delete_sale(request: Request, sale_id: int):
    if not check_login(request):
        return RedirectResponse(url="/login", status_code=303)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT item_id, quantity FROM sales WHERE sale_id = ?", (sale_id,))
    sale = cursor.fetchone()
    
    if sale:
        cursor.execute("UPDATE items SET stock_level = stock_level + ? WHERE item_id = ?", (sale['quantity'], sale['item_id']))
        cursor.execute("DELETE FROM sales WHERE sale_id = ?", (sale_id,))
        
    conn.commit()
    conn.close()
    return RedirectResponse(url="/sales", status_code=303)

# ==========================================
# API ENDPOINTS (Optional but protected)
# ==========================================

@app.post("/items/")
def add_item(item: Item):
    # Pure API route left mostly for testing purposes
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (item_id, name, category, price, stock_level) VALUES (?, ?, ?, ?, ?)",
        (item.item_id, item.name, item.category, item.price, item.stock_level)
    )
    conn.commit()
    conn.close()
    return {"status": "Success", "message": f"{item.name} permanently saved to database!"}

@app.get("/items/")
def get_all_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return {"inventory": items}