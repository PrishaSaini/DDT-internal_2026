#This file is to conncet the whoel entire program to MS access database
#This is to import the neccessary modules
import os 
import pyodbc

#This is to gove the location of databse (exact location)
DEFAULT_DB_PATH=r"C:\Users\prish\OneDrive\Documents\SecondHandShopDB.accdb"
#This is an envorment variable whicuh is used if the database is being moved
DB_PATH=os.environ.get("SECONDHAND_DB", DEFAULT_DB_PATH)

"""This function changes the row  to a dictionary. It is so the values are easier to used"""
def row_dict (cursor, row):
    #Check whether db returned no row. It return nothimg if no row
    if row is None: 
        return None
    #This matches the column name with its value and aswell changes column name to lowercase and strip spaves
    return {c[0].lower().replace(" ",""): v for c, v in zip(cursor.despcription, row)}
"""This function actually connects the db to Access databse   """
def get_connection():
    #Starts error handling if the connection fials 
    try:

    #Opens connection suing MS Access driver
        conn= pyodbc.connect(
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" #Selects the Acess database driver
            f"DBQ={DB_PATH};" #Gives driver location of the db
        )
        print("Connected to database successfully")
        return conn # Sens the opned connection to the part of program which requires it

    # This part only runs if an error occurs in the connection.
    except Exception as e:
        print("Connection failed:",e)
        return None