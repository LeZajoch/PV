# product.py
import datetime
from .db import get_db_connection

class Product:
    def __init__(self, product_id=None, product_name=None, price=0.0,
                 product_status='active', created_at=None):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.product_status = product_status
        self.created_at = created_at or datetime.datetime.now()

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            if self.product_id is None:
                # INSERT
                sql = """
                INSERT INTO Products (product_name, price, product_status, created_at)
                VALUES (?, ?, ?, ?)
                """
                params = (self.product_name, self.price, self.product_status, self.created_at)
                cursor.execute(sql, params)
                conn.commit()
                # Zisk ID
                cursor.execute("SELECT SCOPE_IDENTITY()")
                self.product_id = int(cursor.fetchone()[0])
            else:
                # UPDATE
                sql = """
                UPDATE Products
                SET product_name = ?, price = ?, product_status = ?
                WHERE product_id = ?
                """
                params = (self.product_name, self.price, self.product_status, self.product_id)
                cursor.execute(sql, params)
                conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        if self.product_id is None:
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Products WHERE product_id = ?", (self.product_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def get_by_id(cls, product_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT product_id, product_name, price, product_status, created_at
                FROM Products
                WHERE product_id = ?
            """, (product_id,))
            row = cursor.fetchone()
            if row:
                return cls(*row)
            return None
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT product_id, product_name, price, product_status, created_at
                FROM Products
            """)
            rows = cursor.fetchall()
            products = []
            for row in rows:
                products.append(cls(*row))
            return products
        finally:
            cursor.close()
            conn.close()
