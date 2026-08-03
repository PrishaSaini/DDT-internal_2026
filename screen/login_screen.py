#This file is for screen allwoing users to login to prgram
import tkinter as tk
from tkinter import messagebox
from database.db_connection import get_connection


class LoginScreen:
    def __init__(self, root):
        self.root = root
# frame groups all login together
        self.frame = tk.Frame(root) 
        self.frame.pack(pady=50)

        tk.Label(self.frame, text="Login", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(self.frame, text="Email").pack() 
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack()
        
        tk.Label(self.frame, text="Password").pack() 
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()

        tk.Button(self.frame, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.frame, text="Go to Sign Up", command=self.go_to_signup).pack(pady=5)

   #This is for login and checks details against the database account"""
    def login(self):
            email = self.email_entry.get()
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
                    WHERE SchoolEmail = ? AND [Password]= ? AND AccountStatus =?
                    """
                    cursor.execute (sql, email, password, "Active")
                    user = cursor.fetchone ()

                    if user:
                         current_user ={
                              "id": user["UserID"],
                              "name": user.FirstName,
                              "role": user.Role
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


                     
