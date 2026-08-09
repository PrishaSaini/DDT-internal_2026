#This file contains databse functions used for the listing of items
# This is to import neccessary modules
from datetime import datetime
from database.db_connection import get_connection

def now():
    return datetime.now().isoformat(" ","seconds")

def add_item(item_name, category, item_size, condition, price, listing_type, seller_id, photo_path=""): 

    # For opening connection to databse
    conn= get_connection()
    #Checks whether the datbase connection failed or not
    if conn is None:
        return None
    #Start of database error handling 
    try:
        #Creates a cursor used to run the SQL commans
        cursor = conn.cursor()
        sql="""
        INSERT INTO Items
        (itemsName, Category, ItemSize, Condition, Price, ListingType, Status, SellerID, PhotoPath, DateCreated )
        VALUES(?,?,?,?,?,?,?,?,?,?)"""

        cursor.execute(sql, (
            item_name, category, item_size, condition, price, listing_type,"pending", seller_id, photo_path, now()
        ))
        new_id = cursor.lastrowid
        conn.commit()
        return new_id
    except Exception as e:
        print("add_item error:", e)
        return None
    finally:
        conn.close()

def get_item(item_id):
    conn = get_connection()
    if conn is None:
        return None
    try:
        return conn.execute("SELECT * FROM Items WHERE ItemID =?", (item_id,)).fetchone()
    finally:
        conn.close()
def list_items(search="",exclude_seller=None):
    conn=get_connection()
    if conn is None:
        return[]
    try:
        sql ="SELECT * FROM Items WHERE Status IN ('pending','active')"
        params=[]
        if search:
            sql+="AND (itemsName LIKE ? OR Category LIKE ?)"
            params+=["%"+search+"%"]*2
        if exclude_seller is not None:
            sql+="AND SellerID<>?"
            params.append(exclude_seller)
        return conn.execute(sql + "ORDER BY DateCreated DESC", params).fetchall()
    finally:
        conn.close()
def my_listings(seller_id):
    conn=get_connection()
    if conn is None:
        return[]
    try:
        return conn.execute(
            "SELECT * FROM Items WHERE SellerID= ? ORDER BY DateCreated DESC",
    (seller_id,)
    ).fetchall()
    finally:
        conn.close()

def my_orders(buyer_id):
    conn= get_connection()
    if conn is None:
        return[]
    try:
        return conn.execute("""SELECT o.OrderID, i.itemsName, i.Price, o.Payment, o.Pickup, o.Status, o.DateCreated
        FROM Orders o JOIN Items i ON i.ItemID =o.ItemID
        WHERE o.BuyerID =? ORDER BY o.DateCreated DESC""", (buyer_id,)).fetchall()
    finally:
        conn.close()

def all_items():
    conn = get_connection()
    if conn is None:
        return[]
    try:
        return conn.execute("SELECT * FROM Items ORDER BY DateCreated DESC").fetchall()
    finally:
        conn.close()

def all_orders():
    conn = get_connection()
    if conn is None:
        return[]
    try:
        return conn.execute("""SELECT o.OrderID, i.itemsName, u.FirstName, o.Payment, o.Pickup, o.Status, o.DateCreated FROM Orders o JOIN Items i ON i.itemID = o.ItemID
        JOIN Users u ON u.UserID = o.BuyerID
        ORDER BY o.Datecreated DESC""").fetchall()
    finally:
        conn.close()
        
def set_item_status(item_id, status):
    conn= get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE Items SET STATUS =? WHERE ItemID = ? AND Status = 'pending'",
                       (status, item_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

        


def reserve_item(item_id, buyer_id, payment, pickup):
    conn= get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Items SET Status='reserved' WHERE ItemID =? AND  Status IN ('active')",
            (item_id))
        if cursor.rowcount ==0:
            conn.rollback()
            return False 
        cursor.execute("""INSERT INTO Orders (ItemsID, BuyerID, Paymnet, Pickup, Status, DateCreated)VALUES ( ?,?,?,?,?,?)""",
                                       (item_id, buyer_id, payment, pickup, "reserved", now()))
        conn.commit()
        return True
    finally:
        conn.close()
        
    


    