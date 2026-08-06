#This file contains databse functions used for the listing of items
# This is to import neccessary modules
from datetime import datetime
from database.db_connection import get_connection

AVAILABLE =("pending","active")
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
        new_id = cursor.lastrowid
        conn.commit()
        return new_id
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
        return conn.exclude(sql+"ORDER BY DateCreated DESC", params).fetchall()
    finally:
        conn.close()
def my_listings(seller_id):
    conn=get_connection()
    if conn is None:
        return[]
    try:
        return conn.execute(
            "SELECT * FROM Items WHERE SellerID=? ORDER BY DateCreated DESC"
    (seller_id,)
    ).fetchall()
    finally:
        conn.close()
def my_orders(buyer_id):
    conn= get_connection()
    if conn is None:
        return[]
    try:
        return conn.execute("""SElECT o.OrderID, i.itemsName,i.PRICE,o.Payment, o.Pickup, o.Status,o.DateCreated
        FROM Order o JOIN items i ON i.itemID =o.ItemID
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
        return conn.execute("""SELECT o.OrderID, i.itemsName, u.FirstName, o.Paymet, o.Pickup, o.Status, o.DateCreated FROM Orders o JOIN Items i ON i.itemID = o.ItemID
        JOIN Users u ON u.UserID =o.BuyerID
        ORDER BY o.Datecreated DESC""").fetchall()
    finally:
        conn.close()

def reserve_item(item_id, buyer_id, payment, pickup):
    conn= get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Items SET Status='reserved' WHERE ItemID =? NAD Status IN ('pending,'active)"
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
        
    


    