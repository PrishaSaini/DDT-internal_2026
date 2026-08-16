"""Login screen, shown when the program starts."""
import tkinter as tk
from tkinter import messagebox
from database.db_connection import get_connection
from screen import ui
from helper import verify_password, hash_password
from database.item_db import ACCOUNT_ACTIVE



class LoginScreen:
    """logs a user in and opens the dashboard."""
    def __init__(self, root):
        self.root = root
       
        self.frame = ui.card(root)
        self.frame.pack(pady=50)
       
        ui.accent_bar(self.frame).pack( fill="x", pady=(0,15))
        ui.logo(self.frame,"♻" ).pack()
        ui.title(self.frame, "Macleans Second Hand Shop").pack()
        ui.subtitle(self.frame, "Sign in to continue").pack(pady=(2,18))

        ui.field_label(self.frame, text="Email").pack(fill="x") 
        self.email_entry = ui.entry(self.frame)
        self.email_entry.pack(pady=(2,10))

        ui.field_label(self.frame, text="Password").pack(fill="x") 
        self.password_entry = ui.entry(self.frame, show="*")
        self.password_entry.pack(pady=(2,18))
      

        ui.primary_button(self.frame, "Login", self.login).pack()
        ui.button(
             self.frame,
             "Go to Sign Up",
             self.go_to_signup
        ).pack(pady=(8,0))
        
    def login(self):
            """Check the details and open the dashboard if they are right.
            The wd is checked in Python, never  inside the SQL and a wrong pwd 
            gives the same message as an unknown email."""
            email = self.email_entry.get().strip()
            password = self.password_entry.get()
            if not email or not password:
                messagebox.showerror("Error","Enter email and password please")
                return
            # none menas the databse won't open
            conn = get_connection()
            if conn is None:
                messagebox.showerror("Database Error", "Could not connect to Databse.")
                return
            current_user=None
          
            try: 
                    cursor = conn.cursor()
                    sql="""
                    SELECT * FROM Users
                    WHERE SchoolEmail = ? AND AccountStatus =?
                    """
                    cursor.execute (sql, (email,ACCOUNT_ACTIVE))
                    user = cursor.fetchone ()
                    if user and verify_password(password, user["Password"]):
                          if ":" not in (user["Password"] or ""):
                                          cursor.execute(
                                               "UPDATE Users SET Password = ? WHERE UserID = ?", 
                                               (
                                                    hash_password(password),
                                                    user["UserID"]
                                               )
                                          )
                                          conn.commit()
                          current_user ={
                                                 "id": user["UserID"],
                                                 "name": user["FirstName"],
                                                 "role": user["Role"],
                         }
                    else:
                         messagebox.showerror("Login Failed", "Invalid email or password.")
            except Exception as e:
               messagebox.showerror("Error", f"Login failed: {e}")
               return
            finally:
               conn.close()
               # outside teh try so a dashboard error is not called a login failure.
            if current_user:
                    self.frame.destroy()
                    from screen.dashboard import DashboardScreen
                    DashboardScreen(self.root, current_user)

            
    def go_to_signup(self):
         """Goes to the signup form"""
         self.frame.destroy()
         from screen.signup_screen import SignupScreen
         SignupScreen(self.root)


                     
