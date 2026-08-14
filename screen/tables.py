import tkinter as tk
from tkinter import ttk, messagebox

from database.item_db import(my_listings,
                              my_orders,
                              all_orders, 
                              set_item_status,
                              all_items, 
                              all_users, 
                              set_account_status, 
                              set_order_status
                             )
from helper import fmt_price, status_counts
from screen import ui

ITEM_STATUSES =(
    "pending",
    "active", 
    "reserved",
    "sold",
    "rejected",
    "all"
    )

def _table(parent, headings, rows, widths, iids=None, empty=""):
    tree =ui.table(parent, headings, widths)
    if not rows and empty:
        tree.insert(
            "", 
            "end",
            values=(empty,)+("",)*(len(headings)-1)
        )
    for h, w in zip(headings, widths):
        tree.heading(h, text=h)
        tree.column(h, width=w)
    for i, r in enumerate(rows):
        tree.insert("", "end", iid=(str(iids[i]) if iids else None ),values=r)
    tree.pack(pady=8)
    return tree
def _selected_id(tree):
    selected = tree.selection()
    return int(selected[0] )if selected and selected[0].isdigit()else None


class _BaseScreen:
    title="" 

    def __init__(self,root,user):
        self.root = root
        self.frame = ui.card(root, padx=24, pady =20)
        self.user = user
        self.frame.pack(pady=20)
        ui.accent_bar(self.frame).pack(fill="x", pady=(0,12))
        ui.title(self.frame, self.title).pack(pady=(0,12))
        self.body()
        row = tk.Frame(self.frame, bg=ui.CARD)
        row.pack(pady=(12,0))

        ui.button(
            row, 
            "Back to Dashboard",
            self.back
        ).pack(side="left", padx=5)

        ui.button(
            row,
            "Logout",
            self.logout
        ).pack(side="left", padx=5)

    def logout(self):
        self.frame.destroy()
        from screen.login_screen import LoginScreen
        LoginScreen(self.root)

    def body(self):
        raise NotImplementedError

    def back(self):
        self.frame.destroy()
        from screen.dashboard import DashboardScreen
        DashboardScreen(self.root, self.user)


class MyListingsScreen(_BaseScreen):
    title="My Listings"

    def body(self):
      listings = my_listings(self.user["id"])

      ui.muted_label(
          self.frame,
          status_counts(
              [
              r["Status"] for r in listings],
              ("pending", "active", "reserved", "sold", "rejected")
              ).pack(pady=(0,10)))
      rows = [
          (
              r["itemsName"],
              r["Category"],
              r["ItemSize"],
              r["Condition"],
              fmt_price(r["Price"], r["ListingType"]),
              r["Status"]
          )
          for r in listings
      ]
      _table(
          self.frame,
          ("Item", "category", "Size", "Condition", "Price", "Status"),
          rows,
          (160, 100, 60, 100, 80, 90),
          empty="(you haven't listed anything yet)"
      )
    
class MyOrdersScreen(_BaseScreen):
    title ="My Orders"

    def body(self):
      self.orders = my_orders(self.user["id"])

      ui.muted_label(
          self.frame, 
          status_counts(
              [r["Status"] for r in self.orders],
              ("reserved", "ready", "collected", "cancelled")
          )
      ).pack(pady=(0,10))

      rows=[
          (
           r["OrderID"],
           r["itemsize"],
           r["Status"],
           r["Pickup"],
           r["Payment"],
           r["PickupNotes"] or "",
           fmt_price(r["Price"])
          )
      
      for r in self.orders
      ]

      self.tree =_table(
          self.frame, 
          ("Orders # ", "Item", " Status", "Pickup", "Payment", "Notes", "Price"),
          rows, 
          (60, 150, 80, 90, 110, 110, 70),
          iids =[r["OrderID"] for r in self.orders],
          empty ="(no orders yet)"
      )

      ui.primary_button(
          self.frame,
          "Cancel Reservation",
          self.cancel
      ).pack(pady=(4,0))

    def cancel(self):
        order_id = _selected_id(self.tree)
        order = next(
              (o for o in self.orders if o["OrderID"] == order_id),
              None
          )
        if order is None:
            messagebox.showerror(
                "Error",
                "Please select an order first."
            )
            return
        if order ["Status"]!= "reserved":
            messagebox.showerror(
                "Error",
                "Only reserved orders can be cancelled"
            )
            return
        if not messagebox.askyesno(
            "Cancel",
            f'Cancel your reservation for {order["itemsName"]}?'
        ):
            return
        if not set_order_status(
            order["OrderID"],
            "cancelled",
            buyer_id=self.user["id"]
        ):
            messagebox.showerror(
                "Error",
                "That order can no longer be cancelled"
            )
            return
        messagebox.showinfo(
            "Cancelled",
            "Your reservation has been cancelled"
        )

        self.frame.destroy()
        MyOrdersScreen(self.root, self.user)
class AdminScreen(_BaseScreen):
    title= "Admin Dashboard"

    def __init__(self, root, user, item_filter="all"):
        self._wanted = item_filter
        super().__init__(root,user)

    def body(self):
        notebook = ttk.Notebook(self.frame)
        notebook.pack()
        self._items_tab(self._tab(notebook, "Items"))
        self._orders_tab(self._tab(notebook, "Orders"))
        self._users_tab(self._tab(notebook, "Users"))

    def _tab(self, notebook, text):
        tab = tk.Frame(
            notebook,
            bg=ui.CARD,
            padx=10,
            pady=10
        )
        notebook.add(tab, text=text)
        return tab
    def _reload(self):
        self.frame.destroy()
        AdminScreen(self.root, self.user, self._wanted)

    def _items_tab(self, tab):
            items = all_items()
            top = tk.Frame(tab, bg=ui.CARD)
            top.pack(fill="x")

            ui.muted_label(top, "Show").pack(side="left")

            self.item_filter = ttk.Combobox(
                top, 
                values=ITEM_STATUSES,
                state="readonly",
                width=10
            )
            self.item_filter.set(self._wanted)
            self.item_filter.pack(side="left", padx=6)

            self.item_filter.bind(
                "<<ComboboxSelected>>",
                lambda e: self._refilter()
            )

            ui.muted_label(
                top,
                status_counts(
                    [r["Status"] for r in items],
                    ("pending", "active", "reserved", "sold", "rejected"))
                ).pack(side="left, padx=10")
            shown = (
                    items
                    if self._wanted == "all"
                    else [r for r in items if r["Status"]== self._wanted]
                )
            rows = [
                    (
                                   r["itemsName"],
                                   r["Category"],
                                   r["Condition"],
                                   r["ListingType"],
                                   r["Status"],
                                   fmt_price(r["Price"], r["ListingType"])
                    )
                    for r in shown
                ]
            
            self.items_tree = _table(
                tab, 
                ("Item", "Category", "Condition", "Price", "Type", "Status"),
                rows, 
                (160, 100, 100, 80, 80 ,85),
            
            iids=[r["ItemID"] for r in shown],
            empty="(nothing with this status)"
            )
            buttons = tk.Frame(tab, bg=ui.CARD)
            buttons.pack(pady=4)
            ui.primary_button(
            buttons, 
            "Approve",
            lambda:self.decide("active")
        ).pack(side="left", padx=4)
            ui.button(
            buttons, 
            "Reject",
            lambda: self.decide("rejected")
        ).pack(side="left", padx=4)

    def _refilter(self):
        wanted = self.item_filter.get()

        self.frame.destroy()
        AdminScreen(
            self.root, 
            self.user,
            wanted
        )
             
    def decide(self,status):
        item_id = _selected_id(self.items_tree)

        if  item_id is None:
            messagebox.showerror("Error", "Please select an item first")
            return
        if status == "rejected" and not messagebox.askyesno(
            "Reject", 
            "Reject this listing?"
        ):
            if not set_item_status(item_id, status):
                messagebox.showerror("Error", "That item has already been decided.")
            return
        messagebox.showinfo("Done",f"Item marked{status}.")
        self._reload()

    def _orders_tab(self, tab):
        orders = all_orders()
        ui.muted_label(
            tab, 
            status_counts(
                [r["Status"] for r in orders],
                ("reserved", "ready", "collected", "cancelled")
            )
        ).pack(anchor="w")

        rows = [(
             r["OrderID"],
                       r["itemsize"],
                       r["Status"],
                       r["Pickup"],
                       r["Payment"],
                       r["PickupNotes"] or ""
        )
                       for r in orders

        ]
        self.orders_tree = _table(
        tab, 
        ("Order #", "Item", "Status", "Pickup", "Payment", "Buyer", "Notes"),
        rows,
        (60, 140, 80, 90, 100, 90, 100),
        iids=[r["OrderID"] for r in orders],
        empty="(no orders yet)"
    )
        buttons = tk.Frame(tab, bg= ui.CARD)
        buttons.pack(pady=4)
        ui.primary_button(
        buttons,
            "Mark Ready",
                lambda: self.advance("ready")    
    ).pack(side="left", padx=4)
        ui.button(
        buttons,
        "Cancel Order", lambda: self.advance("cancelled")
    ).pack(side="left", padx=4)
        ui.button(
        buttons,
        "Mark Collected", 
        lambda: self.advance("collected")
    ).pack(side="left", padx=4)

    def advance(self, status):
        order_id = _selected_id(self.orders_tree)
        if order_id is None:
            messagebox.showerror()
            return
        if status == "cancelled" and not messagebox.askyesno():
            return
        if not set_order_status(order_id, status):
            messagebox.showerror()
            return
        messagebox.showinfo()
        self._reload()

    def _users_tab(self,tab):
        users= all_users()
        rows = [
            (
            f'{r["FirstName"]}, {r["LastName"]}', 
            r["SchoolEmail"],
            r["Role"],
            r["AccountStatus"]
            )
            for r in users
        ]

        self.users_tree = _table(tab, 
                                 ("Name", "Email", "Role", "Status"),
                                 rows,
                                 (140, 190, 80, 90),
                                 iids=[r["UserID"] for r in users],
                                 empty="(no users)"
                                 )
        buttons = tk.Frame(tab, bg=ui.CARD)
        buttons.pack(pady=4)
        ui.primary_button(
            buttons,
            "Enable",
            lambda: self.set_users("Active")
            ).pack(side="left", padx=4)
        ui.button(
            buttons,
            "Disable",
            lambda: self.set_user("Disabled")
            ).pack(side="left", padx=4)

def set_user(self, status):
    user_id = _selected_id(self.users_tree)

    if user_id is None:
        messagebox.showerror()
        return

    if status == "Disabled" and not messagebox.askyesno():
        return

    set_account_status(user_id, status)
    messagebox.showinfo()
    self.reload()
       
        

                                                