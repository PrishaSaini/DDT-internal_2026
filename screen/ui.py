import tkinter as tk
from tkinter import ttk

BG = "#eef1f6"
CARD = "#ffffff"
PRIMARY = "#2563eb"
PRIMARY_DK="#1d4ed8"
PRIMARY_LT="#eaf1ff"
TEXT ="#111827"
MUTED = "#6b7280"
BORDER = "#d5dbe6"
FIELD ="#f7f9fc"

FONT = "Arial"

def setup (root):
    """Apply the theme to the root window. Call once"""
    root.configure(bg=BG)
    style = ttk.Style(root)

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("Primary.TButton", font =(FONT,11, "bold"),
                    background=PRIMARY, foreground="white", padding=(14,12), borderwidth=0, focuscolor=PRIMARY
                    )
    style.map("Primary.TButton", background=[("active", PRIMARY_DK), ("pressed",PRIMARY_DK)])

    style.configure("Secondary.TButton", font =(FONT,10, "bold"),
                    background=CARD, foreground="PRIMARY", padding=(14,11), borderwidth=1, focuscolor=CARD
                    )
    
    style.map("Secondary.TButton", background=[("active", PRIMARY_DK), ("pressed",PRIMARY_DK)])

    style.configure("TEntry", font =(FONT,10, "bold"),
                    background=CARD, foreground="PRIMARY", padding=8, borderwidth=1, focuscolor=CARD
                    )
    style.configure("TCombobox", font =(FONT,10, "bold"),
                    background=CARD, foreground="PRIMARY", padding=(14,11), borderwidth=1, focuscolor=CARD
                    )
    
    style.configure("TNotebook", background=CARD, borderwidth=0)
    style.configure("TNotebook.tab", font=(FONT, 10, "bold"), padding=(16,8),
                    background=BG, foreground=MUTED, borderwidth=0),
    style.map("TNotebook.Tab",background=[("selected", CARD)],
     foreground=[("selected", PRIMARY)])
