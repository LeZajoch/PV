# customer.py
import datetime
from .db import get_db_connection

class Customer:
    """Příklad Active Record / Row Gateway pro tabulku Customers."""
    def __init__(self, customer_id=None, first_name=None, last_name=None, email=None,
                 is_active=True, date_registered=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_active = is_active
        self.date_registered = date_registered or datetime.datetime.now()

    def save(self):
        """Uloží objekt do DB (INSERT nebo UPDATE podle ID)."""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            if self.customer_id is None:
                # INSERT
                sql = """
                INSERT INTO Customers (first_name, last_name, email, is_active, date_registered)
                VALUES (?, ?, ?, ?, ?)
                """
                params = (self.first_name, self.last_name, self.email, self.is_active, self.date_registered)
                cursor.execute(sql, params)
                conn.commit()
                # Získáme ID
                cursor.execute("SELECT SCOPE_IDENTITY()")
                self.customer_id = int(cursor.fetchone()[0])
            else:
                # UPDATE
                sql = """
                UPDATE Customers
                SET first_name = ?, last_name = ?, email = ?, is_active = ?
                WHERE customer_id = ?
                """
                params = (self.first_name, self.last_name, self.email, self.is_active, self.customer_id)
                cursor.execute(sql, params)
                conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        """Smaže záznam z DB podle customer_id."""
        if self.customer_id is None:
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Customers WHERE customer_id = ?", (self.customer_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def get_by_id(cls, customer_id):
        """Načte zákazníka podle ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT customer_id, first_name, last_name, email, is_active, date_registered
                FROM Customers 
                WHERE customer_id = ?
            """, (customer_id,))
            row = cursor.fetchone()
            if row:
                return cls(*row)
            return None
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def all(cls):
        """Vrátí seznam všech zákazníků."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT customer_id, first_name, last_name, email, is_active, date_registered
                FROM Customers
            """)
            rows = cursor.fetchall()
            customers = []
            for row in rows:
                customers.append(cls(*row))
            return customers
        finally:
            cursor.close()
            conn.close()
