#This file shows screeb which collects and chgecls the information for signup of an account
import tkinter as tk
from tkinter import messagebox
from helper import is_valid_email, hash_password, MIN_PASSWORD_LEN
from database.db_connection import get_connection
from datetime import datetime
from screen import ui



class SignupScreen:

    def __init__(self, root):
        self.root = root
        self.frame = ui.card(root, padx=32, pady=24)
        self.frame.pack(pady=20)

        ui.accent_bar(self.frame.pack(fill="x", pady=(0,12)))
        ui.title(self.frame, "Sign Up").pack()
        ui.subtitle(self.frame, "Create yout student account").pack(pady=(2,14))

        self.first_name_entry = self._field("First Name")
        self.last_name_entry = self._field("Last Name")
        self.email_entry = self._field("School Email")
        self.password_enrty = self._field("Password", show ="*")
        self.phone_entry = self._field("Fhone Number")
    def _field(self, label, show=None):
        ui.field_label(self.frame, label).pack(fill="x")
        e=ui.entry(self.frame, show=show)
        e.pack(pady=(2,8))

        ui.primary_button(
            self.frame, 
            "Create Account",
            self.signup
        ).pack(pady=(14,0))

        ui.button (self.frame, 
    "Back to Login",
    self.go_to_login).pack(pady=(8, 0))

        

#Collects the forms values, validates them and saves the account
    def signup(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        phone = self.phone_entry.get().strip()
    
        if not first_name or not last_name or not email or not password:
            messagebox.showerror(
            "Error",  
            "Please fill in all required fields."
             )

            return
    
        if not is_valid_email(email):
            messagebox.showerror("Error", "Please enter a valid school email address")
            return
        if len(password) <MIN_PASSWORD_LEN:
            messagebox.showerror(
                "Error",
                f"passowrd must contain at least {MIN_PASSWORD_LEN} characters"
            )
            return
        if phone and not phone.isdigit():
            messagebox.showerror(
                "Error",
                "Phone number must contain digits only."
            )
            return
        
        conn=get_connection()
        if conn is None:
            messagebox.showerror("Error", "Couldn't connect to Database")
            return
        try:
    
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
            sql ="""
                    INSERT INTO Users (FirstName, LastName, SchoolEmail, Password, PhoneNumber, Role, AccountStatus, DateCreated)
                    VALUES 
                (?, ?, ?, ?, ?, ?, ?,?)
                """
            cursor.execute(
                sql, 
                (first_name,
                last_name,
                email,
               hash_password(password),
                 phone,
                 "Student",
                 "Active",
                 datetime.now().isoformat(" ", "seconds"))
            )

            conn.commit()
            messagebox.showinfo(
                "Success",
                "Your account was created created succesfully."
        )
            self.go_to_login()
        except Exception as e:
            messagebox.showerror(
        "Database Error",
        f"Signup fauiled {e}"
        )
        finally:
                conn.close()

        
#Return back to login screen
    def go_to_login(self):

        self.frame.destroy()
        from screen.login_screen import LoginScreen
        LoginScreen(self.root)

        

 