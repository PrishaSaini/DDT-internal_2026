import tkinter as tk

from screen.login_screen import LoginScreen
def main():
    root=tk.Tk()
    root.title("Macleans Reuse Hub")
    root.geometry("600x600")
    LoginScreen(root)
    root.mainloop()

if __name__ =="__main__":
    main()

