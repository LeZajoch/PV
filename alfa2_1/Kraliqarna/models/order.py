# order.py
import datetime
from .db import get_db_connection

class Order:
    def __init__(self, order_id=None, customer_id=None, order_status='pending', order_date=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_status = order_status
        self.order_date = order_date or datetime.datetime.now()
        # Seznam (product_id, quantity)
        self.items = []

    def save(self):
        """Uložení objednávky + položek s využitím transakce."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            conn.autocommit = False  # Začátek transakce

            if self.order_id is None:
                # INSERT do Orders
                sql = """
                INSERT INTO Orders (customer_id, order_status, order_date)
                VALUES (?, ?, ?)
                """
                params = (self.customer_id, self.order_status, self.order_date)
                cursor.execute(sql, params)
                cursor.execute("SELECT SCOPE_IDENTITY()")
                self.order_id = int(cursor.fetchone()[0])
            else:
                # UPDATE Orders
                sql = """
                UPDATE Orders
                SET customer_id = ?, order_status = ?
                WHERE order_id = ?
                """
                params = (self.customer_id, self.order_status, self.order_id)
                cursor.execute(sql, params)
                # Smažeme staré OrderItems
                cursor.execute("DELETE FROM OrderItems WHERE order_id = ?", (self.order_id,))

            # INSERT OrderItems
            for (product_id, quantity) in self.items:
                sql_item = """
                INSERT INTO OrderItems (order_id, product_id, quantity)
                VALUES (?, ?, ?)
                """
                cursor.execute(sql_item, (self.order_id, product_id, quantity))

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Chyba při ukládání objednávky: {e}")
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        """Smaže objednávku a její položky."""
        if self.order_id is None:
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            conn.autocommit = False
            # Nejdříve smažeme OrderItems
            cursor.execute("DELETE FROM OrderItems WHERE order_id = ?", (self.order_id,))
            # Poté Orders
            cursor.execute("DELETE FROM Orders WHERE order_id = ?", (self.order_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Chyba při mazání objednávky: {e}")
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def get_by_id(cls, order_id):
        """Načte objednávku (bez položek)."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT order_id, customer_id, order_status, order_date
                FROM Orders
                WHERE order_id = ?
            """, (order_id,))
            row = cursor.fetchone()
            if row:
                o = cls(*row)
                # Doobjednáme položky
                cursor.execute("SELECT product_id, quantity FROM OrderItems WHERE order_id = ?", (order_id,))
                item_rows = cursor.fetchall()
                for ir in item_rows:
                    o.items.append((ir[0], ir[1]))
                return o
            return None
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def all(cls):
        """Načte jen základní data, bez položek (ty je pak možno dočítat get_by_id)."""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT order_id, customer_id, order_status, order_date
                FROM Orders
            """)
            rows = cursor.fetchall()
            orders = []
            for row in rows:
                orders.append(cls(*row))
            return orders
        finally:
            cursor.close()
            conn.close()
