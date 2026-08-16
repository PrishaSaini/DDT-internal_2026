"""Screens that show a table: My Listings, My Orders and Admin."""
import tkinter as tk
from tkinter import ttk, messagebox

from database.item_db import(my_listings,
                              my_orders,
                              all_orders, 
                              set_item_status,
                              all_items, 
                              all_users, 
                              set_account_status, 
                              set_order_status,
                              get_item,
                              STATUS_SOLD, STATUS_REJECTED, 
                              ORDER_RESERVED, ORDER_READY, ORDER_COLLECTED, ORDER_CANCELLED,
                              ACCOUNT_ACTIVE, ACCOUNT_DISABLED, STATUS_PENDING,ITEM_STATUS_ORDER,
                              STATUS_ACTIVE, STATUS_RESERVED
                             )
from helper import fmt_price, status_counts
from screen import ui
from models.records import Item, User, Order
from models.review_queue import ReviewQueue

#The order teh statuses appera in on screen.
ITEM_STATUS_ORDER=(
    STATUS_PENDING, STATUS_ACTIVE, STATUS_RESERVED, STATUS_SOLD, STATUS_REJECTED
    )
ORDER_STATUS_ORDER = (ORDER_RESERVED, ORDER_READY, ORDER_COLLECTED, ORDER_CANCELLED)
#"all" is only a filter choice, never saved as a status.
FILTER_ALL= "all"
ITEM_STATUSES = ITEM_STATUS_ORDER +(FILTER_ALL,)

def _table(parent, headings, rows, widths, iids=None, empty=""):
    """Build a table. iids are the database ids so we know what was clicked."""
    tree =ui.table(parent, headings, widths)
    for i, r in enumerate(rows):
        tree.insert("", "end", iid=(str(iids[i]) if iids else None), values =r)
    if not rows and empty:
        #Say why the table is empty instead of shwoing nothing.
        tree.insert(
            "", 
            "end",
            values=(empty,)+("",)*(len(headings)-1)
        )
    tree.pack(pady=8)
    return tree

def _selected_id(tree):
    """Id of the clicked row, or None."""
    selected = tree.selection()
    return int(selected[0] )if selected and selected[0].isdigit()else None


class _BaseScreen:
    """Shared layout for the table screens: card, title, Back and Logout."""
    title="" 

    def __init__(self,root,user):
        """Draw the screen."""
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
        """Log out """
        self.frame.destroy()
        from screen.login_screen import LoginScreen
        LoginScreen(self.root)

    def body(self):
        """Each screen fills in its own middle part."""
        raise NotImplementedError

    def back(self):
        """Go back to the dashboard."""
        self.frame.destroy()
        from screen.dashboard import DashboardScreen
        DashboardScreen(self.root, self.user)


class MyListingsScreen(_BaseScreen):
    """Everthing thus user has listed."""
    title="My Listings"

    def body(self):
      """Shows the counts and the listing table."""
      listings = my_listings(self.user["id"])

      ui.muted_label(self.frame, status_counts(
          [r["Status"] for r in listings],
          ITEM_STATUS_ORDER)).pack(pady=(0,10))
#Turn rows into Item objects so we can write i.name instead of a key
      items = [Item.from_row(r) for r in listings]
      rows = [(i.name, i.category, i.size, i.condition, 
               fmt_price(i.price, i.listing_type), i.status) for i in items]
      _table(
          self.frame,
          ("Item", "category", "Size", "Condition", "Price", "Status"),
          rows,
          (160, 100, 60, 100, 80, 90),
          empty="(you haven't listed anything yet)"
      )
    
class MyOrdersScreen(_BaseScreen):
    """This is user's own reservations"""
    title ="My Orders"

    def body(self):
      """Show the counts, the orders table and the cancel button."""
      self.orders = my_orders(self.user["id"])
      ui.muted_label(self.frame, status_counts(
          [r["Status"] for r in self.orders],
          ORDER_STATUS_ORDER)).pack(pady=(0,10))

      rows = [(o.order_id, r["itemsname"], o.status, o.pickup,
              o.payment, o.pickup_notes or "", fmt_price(r["Price"]))
              for r, o in ((r, Order.from_row(r)) for r in self.orders)]
    

      

      self.tree =_table(
          self.frame, 
          ("Orders # ", "Item", " Status", "Pickup", "Payment", "Notes", "Price"),
          rows, 
          (60, 150, 80, 90, 110, 110, 70),
          iids =[r["OrderID"] for r in self.orders],
          empty ="(no orders yet)"
      )
      ui.primary_button(self.frame, "Cancel Reservation", self.cancel).pack(pady=(4,0))

    def cancel(self):
        """Cancel this user's reservation after asking them to confirm."""
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
    """Admin screen with three tabs: items, orders and users."""
    title= "Admin Dashboard"

    def __init__(self, root, user, item_filter="all"):
        """item_filter is set forst because body() need it."""
        self._wanted = item_filter
        super().__init__(root,user)

    def body(self):
        """Build the three tabs"""
        notebook = ttk.Notebook(self.frame)
        notebook.pack()
        self._items_tab(self._tab(notebook, "Items"))
        self._orders_tab(self._tab(notebook, "Orders"))
        self._users_tab(self._tab(notebook, "Users"))

    def _tab(self, notebook, text):
        """Add a tab and return it"""
        tab = tk.Frame(
            notebook,
            bg=ui.CARD,
            padx=10,
            pady=10
        )
        notebook.add(tab, text=text)
        return tab
    def _reload(self):
        """"""
        self.frame.destroy()
        AdminScreen(self.root, self.user, self._wanted)

    def _items_tab(self, tab):
            """Items tab: filter, counts, Approve and reject buttons """
            row_raw = all_items()
            items = [Item.from_row(r) for r in row_raw]

            self.review_queue = ReviewQueue(items)
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
            shown =items if self._wanted == FILTER_ALL else [ i for i in items if i.status == self._wanted]
            rows = [
                    (
                                   i.name,
                                   i.category,
                                   i.condition,
                                   i.listing_type,
                                   i.status,
                                   fmt_price(i.price, i.listing_type)
                    )
                    for i in shown
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

    def review_oldest(self):
        """Pick the listing that has waited the longest"""
        #Another admin may have delat with soem of these already so skip
        #any that are no longer pending
        oldest=None
        while not self.review_queue.is_empty():
            candidate = self.review_queue.peek()
            current = get_item(candidate.item_id)
            if current is not None and current["Status"] == STATUS_PENDING:
                oldest = candidate
                break
            self.review_queue.take()
            if oldest is None:
                messagebox.showinfo("All done", "No listings are wauting for reviw")
                return
            if self._wanted not in(FILTER_ALL, STATUS_PENDING):
                self.frame.destroy()
                AdminScreen(self.root, self.user, STATUS_PENDING)
                self.frame.destroy()
                AdminScreen(self.root, self.user, STATUS_PENDING).review_oldest()
                return
            self.items_tree.selection_set(str(oldest.item_id))
            self.items_tree.see(str(oldest.item_id))
                
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


    def set_user(self,status):
        user_id = _selected_id(self.users_tree)
        if user_id is None:
            messagebox.showerror()
            return
        if status == ACCOUNT_DISABLED and user_id == self.user["id"]:
            messagebox.showerror()
            return
        if status == ACCOUNT_DISABLED and not messagebox.askyesno():
            return
        set_account_status(user_id, status)
        messagebox.showinfo()
        self._reload()