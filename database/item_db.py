#This file contains databse functions used for the listing of items
# This is to import neccessary modules
from datetime import datetime
from database.db_connection import get_connection
"""This function adds a new listing to the items table and it alsoe retunr the new id"""
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
        cursor.execute(sql, (item_name, category, item_size, condition, price, listing_type, "pending", seller_id, photo_path, datetime.now()))
        cursor.execute("SELECT @@IDENTITY")
        new_id = cursor.fetchone()[0]
        conn.commit()
        return new_id
    finally:
        conn.close()


