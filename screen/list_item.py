import tkinter as tk
from tkinter import ttk, messagebox
from database.item_db import add_item
from helper import parse_price

CATEGORIES =("Uniforms", "Textbooks", "Stationery", "Sports Gear", "Other")
SIZES =("XS", "S", "M", "L", "XL","N/A")
CONDITIONS=("New", "Like New", "Good", "Fair")
LISTING_TYPES =("Sale","Donation")

class ListItemScreen:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="List an Item", font=("Arial", 18,"bold")).pack(pady=10)

        self.name_entry =self._entry("Item Name")
        self.category_box = self._dropdown("Category", CATEGORIES)
        self.size_box = self._dropdown("Size", SIZES)
        self.condition_box =self._dropdown("Condition", CONDITIONS)
        self.type_box = self._dropdown("Listing Type", LISTING_TYPES)
        self.price_entry= self._entry("Price (leave blank to donate)")
        self.photo_entry = self._entry("Photo Path(optional)")

        tk.Button(self.frame, text="Create Listing", command=self._create).pack(pady=15)
        tk.Button(self.frame, text="Back to Dashboard", command=self.back).pack(pady=5)

    def _entry(self,label):
        tk.Label(self.frame, text=label).pack()
        e = tk.Entry(self.frame, width=30)
        e.pack(pady=3)
        return e

    def _create(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter an item name.")
            return

        listing_type =self.type_box.get()
        raw_price = self.price_entry.get().strip()
        if listing_type == "Donation" or not raw_price:
            price =0.0
        else:
            price = parse_price(raw_price)
            if price is None:
                messagebox.showerror("Error", "Please neter a valid proce(0 or more).")
                return
        item_id = add_item(name, self.category_box.get(), self.size_box.get(),
                           self.condition_box.get(), price, listing_type,
                           self.user["id"], self.photo_entry.get().strip())
        if item_id is None:
            messagebox.showerror("Error","Could not save the listing")
            return
        messagebox.showinfo("Listed", "Your item has been listed.")
        self.back()

    def back(self):
        self.frame.destroy()
        from screen.dashboard import DashboardScreen
        DashboardScreen(self.root, self.user)

    def _dropdown(self, label, values):
        tk.Label(self.frame, text=label).pack()
        box =ttk.Combobox(self.frame, values=values, state="readonly",width=27)
        box.set(values[0])
        box.pack(pady=3)
        return box