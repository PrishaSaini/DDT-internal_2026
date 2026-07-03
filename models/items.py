from dataclasses import dataclass
from datetime import datetime
@dataclass
class Item:
    item_id: int
    item_name: str
    item_description: str
    item_quantity: int
    estimated_value: float
    date_listed: datetime