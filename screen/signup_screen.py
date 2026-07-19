import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from helper import *
from db_connection import *
fom ui import *


class SignupScreen:

    def __init__(self, root):
        self.root = root

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Sign Up", font=("Arial", 18, "bold"))
        tk.Label(self.frame, text="First Name").pack()
        self.first_name_entry = tk.Entry(self.frame, width=30)
        self.first_name_entry.pack(pady=10)

        tk.Label(self.frame, text="First Name").pack()
        self.first_name_entry = tk.Entry(self.frame, width=30)
        self.first_name_entry.pack(pady=10)

        tk.Label(self.frame, text="School Email").pack()
        self.first_name_entry = tk.Entry(self.frame, width=30)
        self.first_name_entry.pack(pady=10)

        tk.Label(self.frame, text="Password").pack()
        self.first_name_entry = tk.Entry(self.frame, width=30)
        self.first_name_entry.pack(pady=10)

        tk.Label(self.frame, text="Phone Number").pack()
        self.first_name_entry = tk.Entry(self.frame, width=30)
        self.first_name_entry.pack(pady=10)

        tk.Button(self.frame, text="Create Account", command=self.signup).pack(pady=20)
        tk.Button(self.frame, text="Back to Login", command=self.go_to_login).pack(pady=20)

    def signup(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.fpassword_entry.get().strip()
        phone = self.phone_entry.get().strip()
    
        if not first_name or not last_name or not email or not password:
            messagebox.showerror("Error", "Please fill in all required fields.")

        return
    
    if not is_valid_email(email):
        messagebox.shoerror("Error", "Please enter a valid school email address")

        return
    conn = get_connection()

    if conn is None:
        messagebox.shoerror("Error", "Couldn't connect to Database")
        return
try:
    cursor = conn.cursors()

        

 