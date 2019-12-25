# from tkinter import *
import tkinter as tk
from   tkinter import ttk

root = tk.Tk()
root.title("Tk dropdown example")

# Add a grid
mainframe = ttk.Frame(root)
mainframe.grid(row=0, column=0, sticky='NWES' )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)

# Create a Tkinter variable
tkvar = tk.StringVar(root)

# Dictionary with options
choices = { 'Pizza','Lasagne','Fries','Fish','Potatoe'}
tkvar.set('Pizza') # set the default option

popupMenu = tk.OptionMenu(mainframe, tkvar, *choices)
tk.Label(mainframe, text="Choose a dish").grid(row = 0, column = 1)
popupMenu.grid(row = 1, column =1)

# on change dropdown value
def change_dropdown(*args):
    print( tkvar.get() )

# link function to change dropdown
tkvar.trace('w', change_dropdown)

root.mainloop()