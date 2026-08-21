from dataclasses import dataclass
from datetime import datetime


def _parse_date(text):
    """Turn a staored date string into a date. None if it will not read."""
    try:
        return datetime.fromisoformat(text)
    except (ValueError, TypeError):
        return None


@dataclass
class Item:
    """One item listed in the shop."""

    item_id: int
    name: str
    category: str
    size: str
    condition: str
    price: float
    listing_type: str
    status: str
    seller_id: int
    photo_path: str
    drop_time: str
    date_created: datetime

    @classmethod
    def from_row(cls, row):
        """Make an Item from a database row."""
        return cls(
            item_id=row["ItemID"],
            name=row["itemsName"],
            category=row["Category"],
            size=row["ItemSize"],
            condition=row["Condition"],
            price=row["Price"],
            listing_type=row["ListingType"],
            status=row["Status"],
            seller_id=row["SellerID"],
            photo_path=row["PhotoPath"],
            drop_time=row["DropTime"],
            date_created=_parse_date(row["DateCreated"]),
        )

    def is_free(self):
        """True if the item is free."""
        return self.listing_type == "Donation" 


@dataclass
class User:
    """One user account. password holds the scrambled version"""
    user_id: int
    first_name: str
    last_name: str
    email: str
    password: str
    phone: str
    role: str
    account_status: str
    date_created: datetime

    @classmethod
    def from_row(cls, row):
        """Make a User from a database row."""
        return cls(
            user_id=row["UserID"],
            first_name=row["FirstName"],
            last_name=row["LastName"],
            email=row["SchoolEmail"],
            password=row["Password"],
            phone=row["PhoneNumber"],
            role=row["Role"],
            account_status=row["AccountStatus"],
            date_created=_parse_date(row["DateCreated"])
        )

    def full_name(self):
        """First and last name together"""
        return f"{self.first_name} {self.last_name}"


@dataclass
class Order:
    """One reservation of an item by a buyer."""

    order_id: int
    item_id: int
    buyer_id: int
    payment: str
    pickup: str
    pickup_notes: str
    status: str
    date_created: datetime

    @classmethod
    def from_row(cls, row):
        """Make an Order from a database row"""
        return cls(
            order_id=row["OrderID"],
            item_id=row["ItemID"],
            buyer_id=row["BuyerID"],
            payment=row["Payment"],
            pickup=row["Pickup"],
            pickup_notes=row["PickupNotes"],
            status=row["Status"],
            date_created=_parse_date(row["DateCreated"]),
        )


if __name__ == "__main__":
    # Check each type is built correctly. A dict stands in for a database row.
    item_row = {
        "ItemID": 1, "itemsName": "Blazer", "Category": "Uniform",
        "ItemSize": "M", "Condition": "Good", "Price": 25.0,
        "ListingType": "Sale", "Status": "active", "SellerID": 7,
        "PhotoPath": "", "DropTime": "Mon lunch",
        "DateCreated": "2026-01-31 12:00:00"}
    item = Item.from_row(item_row)
    assert item.name == "Blazer" and item.price == 25.0 and item.seller_id == 7
    assert item.date_created.year == 2026
    assert not item.is_free()

    # A sale priced at 0 is still free

    assert Item.from_row({**item_row, "Price": 0}).is_free()
    assert Item.from_row({**item_row, "ListingType": "Donation"}).is_free()
    assert Item.from_row(
        {**item_row, "DateCreated": "not a date"}).date_created is None

    user = User.from_row({"UserID": 2, "FirstName": "Sam", "LastName": "Blake",
                          "SchoolEmail": "s@x.nz", "Password": "salt:digest",
                          "PhoneNumber": "021", "Role": "Student",
                          "AccountStatus": "Active",
                          "DateCreated": "2026-01-31 12:00:00"})

    assert user.full_name() == "Sam Blake" and user.role == "Student"
    order = Order.from_row(
        {"OrderID": 3, "ItemID": 1, "BuyerID": 2, "Payment": "Cash",
         "Pickup": "Mon lunch", "PickupNotes": "",
         "Status": "reserved", "DropTime": "Mon lunch",
         "DateCreated": "2026-01-31 12:00:00"})

    assert order.order_id == 3 and order.status == "reserved"
    print("models self check OK")
