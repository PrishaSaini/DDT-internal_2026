import tkinter as tk
from screen import ui

from screen.login_screen import LoginScreen
def main():
    root=tk.Tk()
    root.title("Macleans Reuse Hub")
    root.geometry("720 x 700")
    ui.setup(root)
    LoginScreen(root)
    root.mainloop()

if __name__ =="__main__":
    main()

