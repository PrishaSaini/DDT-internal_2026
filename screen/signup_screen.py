import tkinter as tk
from tkinter import messagebox
from helper import is_valid_email
from database.db_connection import get_connection



class SignupScreen:

    def __init__(self, root):
        self.root = root

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Sign Up", font=("Arial", 18, "bold")).pack(pady=(0,20))
        tk.Label(self.frame, text="First Name").pack()
        self.first_name_entry = tk.Entry(self.frame, width=30)
        self.first_name_entry.pack(pady=10)

        tk.Label(self.frame, text="Last Name").pack()
        self.last_name_entry = tk.Entry(self.frame, width=30)
        self.last_name_entry.pack(pady=10)

        tk.Label(self.frame, text="School Email").pack()
        self.email_entry = tk.Entry(self.frame, width=30)
        self.email_entry.pack(pady=10)

        tk.Label(self.frame, text="Password").pack()
        self.password_entry = tk.Entry(self.frame, width=30, show="*")
        self.password_entry.pack(pady=10)

        tk.Label(self.frame, text="Phone Number").pack()
        self.phone_number_entry = tk.Entry(self.frame, width=30)
        self.phone_number_entry.pack(pady=10)

        tk.Button(self.frame, text="Create Account", command=self.signup).pack(pady=20)
        tk.Button(self.frame, text="Back to Login", command=self.go_to_login).pack(pady=20)

        

    def signup(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip().lower()
        password = self.password_entry.get()
        phone = self.phone_number_entry.get().strip()
    
        if not first_name or not last_name or not email or not password:
            messagebox.showerror(
            "Error",  
            "Please fill in all required fields."
             )

            return
    
        if not is_valid_email(email):
            messagebox.showerror("Error", "Please enter a valid school email address")
            return
        if len(password) <6:
            messagebox.showerror(
                "Error",
                "passowrd must contain at leats 6 characters."
            )
            return
        if phone and not phone.isdigit():
            messagebox.showerror(
                "Error",
                "Phone number must contain digits only."
            )
            return
        conn = None
        cursor = None
        try:
            conn=get_connection()

            if conn is None:
                messagebox.showerror("Error", "Couldn't connect to Database")
                return
    
            cursor = conn.cursor()

            cursor.execute(
                "SELECT UserID FROM Users WHERE SchoolEmail =?",(email,)
            )

            if cursor.fetchone():
                messagebox.showerror(
                    "Error",
                    "An account with this email already exists."
                )
                return
            insert_query="""
                    INSERT INTO Users (FirstName, LastName, SchoolEmail, [Password], PhoneNumber, Role, AccountStatus)
                    VALUES 
                (?, ?, ?, ?, ?, ?, ?)
                """
            cursor.execute(
                insert_query, 
                (first_name,
                last_name,
                email,
                password,
                 phone or None,
                 "Student",
                 "Active")
            )

            conn.commit()
            messagebox.showinfo(
                "Success",
                "Your account was created created succesfully."
        )
            self.go_to_login()
        except Exception as error:
            if conn is not None:
             conn.rollback()
            messagebox.showerror(
        "Database Error",
        f"Could not create the accound.\n\n{error}"
        )
        finally:
            if cursor is not None:
                cursor.close()

        if conn is not None:
            conn.close()

    def go_to_login(self):
        from screen.login_screen import LoginScreen

        self.frame.destroy()
        LoginScreen(self.root)

        

 