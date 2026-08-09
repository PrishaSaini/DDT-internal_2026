import tkinter as tk
from tkinter import ttk, messagebox
from database.item_db import list_items, get_item, reserve_item
from helper import fmt_price
PAYMENT_OPTIONS=("Card", "Cash")
class CatalogueScreen:
    def __init__(self, root,user):
        self.root = root
        self.user= user
        self.frame =tk.Frame(root)
        self.frame.pack(pady=20)
        tk.Label(self.frame, text="Catalouge", font=("Arial", 18, "bold")).pack(pady=10)
        search_row =tk.Frame(self.frame)
        search_row.pack(pady=5)
        tk.Label(search_row,text="Search").pack(side="left")
        self.search_entry = tk.Entry(search_row, width=25)
        self.search_entry.pack(side="left",padx=5)
        tk.Button(search_row, text="Go", command=self.refresh).pack(side="left")

        columns =("name", "category", "size", "condition", "price")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=10)
        for c, w in zip(columns,(160, 100, 60, 90, 90)):
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=w)
        self.tree.pack(pady=10)
        tk.Button(self.frame, text="Reserve Selected", command=self.reserve).pack(pady=5)
        tk.Button(self.frame,text="Back to Dashboard", command=self.back).pack(pady=5)

        self.refresh()

    def refresh(self):
                self.tree.delete(*self.tree.get_children())
                rows = list_items(self.search_entry.get().strip(),exclude_seller=self.user["id"])
                for r in rows:
                    self.tree.insert("","end",iid=str(r["itemID"]), values=(
                        r["itemsName"], r["Category"], r["ItemSize"],r["Condition"], fmt_price(r["Price"])
                    ))

    def reserve(self):
                selected = self.tree.selection()
                if not selected:
                    messagebox.showerror("Error", "Please select an item first.")
                    return 
                item = get_item(int(selected[0]))
                if item is None:
                    messagebox.showerror("Error","That item no longer exists.")
                    self.refresh()
                    return
                self.frame.destroy()
                ItemDetailScreen(self.root, self.user, item)

    def back(self):
                self.frame.destroy()
                from screen.dashboard import DashboardScreen
                DashboardScreen(self.root, self.user)

class ItemDetailScreen:
        def __init__(self,root,user,item):
                self.root = root
                self.user = user
                self.item = item

                self.frame = tk.Frame(root)
                self.frame.pack(pady=30)

                tk.Label(self.frame, text=item["ItemsName"], font=("Arial", 18, "bold")).pack(pady=5)
                tk.Label(self.frame, text=f'{item["Category"]} . Size{item["ItemSize"]} . {item["Condition"]}').pack()
                tk.Label(self.frame, text=fmt_price(item["Price"]), font=("Arial",14)).pack(pady=10)
                tk.Label(self.frame, text="Payment method", font=("Arial", 10, "bold")).pack(pady=(10, 0))
                self.payment =tk.StringVar(value=PAYMENT_OPTIONS[0])
                for option in PAYMENT_OPTIONS:
                    tk.Radiobutton(self.frame, text=option, value=option,
                                   variable=self.payment).pack(anchor="w")
                tk.Label(self.frame, text="Pickup location",font=("Arial",10,"bold")).pack(pady=(10,0))
                self.pickup_entry = tk.Entry(self.frame, width=30)
                self.pickup_entry.pack(pady=5)

                tk.Button(self.frame, text="Confirm Reserve", command=self.confirm).pack(pady=10)
                tk.Button(self.frame, text="Back", command=self.back).pack(pady=5)

        def confirm(self):
                        pickup =self.pickup_entry.get().strip()
                        if not pickup:
                            messagebox.showerror("Error", "Please enter a pickup location.")
                            return
                        if not reserve_item(self.item["ItemID"], self.user["id"], self.payment.get(),pickup):
                            messagebox.showerror("Error", "Sorry, that item is no longer available.")
                            self.back()
                            return
                        messagebox.showinfo("Reserved", "Item reserved. Check My Orders for the details.")
                        self.back()
                        return

        def back(self):
                        self.frame.destroy()
                        CatalogueScreen(self.root,self.user)