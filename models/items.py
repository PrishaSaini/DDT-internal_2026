#This file 
#This is to import all the neccessary modules
from dataclasses import dataclass
from datetime import datetime
#Automaticaally creates the setup from the itemclass the setup method for it
@dataclass
class Item:
    #Create sclass to reprenstent each item
    item_id: int
    item_name: str
    item_description: str
    item_quantity: int
    estimated_value: float
    date_listed: datetime