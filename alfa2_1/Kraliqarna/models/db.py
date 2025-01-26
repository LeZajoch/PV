# db.py
import pyodbc
import configparser
import os


def get_db_connection():
    """Načte nastavení z config.ini a vrátí připojení k MSSQL."""
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "..", "config.ini"))

    driver = config.get('DATABASE', 'driver')
    server = config.get('DATABASE', 'server')
    database = config.get('DATABASE', 'database')
    uid = config.get('DATABASE', 'uid')
    pwd = config.get('DATABASE', 'pwd')

    connection_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={uid};PWD={pwd}"

    try:
        conn = pyodbc.connect(connection_str)
        return conn
    except pyodbc.Error as e:
        raise Exception(f"Chyba připojení k databázi: {e}")
