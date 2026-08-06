import tkinter as tk
from tkinter import ttk

from database.item_db import my_listings, my_orders, all_items, all_orders
from helper import fmt_price

def _table(parent, headings, rows, widths):
    tree =ttk.Treeview(parent, columns=headings, show="headings", height=8)
    for h, w in zip(headings, widths):
        tree.heading(h, text=h)
        tree.column(h, width=w)
    for r in rows:
        tree.insert("", "end", values=r)
    tree.pack(pady=8)
    return tree

class _BaseScreen:
    title="" 

    def __init__(self,root,user):
        self.root = root
        self.user = user

        self.frame =tk.Frame(root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text=self.title, font=("Arial", 28, "bold")).pack(pady=10)
        self.body()
        tk.Button(self.frame, text="Back to Dashboard", command=self.back).pack(pady=10)

    def body(self):
        raise NotImplementedError

    def back(self):
        self.frame.destroy()
        from screen.dashboard import DashboardScreen
        DashboardScreen(self.root, self.user)


class MyListingsScreen(_BaseScreen):
    title="My Listing"

    def body(self):
        rows=[(r["ItemsName"], r["Category"], r["ItemSize"], r["Condition"], 
               fmt_price(r["Price"]), r["Status"]) for r in my_listings(self.user["id"])]
        _table(self.frame),("Name", "Category", "Size", "Condition", "Price", "Status")
        rows, (150,100,60,90,90,90)
class MyOrdersScreen(_BaseScreen):
    title ="My Orders"

    def body(self):
        rows=[(r["OrderID"], r["itemsName"], fmt_price(r["Price"]), r["Payment"], 
                                                       r["Pickup"], r["Status"]) for r in my_orders(self.user["id"])]
        _table(self.frame),("Order", "Item", "Price", "Payment", "Pickup", "Status")
        rows, (150,100,60,90,90,90)


class AdminScreen(_BaseScreen):
    title="Admin Dashboard"

    def body(self):
        tk.Label(self.frame, text="All Items", font=("Arial", 12, "bold")).pack() 
        item_row=[(r["ItemName"], r["Category"], fmt_price(r["Price"]), r["ListingType"], r["Status"]) for r in all_items()]
        item_row, (150,100,60,90,90,90)
        tk.Label(self.frame, text="All Orders", font=("Arial", 12, "bold")).pack()
        item_row=((r["OrderID"], r["ItemsName"], r["Pickup"], r[" First Name"], r["Payment"], r["Statuts"])  for r in all_items())
        _table(self.frame("Order", "Item", "Buyer", "Payment", "Pickup", "Status"),)
        item_row, (60, 140, 100, 120, 120, 90)

                                                
    