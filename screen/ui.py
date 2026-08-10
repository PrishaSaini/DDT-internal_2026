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
                    background=CARD, foreground=PRIMARY, padding=(14,11), borderwidth=1, focuscolor=CARD
                    )
    
    style.map("Secondary.TButton", background=[("active", PRIMARY_LT), ("pressed",PRIMARY_LT)])

    style.configure("TEntry", font =(FONT,10),
                    fieldbackground=CARD, foreground=TEXT, padding=8, borderwidth=1, focuscolor=CARD
                    )
    style.configure("TCombobox", font =(FONT,10),
                    fieldbackground=FIELD, foreground=TEXT, padding=(14,11), borderwidth=1, focuscolor=CARD
                    )
    
    style.configure("TNotebook", background=CARD, borderwidth=0)
    style.configure("TNotebook.Tab", font=(FONT, 10, "bold"), padding=(16,8),
                    background=BG, foreground=MUTED, borderwidth=0)
    style.map("TNotebook.Tab",background=[("selected", CARD)],
     foreground=[("selected", PRIMARY)])
    style.configure("Treeview", 
                    background=CARD,
                    fieldbackground=CARD,
                    foreground=TEXT,
                    font=(FONT,10),
                    rowheight=26,
                    bordercolor=BORDER,
                    lightcolor=BORDER,
                    darkcolor=BORDER)
    style.configure("Treeview.Heading",
                    font=(FONT, 10, "bold"),
                    background=FIELD,
                    foreground=MUTED,
                    relief="flat",
                    padding=6)
    style.map("Treeview", 
              background=[("selected", PRIMARY)],
              forground=[("selected", "white")])

def card(parent, padx=40, pady=30):
     """A white panel to hold a screen's content."""
     return tk.Frame(parent, bg=CARD, padx=padx, pady=pady, highlightbackground=BORDER, highlightthickness=1)

def accent_bar(parent):
    """Thin brand-colored strip across the top of a card."""
    return tk.Frame(parent,bg=PRIMARY,height=4)

def logo(parent, emoji="placeholder"):
    return tk.Label(parent, text=emoji, bg=CARD, fg=PRIMARY, font=(FONT,30))

def title(parent, text, anchor="center"):
    return tk.Label(parent, text=text, bg=CARD, fg=TEXT, font=(FONT,22,"bold"), anchor=anchor)


def subtitle(parent, text, anchor="center"):
    return tk.Label(parent, text=text, bg=CARD, fg=MUTED, font=(FONT,11), anchor=anchor)

def field_label(parent,text):
    return tk.Label(parent, text=text, bg=CARD, fg=TEXT, font=(FONT,10,"bold"), anchor="w")


def entry(parent, show=None, width=34):
    return ttk.Entry(parent, width=34, show=show, font=(FONT,10))


def primary_button(parent, text, command):
    return ttk.Button(parent, width=34, text=text, command=command, style="Primary.TButton")


def button(parent, text, command):
    return ttk.Button(parent, width=34, text=text, command=command, style="Secondary.TButton")

def muted_label(parent, text):
    return tk.Label(parent, text=text, bg=CARD, fg= MUTED, font=(FONT,10))

def table(parent,headings,widths, height=8):
    tree=ttk.Treeview(parent, columns=headings, show="headings",height=height)
    for h, w in zip(headings,widths):
        tree.heading(h, text=h)
        tree.column(h,width=w)
        return tree