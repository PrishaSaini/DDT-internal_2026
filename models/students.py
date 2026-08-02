#This file staores details needed for ome student record
from dataclasses import dataclass
from datetime import datetime

#Automaticaally creates the setup from the studentclass the setup method for it
@dataclass
class Student:
    student_id:int
    first_name: str
    last_name: str
    year: int
    address: str
    created_at: datetime
    updated_at: datetime
    email: str
    phone: str
