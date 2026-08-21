"""All the database queries for items, orders and users."""
from datetime import datetime

from database.db_connection import get_connection

# An item goes : pending -> active -> reserved -> sold. Admin can reject it.
STATUS_PENDING = "pending"
STATUS_ACTIVE = "active"
STATUS_RESERVED = "reserved"
STATUS_SOLD = "sold"
STATUS_REJECTED = "rejected"

# An order goes: reserved -> ready -> collected, or gets canacelled.
ORDER_RESERVED = "reserved"
ORDER_READY = "ready"
ORDER_COLLECTED = "collected"
ORDER_CANCELLED = "cancelled"

# Once an order is collected or cancelled it cannot change again
FINAL_ORDER_STATUSES = (ORDER_COLLECTED, ORDER_CANCELLED)

# Finishing an order also changes its item.
ITEM_STATUS_FOR = {ORDER_COLLECTED: STATUS_SOLD, 
                   ORDER_CANCELLED: STATUS_ACTIVE}
ORDER_VALID_OPTIONS = {ORDER_RESERVED:(
    ORDER_READY,
    ORDER_CANCELLED),ORDER_READY:(ORDER_COLLECTED,ORDER_CANCELLED)}

ACCOUNT_ACTIVE = "Active"
ACCOUNT_DISABLED = "Disabled"
ROLE_STUDENT = "Student"
ROLE_ADMIN = "Admin"


def _now():
    """Today's date and time as text, for the DateCreated columns."""
    return datetime.now().isoformat(" ", "seconds")


def add_item(item_name, category, item_size, condition, price, listing_type,
             seller_id, photo_path="", drop_time=""):
    """Save a new listing and return its id. New items start as pending."""
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO Items
        (itemsName, Category, ItemSize, Condition, Price, ListingType, Status,
          SellerID, PhotoPath, DropTime, DateCreated )
        VALUES(?,?,?,?,?,?,?,?,?,?,?)"""
        cursor.execute(
            sql,
            (item_name,
             category,
             item_size,
             condition,
             price,
             listing_type,
             STATUS_PENDING,
             seller_id,
             photo_path,
             drop_time,
             _now()))
        new_id = cursor.lastrowid
        conn.commit()
        return new_id
    finally:
        conn.close()


def get_item(item_id):
    """Find one item by its id."""
    conn = get_connection()
    if conn is None:
        return None
    try:
        return conn.execute(
            "SELECT * FROM Items WHERE ItemID =?", (item_id,)).fetchone()
    finally:
        conn.close()


def list_items(search=""):
    """Items for the catalogue: approved and not yet taken"""
    conn = get_connection()
    if conn is None:
        return []
    try:
        sql = "SELECT * FROM Items WHERE Status = ? "
        params = [STATUS_ACTIVE]
        if search:
            sql += (
                "AND (itemsName LIKE ? OR Category LIKE ? "
                " OR ItemSize LIKE ? OR Condition LIKE ? "
                " OR CAST(Price AS TEXT) LIKE ? OR ListingType LIKE ?) ")
            params += ["%" + search + "%"] * 6
        return conn.execute(
            sql + "ORDER BY DateCreated DESC",
            params).fetchall()
    finally:
        conn.close()


def my_listings(seller_id):
    conn = get_connection()
    if conn is None:
        return []
    try:
        return conn.execute(
            "SELECT * FROM Items WHERE SellerID= ? ORDER BY DateCreated DESC",
            (seller_id,)
        ).fetchall()
    finally:
        conn.close()


def my_orders(buyer_id):
    """Featch this buyer's orders, with the item name from Items"""
    conn = get_connection()
    if conn is None:
        return []
    try:
        return conn.execute("""
        SELECT o.OrderID, o.ItemID, o.BuyerID, i.itemsName, i.Price,
        i.ListingType, 
        o.Payment, o.Pickup, o.Status, o.DateCreated, o.PickupNotes 
        FROM Orders o JOIN Items i ON i.ItemID =o.ItemID
        WHERE o.BuyerID =? ORDER BY o.DateCreated DESC""", 
        (buyer_id,)).fetchall()
    finally:
        conn.close()


def all_items():
    """Every item, for the admin screen."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        return conn.execute(
            "SELECT * FROM Items ORDER BY DateCreated DESC"
            ).fetchall()
    finally:
        conn.close()


def all_orders():
    """EVERY order with its item and buyer name, for the admin screen."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        return conn.execute("""
        SELECT o.OrderID, o.ItemID,  o.BuyerID, i.itemsName, u.FirstName, 
        o.Payment, o.Pickup, o.Status, o.DateCreated, o.PickupNotes 
        FROM Orders o 
        JOIN Items i ON i.itemID = o.ItemID
        JOIN Users u ON u.UserID = o.BuyerID
        ORDER BY o.Datecreated DESC""").fetchall()
    finally:
        conn.close()


def set_item_status(item_id, status):
    """Approve or reject an item. False if it was already decided"""
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Items SET Status  = ? WHERE ItemID = ? AND Status = ? ",
            (status,
             item_id,
             STATUS_PENDING))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def reserve_item(item_id, buyer_id, payment, pickup, pickup_notes=""):
    """Reserve an item, False if someoen else got it first."""
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        # Active item only, 0 rows means it was already taken.
        cursor.execute(
            "UPDATE Items SET Status= ? WHERE ItemID =? AND  Status = ?",
            (STATUS_RESERVED,
             item_id,
             STATUS_ACTIVE))
        if cursor.rowcount == 0:
            conn.rollback()
            return False
        item = cursor.execute(
            "SELECT ItemSize, Listingtype FROM Items WHERE ItemID = ?", (
                item_id,)
        ).fetchone()
        cursor.execute(
            """
            INSERT INTO Orders
            (ItemID, BuyerID, ItemSize, Payment, Pickup, PickupNotes,
            ListingType,
            Status, DateCreated)
            VALUES ( ?,?,?,?,?,?,?,?,?)""",
            (item_id,
             buyer_id,
             item["ItemSize"],
             payment,
             pickup,
             pickup_notes,
             item["ListingType"],
             ORDER_RESERVED,
             _now())
        )
        conn.commit()
        return True
    finally:
        conn.close()


def all_users():
    """Every user account, for the admin screen."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        return conn.execute(
            "SELECT * FROM Users ORDER BY DateCreated DESC").fetchall()
    finally:
        conn.close()


def set_account_status(user_id, status):
    """Apprive or reject an """
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE Users SET AccountStatus = ? WHERE UserID = ?", 
            (status,user_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def set_order_status(order_id, status, buyer_id=None):
    """Change an order's status. False if it is already finshed.

    Pass buyer_id so a studnet can only cancel their own order,
    """
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        # A finished order must not be changed again.
        # placeholders = ",".join("?" * len(FINAL_ORDER_STATUSES))
        # status not in(ORDER_COLLECTED, ORDER_CANCELLED)
        # sql = f"""UPDATE Orders SET Status = ? 
        #           WHERE OrderID = ? AND Status NOT IN ({placeholders})"""
        # params = [status, order_id] + list(FINAL_ORDER_STATUSES)
        order = cursor.execute(
            "SELECT Status from Orders WHERE OrderID =?",(order_id,)
        ).fetchone()
        if order is None:
            return False
        current_status = order["Status"]
        if status not in ORDER_VALID_OPTIONS.get(current_status,()):
            return False
        sql="""UPDATE Orders SET Status = ? 
        WHERE OrderID = ? AND Status = ?"""
        params = [status, order_id, current_status]
        if buyer_id is not None:
            sql+=" AND BuyerID = ?"
            params.append(buyer_id)
        cursor.execute(sql, params)
        if cursor.rowcount == 0:
            conn.rollback()
            return False
        item_status = ITEM_STATUS_FOR.get(status)
        if item_status:
            cursor.execute("""UPDATE Items SET Status = ? 
            WHERE ItemID = (SELECT ItemId FROM Orders 
                            WHERE OrderID = ?)""",
                           (item_status, order_id))
        conn.commit()
        return True
    finally:
        conn.close()


MAX_PHOTOS = 3


def add_photos(item_id, paths):
    paths = [p.strip() for p in paths if p and p.strip()][:MAX_PHOTOS]
    if not paths:
        return 0
    conn = get_connection()
    if conn is None:
        return 0
    try:
        conn.executemany(
            "INSERT INTO ItemPhotos (ItemID, Path, Position) VALUES (?,?,?)",
            [(item_id, path, i) for i, path in enumerate(paths)]
        )
        conn.commit()
        return len(paths)
    finally:
        conn.close()


def item_photos(item_id):
    conn = get_connection()
    if conn is None:
        return []
    try:
        return [r["Path"] for r in conn.execute(
            "SELECT Path FROM ItemPhotos WHERE ItemID = ? ORDER BY Position",
            (item_id,))]
    finally:
        conn.close()
    # none menas the databse won't open

def user_login_check(email):
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        sql = """
        SELECT * FROM Users
        WHERE SchoolEmail = ? AND AccountStatus =?
        """
        cursor.execute(sql, (email, ACCOUNT_ACTIVE))
        user = cursor.fetchone()
        if user is None:
            return False
        else:
            return user
    finally:
        conn.close()

def create_account(first_name, last_name, email, hashed_password, phone):
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT UserID FROM Users WHERE SchoolEmail =?", (email,)
            )
        if cursor.fetchone():
            return False
    
        sql = """
        INSERT INTO Users
        (FirstName,
        LastName,
        SchoolEmail,
        Password,
        PhoneNumber,
        Role,
        AccountStatus,
        DateCreated)
        VALUES (?, ?, ?, ?, ?, ?, ?,?)
        """
        cursor.execute(
            sql,
            (first_name,
             last_name,
             email,
             hashed_password,
             phone,
             ROLE_STUDENT,
             ACCOUNT_ACTIVE,
             datetime.now().isoformat(" ", "seconds")))
        conn.commit()
        return True
    finally:
        conn.close()
