"""Opens the database and creates its tables"""
import os 
import sqlite3
from pathlib import Path

#Database file sits next to main.py. SECONDHAND_DB can point somehwere else.
DEFAULT_DB_PATH= Path(__file__).resolve().parent.parent/"secondhand.db"
DB_PATH=os.environ.get("SECONDHAND_DB", str(DEFAULT_DB_PATH))

SCHEMA ="""
CREATE TABLE IF NOT EXISTS Users (
    UserID        INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName     TEXT NOT NULL,
    LastName      TEXT NOT NULL,
    SchoolEmail   TEXT NOT NULL UNIQUE COLLATE NOCASE,
    Password      TEXT NOT NULL, 
    PhoneNumber   TEXT,
    Role          TEXT NOT NULL DEFAULT 'Student',
    AccountStatus TEXT NOT NULL DEFAULT 'Active',
    DateCreated   TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS Items (
    ItemID        INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemsName     TEXT NOT NULL,
    Category      TEXT,
    ItemSize      TEXT, 
    Condition     TEXT NOT NULL, 
    Price         REAL,
    ListingType   TEXT,
    Status        TEXT NOT NULL DEFAULT 'pending',
    SellerID      INTEGER REFERENCES Users(UserID),
    PhotoPath     TEXT,
    DateCreated   TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS Orders (
    OrderID       INTEGER PRIMARY KEY AUTOINCREMENT,
    ItemID        INTEGER REFERENCES Items(ItemID),
    BuyerID       INTEGER REFERENCES Users(UserID),
    ItemSize      TEXT, 
    Payment       TEXT NOT NULL, 
    Pickup        TEXT NOT NULL,
    PickupNotes   TEXT,
    ListingType   TEXT NOT NULL,
    Status        TEXT NOT NULL DEFAULT 'reserved',
    DateCreated   TEXT NOT NULL
);
"""

def _add_missing_columns(conn):
   """Add any column missing from an older database file."""
   columns ={r[1] for r in conn.execute("PRAGMA table_info(Orders)")}
   if columns and "PickupNotes" not in columns:
        conn.execute("Alter Table Orders ADD COLUMN PickupNotes TEXT")
        conn.commit()


def get_connection():
    """Open the database, none if it will not open."""
    try:
        conn= sqlite3.connect(DB_PATH)
        #read columns by name, e.g row ["Price"]
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SCHEMA)
        _add_missing_columns(conn)
        return conn
    except Exception as e:
        print("Connection failed:",e)
        return None