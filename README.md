# 🛋️ Furniture Order Management System (OMS)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-Database-07405E?style=for-the-badge&logo=sqlite)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange?style=for-the-badge)

</div>

---

# 📌 Overview

The **Furniture Order Management System (OMS)** is a modern full-stack inventory and order processing platform developed for retail furniture businesses.  
It provides centralized management for:

- 📦 Inventory & stock control
- 🧾 Purchase orders
- 🛒 Customer sales
- 📊 Financial analytics
- 📈 Business reporting

Built using **FastAPI**, **SQLite**, and **Bootstrap 5**, the system delivers high performance with a clean and responsive interface.

---

# ✨ Key Features

## 🔐 Authentication & Security
- Secure staff login system
- Cookie-based session authentication
- Protected admin routes
- User session management

---

## 📊 Executive Dashboard
- Real-time KPI monitoring
- Monthly revenue tracking
- Monthly expenditure tracking
- Inventory asset valuation
- Business performance indicators

---

## 📈 Analytics & Visualization
- Interactive charts powered by Chart.js
- 30-day revenue vs expense cashflow graph
- Top-selling product analytics
- Inventory movement trends

---

## 📦 Inventory Management
- Add, update, and remove inventory items
- Real-time stock availability
- Automatic stock deductions after sales
- Automatic stock increments after purchases
- Low-stock monitoring

---

## 🧾 Purchase Order Management
- Supplier tracking
- Purchase order history
- Purchase cost management
- Inbound inventory handling

---

## 🛒 Sales Management
- Customer order processing
- Invoice generation support
- Sales history tracking
- Profit calculation

---

## 🔍 Smart Search & Filtering
Search records dynamically by:
- Product name
- Supplier
- Category
- Date
- Order ID
- Customer

---

# 🖼️ System Preview

## 🔒Athentication
<img width="1920" height="1080" alt="Screenshot (167)" src="https://github.com/user-attachments/assets/afd855ea-4eba-4e67-afd8-0ad6f52b6763" />

## 📊 Dashboard
<img width="1920" height="1080" alt="Screenshot (168)" src="https://github.com/user-attachments/assets/80d5edae-f1f9-4111-ab9b-79b59d45715b" />

## 📦 Inventory Module
<img width="1920" height="1080" alt="Screenshot (169)" src="https://github.com/user-attachments/assets/fea0c431-e63c-435b-bc3e-8f2a426fff38" />

## 🛒 Sales Module
<img width="1920" height="1080" alt="Screenshot (170)" src="https://github.com/user-attachments/assets/77c7d7a9-6ee5-47cc-b057-3c49098ae6a5" />

## 📦 Purches Module
<img width="1920" height="1080" alt="Screenshot (171)" src="https://github.com/user-attachments/assets/a6d67d21-fe0a-4e0f-a193-672945ac1318" />

## 🏢 Supplier Module
<img width="1920" height="1080" alt="Screenshot (172)" src="https://github.com/user-attachments/assets/404e6e7f-91a2-4314-bd03-2011b37a443f" />

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3 |
| API Framework | FastAPI |
| ASGI Server | Uvicorn |
| Frontend | HTML5, Bootstrap 5 |
| Templates | Jinja2 |
| Charts | Chart.js |
| Database | SQLite3 |
| ORM/DB Access | SQLite Native Queries |
| Authentication | Cookie Sessions |

---

# 📂 Project Structure

```bash
furniture-oms/
│
├── static/                # CSS, JS, Images
├── templates/             # Jinja2 HTML Templates
├── database/              # SQLite database files
├── exports/               # Generated reports
├── main.py                # FastAPI application
├── fix_db.py              # Database initialization script
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/furniture-oms.git
cd furniture-oms
```

---

## 2️⃣ Create Virtual Environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a requirements file:

```bash
pip install fastapi uvicorn jinja2 python-multipart
```

---

## 4️⃣ Initialize the Database

```bash
python fix_db.py
```

This will:
- Create required tables
- Configure foreign keys
- Generate the default admin account

---

## 5️⃣ Run the Server

```bash
uvicorn main:app --reload
```

---

# 🌐 Access the Application

Open your browser:

```text
http://127.0.0.1:8000
```

---

# 🔑 Default Login Credentials

| Role | Username | Password |
|---|---|---|
| Administrator | admin | admin123 |

> ⚠️ Change the default password after first login.

---

# 📊 Database Design

The system uses a relational SQLite database with:
- Foreign key relationships
- Normalized table structures
- Transaction-safe inventory updates

### Core Tables
- users
- inventory
- suppliers
- purchase_orders
- sales_orders
- order_items

---

# 🔄 Inventory Workflow

```text
Supplier → Purchase Order → Inventory Stock ↑
Customer → Sales Order → Inventory Stock ↓
```

---

# 📈 Reporting Capabilities

The OMS provides:
- Revenue reports
- Expense reports
- Profit analysis
- Inventory valuation
- Product performance analytics
- Exportable Excel/CSV statements

---

# 🚀 Future Improvements

- JWT authentication
- REST API endpoints
- Docker deployment
- PostgreSQL support
- Multi-user roles & permissions
- Email notifications
- Barcode scanner integration
- AI-powered sales forecasting
- Cloud deployment support

---

# 🧪 Example API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Dashboard |
| GET | `/inventory` | View inventory |
| POST | `/inventory/add` | Add item |
| GET | `/sales` | Sales records |
| POST | `/sales/create` | Create sale |
| GET | `/reports/export` | Export reports |

---

# 🛡️ Security Features

- Cookie-based authentication
- Route protection
- Form validation
- Secure session handling
- SQL foreign key integrity

---

# 🤝 Contributing

Contributions are welcome!

## Steps
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to your branch
5. Open a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

### YOUR NAME
Full Stack Developer

- GitHub: https://github.com/akalankapulinda
- LinkedIn: https://linkedin.com/in/007akalankapulinda

---

# ⭐ Support

If you like this project:

- ⭐ Star the repository
- 🍴 Fork the project
- 🐛 Report issues
- 💡 Suggest features

---

<div align="center">

### 🚀 Built with FastAPI & Passion for Business Automation

</div>
