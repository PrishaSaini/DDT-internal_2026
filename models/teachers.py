#This class stores details neede for the tecaher
from dataclasses import dataclass
from datetime import datetime
#Automaticaally creates the setup from the teacherclass the setup method for it
@dataclass
class Teacher:
    teacher_id: int
    first_name: str
    last_name: str
    email: str
    subject: str
    address: str
    password: str
    created_at:datetime
    updated_at: datetime