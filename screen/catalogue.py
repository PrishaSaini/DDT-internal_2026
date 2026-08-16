import tkinter as tk
from tkinter import ttk, messagebox
from database.item_db import list_items, get_item, reserve_item
from helper import fmt_price
from screen import ui
PAYMENT_OPTIONS=("Card", "Cash")
PICKUP_SLOTS=("Mon lunch", "tue lunch", "wed lunch", "thurs lunch", "fri lunch")
class CatalogueScreen: 
    def __init__(self, root,user):
        self.root = root
        self.user= user
        
        self.frame =ui.card(root, padx=24, pady=20)
        self.frame.pack(pady=20)

        ui.accent_bar(self.frame).pack(fill="x", pady=(0,12))
        ui.title(self.frame, "Catalogue").pack(pady=(0, 10))
        search_row =tk.Frame(self.frame)
        search_row.pack(pady=5)
        ui.field_label(search_row,text="Search").pack(side="left", padx=(0, 6))
        self.search_entry = ui.entry(search_row, width=25)
        self.search_entry.pack(side="left",padx=5)
        ui.primary_button(search_row, "Go", self.refresh).pack(side="left")

        self.tree =ui.table(
                self.frame, ("Item", "Category", "Size", "Condition", "Price"),
                (170,100,60,100,80),
                height=10
        )
        self.tree.pack(pady=10)
        buttons=tk.Frame(self.frame, bg=ui.CARD)
        buttons.pack(pady=5)

        ui.primary_button(buttons, "Reserve Selected", self.reserve).pack(pady=5)
        ui.button(buttons, "Back to Dashboard", self.back).pack(side="left", pady=5)

        self.refresh()

    def refresh(self):
                self.tree.delete(*self.tree.get_children())
                rows = list_items(self.search_entry.get().strip())
                for r in rows:
                    self.tree.insert("","end",iid=str(r["ItemID"]), values=(
                        r["ItemsName"], r["Category"], r["ItemSize"],r["Condition"], fmt_price(r["Price"], r["ListingType"])))
                    if not rows:
                            self.tree.insert("", "end", values=("(nothing available right now)," "", "", "",))
                    

    def reserve(self):
                selected = self.tree.selection()
                if not selected or not selected[0].isdigit():
                    messagebox.showerror("Error", "Please select an item first.")
                    return 
                item = get_item(int(selected[0]))
                if item is None:
                    messagebox.showerror("Error","That item no longer exists.")
                    self.refresh()
                    return
                if item["SellerID"] ==self.user["id"]:
                        messagebox.showerror("Error", "You cant reserve your own listing.")
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

                self.frame = ui.card(root, padx=32, pady=24)
                self.frame.pack(pady=30)

                ui.accent_bar(self.frame).pack(fill="x",pady=(0,12))
                ui.title(self.frame, item["ItemsName"]).pack(pady=(0,2))
                ui.subtitle(self.frame,
                            f'{item["Category"]}  .  Size{item["ItemSize"]}  .  {item["Condition"]}').pack()
                ui.subtitle(self.frame, fmt_price(item["Price"], item["ListingType"])).pack(pady=(4,12))
                for option in PAYMENT_OPTIONS:
                    tk.Radiobutton(self.frame, text=option, value=option,
                                   variable=self.payment).pack(anchor="w")
                    ui.field_label(self.frame, "Pickup slot").pack(fill="x", pady=(10,2))
                    self.pickup=tk.StringVar(value="")
                    for slot in PICKUP_SLOTS:
                            tk.Radiobutton(self.frame,text=slot,value=slot,variable=self.pickup,
                                           bg=ui.CARD, fg=ui.TEXT,activebackground=ui.CARD,
                                           font=(ui.FONT,10)).pack(anchor="w")
                            ui.field_label(self.frame,"Pickup notes (optional)").pack(fill="x", pady=(10,2))
                            self.notes_entry = ui.entry(self.frame)
                            self.notes_entry.pack(pady=(0, 12))

                            buttons =tk.Frame(self.frame, bg=ui.CARD)
                            buttons.pack()

                ui.primary_button(buttons, "Confirm Reserve", self.confirm).pack(pady=10)
                ui.button(buttons, "Back", self.back).pack(side="left", padx=5)

        def confirm(self):
                        pickup =self.pickup.get().strip()
                        if not pickup:
                            messagebox.showerror("Error", "Please enter a pickup slot.")
                            return
                        if not reserve_item(self.item["ItemID"], self.user["id"], self.payment.get(),pickup, self.notes_entry.get().strip()):
                            messagebox.showerror("Error", "Sorry, that item is no longer available.")
                            self.back()
                            return
                        messagebox.showinfo("Reserved", "Item reserved. Check My Orders for the details.")
                        self.back()
                        return

        def back(self):
                        self.frame.destroy()
                        CatalogueScreen(self.root,self.user)