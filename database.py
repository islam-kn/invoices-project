import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_name="invoiciz.db"):
        self.db_name = db_name
        self.conn = None

    @contextmanager
    def get_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            yield self.conn
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None

    def execute_query(self, query, params=()):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()

    def create_tables(self):
        with self.get_connection() as conn:
            # Drop existing invoices table if it exists
            conn.execute("DROP TABLE IF EXISTS invoice_items")
            conn.execute("DROP TABLE IF EXISTS invoices")
            
            # Recreate invoices table with type column
            conn.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_id INTEGER,
                    customer_id INTEGER,
                    date TEXT NOT NULL,
                    total REAL NOT NULL,
                    type TEXT NOT NULL DEFAULT 'Bon de commande',
                    FOREIGN KEY (owner_id) REFERENCES owner(id),
                    FOREIGN KEY (customer_id) REFERENCES customers(id)
                )
            """)
            
            # Recreate invoice_items table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS invoice_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER,
                    price REAL,
                    FOREIGN KEY (invoice_id) REFERENCES invoices(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS owner (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    phone TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    phone TEXT NOT NULL
                )
            """)

    def add_owner(self, name, address, phone):
        return self.execute_query(
            "INSERT INTO owner (name, address, phone) VALUES (?, ?, ?)",
            (name, address, phone)
        )

    def get_owners(self):
        return self.execute_query("SELECT * FROM owner")

    def update_owner(self, owner_id, name, address, phone):
        return self.execute_query(
            "UPDATE owner SET name = ?, address = ?, phone = ? WHERE id = ?",
            (name, address, phone, owner_id)
        )

    def delete_owner(self, owner_id):
        return self.execute_query("DELETE FROM owner WHERE id = ?", (owner_id,))

    def add_invoice(self, owner_id, customer_id, date, total, invoice_type):
        cursor = self.execute_query(
            """INSERT INTO invoices 
               (owner_id, customer_id, date, total, type) 
               VALUES (?, ?, ?, ?, ?)
               RETURNING id""",
            (owner_id, customer_id, date, total, invoice_type)
        )
        return cursor[0][0] if cursor else None

    def get_invoices(self):
        return self.execute_query("SELECT * FROM invoices")

    def update_invoice(self, invoice_id, owner_id, customer_id, date, total, invoice_type):
        return self.execute_query(
            """UPDATE invoices 
               SET owner_id = ?, customer_id = ?, date = ?, total = ?, type = ? 
               WHERE id = ?""",
            (owner_id, customer_id, date, total, invoice_type, invoice_id)
        )

    def delete_invoice(self, invoice_id):
        return self.execute_query("DELETE FROM invoices WHERE id = ?", (invoice_id,))

    def add_product(self, name, description, price):
        return self.execute_query(
            "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
            (name, description, price)
        )

    def get_products(self):
        return self.execute_query("SELECT * FROM products")

    def update_product(self, product_id, name, description, price):
        return self.execute_query(
            "UPDATE products SET name = ?, description = ?, price = ? WHERE id = ?",
            (name, description, price, product_id)
        )

    def delete_product(self, product_id):
        return self.execute_query("DELETE FROM products WHERE id = ?", (product_id,))

    def add_customer(self, name, address, phone):
        return self.execute_query(
            "INSERT INTO customers (name, address, phone) VALUES (?, ?, ?)",
            (name, address, phone)
        )

    def get_customers(self):
        return self.execute_query("SELECT * FROM customers")

    def update_customer(self, customer_id, name, address, phone):
        return self.execute_query(
            "UPDATE customers SET name = ?, address = ?, phone = ? WHERE id = ?",
            (name, address, phone, customer_id)
        )

    def delete_customer(self, customer_id):
        return self.execute_query("DELETE FROM customers WHERE id = ?", (customer_id,))

    def add_invoice_item(self, invoice_id, product_id, quantity, price):
        return self.execute_query(
            """INSERT INTO invoice_items 
               (invoice_id, product_id, quantity, price) 
               VALUES (?, ?, ?, ?)""",
            (invoice_id, product_id, quantity, price)
        )

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None


db = Database()
db.create_tables()

