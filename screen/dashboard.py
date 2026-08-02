#This file is the mian menu shown after the uswer logs in
import tkinter as tk
from tkinter import messagebox 

class DashboardScreen:
    def __init__(self, root, user=None):
     self.root= root
     name =(user or {}).get("name","User")if isinstance(user, dict)else user
    
     self.frame=tk.Frame(root)
     self.frame.pack(pady=50)
     tk.Label(
        self.frame, 
        text =f"Welcome, {name}!",
        font=("Arial",14)
       ).pack(pady=10)
     tk.Label(
        self.frame, 
        text ="Dashboard",
        font=("Arial",20, "bold")
       ).pack(pady=10)
     tk.Label(
        self.frame, 
        text ="You have successfully logged in",
       ).pack(pady=10)
     
     tk.Button(
        self.frame,
        text="Browse Catalogue",
        width=30,
        command=self.not_connected
     ).pack(pady=10)

     tk.Button(
             self.frame,
             text="List an Item",
             width=30,
             command=self.not_connected
          ).pack(pady=10)
     
     tk.Button(
             self.frame,
             text="My Listings",
             width=30,
             command=self.not_connected
          ).pack(pady=10)

     tk.Button(
          self.frame,
          text="My Orders",
          width=30,
          command=self.not_connected
          ).pack(pady=10)
     

     tk.Button(
       self.frame, 
       text="Logout" ,
       command=self.logout,
    ).pack(pady=20)

    def not_connected(self):
       messagebox.showinfo("Not connected to other pages yet", "Not connected yet" )

    def logout(self):
        self.frame.destroy()
        from screen.login_screen import LoginScreen
        LoginScreen(self.root)

    