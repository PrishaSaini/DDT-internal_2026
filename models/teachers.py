from dataclasses import dataclass
from datetime import datetime

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