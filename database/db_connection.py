#This file is to conncet the whoel entire program to MS access database
#This is to import the neccessary modules
import os 
import sqlite3
from pathlib import Path

#This is to gove the location of databse (exact location)
DEFAULT_DB_PATH= Path(__file__).resolve().parent.parent/"secondhand.db"
#This is an envorment variable whicuh is used if the database is being moved
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
    """CREATE TABLE IF NOT EXISTS won't add a column to a table that already exists, so bring older secondhand.db files up to date without losing rows."""
    columns ={r[1] for r in conn.execute("PRAGMA table_info(Orders)")}
    if columns and "PickupNotes" not in columns:
        conn.execute("Alter Table Orders ADD COLUMN PickupNotes TEXT")
        conn.commit()
def get_connection():
    #Starts error handling if the connection fials 
    try:
    #Opens connection suing MS Access driver
        conn= sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SCHEMA)
        return conn

    # This part only runs if an error occurs in the connection.
    except Exception as e:
        print("Connection failed:",e)
        return None