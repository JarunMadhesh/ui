
# Implementation of Collapsible Pane container

# importing tkinter and ttk modules
import time
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

def print1():
    time.sleep(5)
    print(1)

def print2():
    time.sleep(10)
    print(2)


class CollapsiblePane(ttk.Frame):
    """
     -----USAGE-----
    collapsiblePane = CollapsiblePane(parent,
                          expanded_text =[string],
                          collapsed_text =[string])

    collapsiblePane.pack()
    button = Button(collapsiblePane.frame).pack()
    """

    def __init__(self, parent, title):

        ttk.Frame.__init__(self, parent)

        # These are the class variable
        # see a underscore in expanded_text and _collapsed_text
        # this means these are private to class
        self.parent = parent
        self._isopen = True
        self._title = title

        s = ttk.Style()
        # Create style used by default for all Frames
        s.configure('TFrame', background='white')
        self.configure(style="TFrame")

        # Here weight implies that it can grow it's
        # size if extra space is available
        # default weight is 0
        self.columnconfigure(1, weight=1)

        # Tkinter variable storing integer value
        self._variable = tk.IntVar()

        self._label = tk.Label(self, text=self._title, background="white")
        self._label.grid(row=0, column=0, sticky="w", padx=10)

        # This will create a separator
        # A separator is a line, we can also set thickness
        self._separator = ttk.Separator(self, orient="horizontal")
        self._separator.grid(row=0, column=1, sticky="we")

        self._button = ctk.CTkButton(self, text= "↓",
                                       command=self._activate, border_width=0, width=20, height=20, corner_radius=30, fg_color="transparent", text_color="black", hover_color="white")
        self._button.grid(row=0, column=2, padx=10, pady=5)

        frame = ttk.Frame(self, height=5, width=690)
        frame.grid(row=1, columnspan=3)
        frame.configure(style="TFrame")

        self.frame = ttk.Frame(self)

        # This will call activate function of class
        self._activate()

    def _activate(self):
        self._isopen = not self._isopen
        if not self._isopen:

            # As soon as button is pressed it removes this widget
            # but is not destroyed means can be displayed again
            self.frame.grid_forget()
            # This will change the text of the checkbutton
            self._button.configure(text="↓")

        elif self._isopen:
            # increasing the frame area so new widgets+*-
            # could reside in this container
            self.frame.grid(row=2, column=0, columnspan=3)
            self._button.configure(text="↑")

