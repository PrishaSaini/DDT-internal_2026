#This file is for screen allwoing users to login to prgram
import tkinter as tk
from tkinter import messagebox
from database.db_connection import get_connection
from screen import ui
from helper import verify_password, hash_password



class LoginScreen:
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
        self.email_entry = ui.entry(self.frame, show="*")
        self.email_entry.pack(pady=(2,18))
      

        ui.primary_button(self.frame, "Login", self.login).pack()
        ui.button(
             self.frame,
             "Go to Sign Up",
             self.go_to_signup
        ).pack(pady=(8,0))
        
    def login(self):
            email = self.email_entry.get().strip()
            password = self.password_entry.get()
            if not email or not password:
                messagebox.showerror("Error","Enter email and password please")
                return
            
            conn = get_connection()
            if conn is None:
                messagebox.showerror("Database Error", "Could not connect to Databse.")
                return
            current_user=None
            if ":" not in (user["Passowrd"] or ""):
                 cursor.execute(
                      "UPDATE Users SET Password = ? WHERE UserID = ?", 
                      (
                           hash_password(password),
                           user["UserID"]
                      )
                 )
                 conn.commit()
            try: 
                    cursor = conn.cursor()
                    sql="""
                    SELECT * FROM Users
                    WHERE SchoolEmail = ? AND AccountStatus =?
                    """
                    cursor.execute (sql, (email, "Active"))
                    user = cursor.fetchone ()

                    if user and verify_password(password, user["Password"]):
                         current_user ={
                              "id": user["UserID"],
                              "name": user["FirstName"],
                              "role": user["Role"],
                         }

                         
                    else:
                         messagebox.showerror("Login Failed", "Invalid email or password.")
                        
            except Exception as e:
                 messagebox.showerror("Error", f"Login failed: {e}")

            finally:
                 conn.close()
                 if current_user:
                      self.frame.destroy()
                      from screen.dashboard import DashboardScreen
                      DashboardScreen(self.root, current_user)

#Changes login screen to signup SCreen
            
    def go_to_signup(self):
         self.frame.destroy()
         from screen.signup_screen import SignupScreen
         SignupScreen(self.root)


                     
