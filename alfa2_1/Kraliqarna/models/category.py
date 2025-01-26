# category.py
from .db import get_db_connection

class Category:
    def __init__(self, category_id=None, category_name=None):
        self.category_id = category_id
        self.category_name = category_name

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            if self.category_id is None:
                # INSERT
                sql = "INSERT INTO Categories (category_name) VALUES (?)"
                cursor.execute(sql, (self.category_name,))
                conn.commit()
                cursor.execute("SELECT SCOPE_IDENTITY()")
                self.category_id = int(cursor.fetchone()[0])
            else:
                # UPDATE
                sql = "UPDATE Categories SET category_name = ? WHERE category_id = ?"
                cursor.execute(sql, (self.category_name, self.category_id))
                conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        if self.category_id is None:
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Categories WHERE category_id = ?", (self.category_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def get_by_id(cls, category_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT category_id, category_name FROM Categories WHERE category_id = ?", (category_id,))
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
            cursor.execute("SELECT category_id, category_name FROM Categories")
            rows = cursor.fetchall()
            categories = []
            for row in rows:
                categories.append(cls(*row))
            return categories
        finally:
            cursor.close()
            conn.close()
