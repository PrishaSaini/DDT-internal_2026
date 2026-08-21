# This file is the mian menu shown after the uswer logs in
import tkinter as tk
from screen import ui


class DashboardScreen:
    def __init__(self, root, user=None):
        self.root = root
        self.user = user if isinstance(user, dict) else {
            "id": None, "name": user, "role": ""}
        name = self.user.get("name") or "User"
        role = self.user.get("role") or "Student"

        self.frame = ui.card(root, padx=36, pady=28)
        self.frame.pack(pady=40)

        ui.accent_bar(self.frame).pack(fill="x", pady=(0, 14))
        ui.logo(self.frame, "♻").pack()

        ui.subtitle(self.frame, text=f"Welcome, {name}  .  {role}!").pack()
        ui.title(self.frame, text="Dashboard").pack()
        tk.Label(self.frame,
                 text="You have successfully logged in",).pack(pady=10)
        ui.primary_button(self.frame, "Browse Catalogue",
                          self.catalogue).pack(pady=(5,30))
        ui.button(self.frame, "List an Item", self.list_item).pack(pady=4, fill="x")
        ui.button(self.frame, "My Listings", self.my_listings).pack(pady=4, fill="x")
        ui.button(self.frame, "My Orders", self.my_orders).pack(pady=4, fill="x")
        if self.user.get("role") == "Admin":
            ui.button(self.frame,  text="Admin Dashboard",
                      command=self.admin).pack(pady=4, fill="x")
        ui.button(self.frame, text="Logout",
                  command=self.logout,).pack(pady=(30, 0))

    def _go(self, screen_cls):
        self.frame.destroy()
        screen_cls(self.root, self.user)

    def catalogue(self):
        from screen.catalogue import CatalogueScreen
        self._go(CatalogueScreen)

    def list_item(self):
        from screen.list_item import ListItemScreen
        self._go(ListItemScreen)

    def my_orders(self):
        from screen.tables import MyOrdersScreen
        self._go(MyOrdersScreen)

    def my_listings(self):
        from screen.tables import MyListingsScreen
        self._go(MyListingsScreen)

    def admin(self):
        from screen.tables import AdminScreen
        self._go(AdminScreen)

    def logout(self):
        self.frame.destroy()
        from screen.login_screen import LoginScreen
        LoginScreen(self.root)
