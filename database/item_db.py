from datetime import datetime

from database.db_connection import get_connection

def add_item(item_name, category, item_size, condition, price, listing_type, seller_id, photo_path=""):
    conn= get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql="""
        INSERT INTO Items
        (itemsName, Category, ItemSize, Condition, Price, ListingType, Status, SellerID, PhotoPath, DateCreated )
        VALUES(?,?,?,?,?,?,?,?,?,?)"""
        cursor.execute(sql, (item_name, category, item_size, condition, price, listing_type, "pending", seller_id, photo_path, datetime.now()))
        cursor.execute("SELECT @@IDENTITY")
        new_id = cursor.fetchone()[0]
        conn.commit()
        return new_id
    finally:
        conn.close()

