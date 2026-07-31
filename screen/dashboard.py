import tkinter as tk

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
       text="Logout" ,
       command=self.logout,
    ).pack(pady=20)

    def logout(self):
        self.frame.destroy()
        from screen.login_screen import LoginScreen
        LoginScreen(self.root)