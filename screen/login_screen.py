#This file is for screen allwoing users to login to prgram
import tkinter as tk
from tkinter import messagebox
from database.db_connection import get_connection
from screen import ui
from helper import verify_password



class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#F0F5F6")
# frame groups all login together
        self.frame = ui.card(root)
        self.frame.pack(pady=50)
        self.frame.configure(width=450, height=450)
        self.frame.pack_propagate(False)

        tk.Label(self.frame, text="Macleans SecondHand Shop", font=("Arial", 15, "bold"), bg="white", fg="navy").pack(pady=15)
        tk.Label(self.frame, text="Email").pack() 
        self.email_entry = tk.Entry(self.frame, font=("Arial", 14),width=20)
        self.email_entry.pack()
        
        tk.Label(self.frame, text="Password").pack() 
        self.password_entry = tk.Entry(self.frame, show="*" ,font=("Arial", 14),width=20)
        self.password_entry.pack()

        tk.Button(self.frame, text="Login", command=self.login,  font=("Arial", 11), bg="#0B2E59", fg="white" ,width=20, height=1, relief="flat", bd=0).pack(pady=(15,10))
        tk.Button(self.frame, text="Create account", command=self.go_to_signup, font=("Arial", 11),  bg="#0B2E59", fg="white" ,width=20, height=1, relief="flat", bd=0).pack(pady=(15,10))
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

                         self.frame.destroy()
                         from screen.dashboard import DashboardScreen
                         DashboardScreen(self.root, current_user)
                    else:
                         messagebox.showerror("Login Failed", "Invalid email or password.")
                        
            except Exception as e:
                 messagebox.showerror("Error", f"Login failed: {e}")

            finally:
                 conn.close()

#Changes login screen to signup SCreen
            
    def go_to_signup(self):
         self.frame.destroy()
         from screen.signup_screen import SignupScreen
         SignupScreen(self.root)


                     
