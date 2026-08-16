"""Macleans Reuse Hub - a second-hand shop for school uniform, stationary etc
Run it with: python main.py
"""

import tkinter as tk
from screen import ui

from screen.login_screen import LoginScreen
def main():
    """Open the windown and show the login screen"""
    root=tk.Tk()
    root.title("Macleans Reuse Hub")
    root.geometry("720x700")
    # Theme must be set before any screen is built
    ui.setup(root)
    LoginScreen(root)
    # Hand it over to tkinter which now waits for user input
    root.mainloop()

if __name__ =="__main__":
    main()

