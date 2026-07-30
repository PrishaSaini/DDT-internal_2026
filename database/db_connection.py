import os
import pyodbc

DEFAULT_DB_PATH=r"C:\Users\prish\OneDrive\Documents\SecondHandShopDB.accdb"
DB_PATH=os.environ.get("SECONDHAND_DB", DEFAULT_DB_PATH)

def row_dict (cursor, row):
    if row is None:
        return None
    return {c[0].lower().replace(" ",""): v for c, v in zip(cursor.despcription, row)}

def get_connection():
    try:
    
        conn= pyodbc.connect(
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            f"DBQ={DB_PATH};"
        )
        print("Connected to database successfully")
        return conn
    except Exception as e:
        print("Connection failed:",e)
        return None