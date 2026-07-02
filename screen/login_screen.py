import tkinter as tk
from tkinter import messagebox

class LoginScreen:
    def __init__(self, root):
        self.root = root

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

        def login(self):
            email = self.email_entry.get()
            password = self.password_entry.get()
            if not email or not password:
                messagebox.showerror("Error")
                return