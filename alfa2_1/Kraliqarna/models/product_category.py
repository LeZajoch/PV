# product_category.py
from .db import get_db_connection

class ProductCategory:
    """
    Vazební tabulka M:N: Propojuje product_id s category_id.
    """
    def __init__(self, product_id=None, category_id=None):
        self.product_id = product_id
        self.category_id = category_id

    def save(self):
        if self.product_id is None or self.category_id is None:
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # INSERT (PK je [product_id, category_id], tak ať nedojde k duplicitě)
            sql_check = """SELECT COUNT(*) FROM ProductCategories 
                           WHERE product_id = ? AND category_id = ?"""
            cursor.execute(sql_check, (self.product_id, self.category_id))
            count = cursor.fetchone()[0]
            if count == 0:
                sql_insert = """
                INSERT INTO ProductCategories (product_id, category_id)
                VALUES (?, ?)
                """
                cursor.execute(sql_insert, (self.product_id, self.category_id))
                conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        if self.product_id is None or self.category_id is None:
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            sql_del = """DELETE FROM ProductCategories 
                         WHERE product_id = ? AND category_id = ?"""
            cursor.execute(sql_del, (self.product_id, self.category_id))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def get_all(cls):
        """
        Vrací všechny vazby (product_id, category_id).
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT product_id, category_id FROM ProductCategories")
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append(cls(*row))
            return result
        finally:
            cursor.close()
            conn.close()
