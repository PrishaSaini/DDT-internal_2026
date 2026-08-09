import tkinter as tk
from tkinter import ttk, messagebox

from database.item_db import(my_listings, my_orders, all_orders, set_item_status, all_items)
from helper import fmt_price

def _table(parent, headings, rows, widths, iids=None):
    tree =ttk.Treeview(parent, columns=headings, show="headings", height=8)
    for h, w in zip(headings, widths):
        tree.heading(h, text=h)
        tree.column(h, width=w)
    for i, r in enumerate(rows):
        tree.insert("", "end", iid=(str(iids[i]) if iids else None ),values=r)
    tree.pack(pady=8)
    return tree

class _BaseScreen:
    title="" 

    def __init__(self,root,user):
        self.root = root
        self.root.configure(bg="#F0F5F6")
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
    title="My Listings"

    def body(self):
        rows=[(r["ItemsName"], r["Category"], r["ItemSize"], r["Condition"], 
               fmt_price(r["Price"]), r["Status"]) for r in my_listings(self.user["id"])]
        _table(self.frame,("Name", "Category", "Size", "Condition", "Price", "Status"),
        rows, (150,100,60,90,90))
class MyOrdersScreen(_BaseScreen):
    title ="My Orders"

    def body(self):
        rows=[(r["OrderID"], r["ItemsName"], fmt_price(r["Price"]), r["Payment"], 
                                                       r["Pickup"], r["Status"]) for r in my_orders(self.user["id"])]
        _table(self.frame,("Order", "Item", "Price", "Payment", "Pickup", "Status"),
        rows, (150,100,60,90,90,90))


class AdminScreen(_BaseScreen):
    title= "Admin Dashboard"

    def body(self):
        tk.Label(self.frame, text="All Items", font=("Arial", 12, "bold")).pack()
        items= all_items() 
        item_rows=[(r["ItemsName"], r["Category"], fmt_price(r["Price"]), r["ListingType"], r["Status"]) for r in items]
        self.items_tree =_table (self.frame,("Name", "Category", "Price", "Type", "Status"),
        item_rows, (150,100,60,90,90,90), iids=[r["ItemID"] for r in items])
        tk.Label(self.frame, text="All Orders", font=("Arial", 12, "bold")).pack()
        order_rows=((r["OrderID"], r["ItemsName"], r["FirstName"], r["Pickup"], r["Payment"], r["Status"])  for r in all_orders())
        _table(self.frame, ("Order", "item", "Buyer", "Pickup", "Payment", "Status"), order_rows, (60, 140, 100, 120, 120, 90))
        buttons = tk.Frame(self.frame)
        buttons.pack(pady=4)

        tk.Button(
             buttons, text="Approve", width=10, command=lambda: self.decide("active")).pack(side="left",padx=4)
        tk.Button (buttons, text="Reject", width=10, command=lambda: self.decide("rejected")).pack(side="left",padx=4)
    def decide(self,status):
        selected = self.items_tree.selection()

        if not selected:
            messagebox.showerror("Error", "Please select an item first")
            return
        if not set_item_status(int(selected[0]),status):
            messagebox.showerror("Error", "That item has already been decided.")
            return
        messagebox.showinfo("Done",f"Item marked{status}.")
        self.frame.destroy()
        AdminScreen(self.root, self.user)

       
        

                                                