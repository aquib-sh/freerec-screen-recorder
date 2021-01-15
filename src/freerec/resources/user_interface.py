from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

class Application(Tk):
    def __init__(self, size):
        super().__init__()
        self.geometry(size)
        self.resizable(False, False)
    
    def get_root(self):
        return self

    def set_title(self, title):
        self.title(title)

    def set_icon(self, path):
        self.iconbitmap(False, path)

    def add_button(self, value, row_, column_, command_=None): 
        button = ttk.Button(self, text=value, command=command_)
        button.grid(row=row_, column=column_)
        return button
    
    def add_label(self, value, row_, column_):
        lbl = Label(text=value)       
        lbl.grid(row=row_, column=column_)
 
    def add_check_box(self, value, row_, column_):
        var = IntVar()
        chk_box = Checkbutton(self, text=value, 
            variable=var)
        chk_box.grid(row=row_, column=column_) 
        return var

    def start(self):
        self.mainloop()

