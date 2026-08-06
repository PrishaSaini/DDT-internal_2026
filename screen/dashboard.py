#This file is the mian menu shown after the uswer logs in
import tkinter as tk

class DashboardScreen:
   def __init__(self, root, user=None):
     self.root= root
     self.user = user if isinstance(user, dict) else{"id":None,"name": user, "role":""}
     name =self.user.get("name")or "User"
    
     self.frame=tk.Frame(root)
     self.frame.pack(pady=30)

     tk.Label(self.frame, text =f"Welcome, {name}!",font=("Arial",14)).pack(pady=10)
     tk.Label(self.frame,text ="Dashboard",font=("Arial",20, "bold")).pack(pady=10)
     tk.Label(self.frame,text ="You have successfully logged in",).pack(pady=10)
     tk.Button(self.frame,text="Browse Catalogue",width=30,command=self.catalogue).pack(pady=10)
     tk.Button(self.frame,text="List an Item",width=30,command=self.list_item).pack(pady=10)
     tk.Button(self.frame,text="My Listings",width=30,command=self.my_listings).pack(pady=10)
     tk.Button(self.frame,text="My Orders",width=30,command=self.my_orders).pack(pady=10)
     if self.user.get("role")== "Admin":
        tk.Button(self.frame,  text="Admin Dashboard", width=20, command=self.admin).pack(pady=4)
        tk.Button(self.frame,text="Logout" ,command=self.logout,).pack(pady=20)


   def _go(self,screen_cls):
       self.frame.destroy()
       screen_cls(self.root, self.user)
   def catalogue(self):
      from screen.catalouge import CatalogueScreen
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

    