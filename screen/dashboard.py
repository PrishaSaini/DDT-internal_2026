import tkinter as tk

class DashboardScreen:
    def __init__(self, root, user_name="User"):
     self.root= root
    
     self.frame=tk.Frame(root)
     self.frame.pack(pady=50)
    
    tk.Label(
        self.frame, 
        text =f"Wecome, {user_name}!",
        font=("Arial",14)
       ).pack(pady=10)
    
    tk.Label(
        self.frame, 
        text ="DashBoard",
        font=("Arial",20, "bold")
       ).pack(pady=10)
    
    tk.Label(
        self.frame, 
        text ="You have succesfully logged in",
       ).pack(pady=10)
    
    tk.Button (
       self-frame, 
       text-'Logout'
       command=self.logout
    ).pack(pady=20)

    def logout(self):
        self.frame.destroy()