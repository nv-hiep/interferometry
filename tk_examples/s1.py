#!/usr/bin/env python
import os
import sys
try:               # Python 2.7x
    import Tkinter as tk
    import ttk
    import tkFont
    import tkMessageBox
    import tkFileDialog
    import tkSimpleDialog
    from ScrolledText import ScrolledText as tkScrolledText
except Exception:  # Python 3.x
    import tkinter as tk
    from tkinter import ttk
    import tkinter.font as tkFont
    import tkinter.messagebox as tkMessageBox
    import tkinter.filedialog as tkFileDialog
    import tkinter.simpledialog as tkSimpleDialog
    from tkinter.scrolledtext import ScrolledText as tkScrolledText

import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.colors import LogNorm
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

# Webcam library
try:
    import cv2
    hasCV2 = True
except ImportError:
    hasCV2 = False

# Disable cv2 use on Mac OS because of buggy implementation
if sys.platform=="darwin":
    hasCV2 = False



class Root(tk.Tk):
    def __init__(self):
        # super(Root, self).__init__()
        self.title("Python Tkinter Dialog Widget")
        self.minsize(640, 400)
        # self.wm_iconbitmap('icon.ico')

        self.labelFrame = ttk.LabelFrame(self, text = "Open File")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)

        self.button()

        self.menubar = tk.Menu(root)
        self.filemenu = tk.Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=donothing)
        self.filemenu.add_command(label="Open", command=donothing)
        self.filemenu.add_command(label="Save", command=donothing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        self.helpmenu = tk.Menu(menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=donothing)
        self.helpmenu.add_command(label="About...", command=donothing)
        self.helpmenu.add_command(label="Instructions",
                                      command=lambda fileName="docs/HELP.txt",
                                      title="Vriendly VRI Instructions" :
                                      _show_textfile(fileName, title))
        self.menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)



    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse A File",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)



def show_textfile(fileName, title=""):
    """Show a text file in a new window."""

    helpWin = tk.Toplevel(background=bgColour)
    helpWin.title(title)
    helpTxt = tkScrolledText(helpWin, width=80,
                                  font=fontFixed)
    helpTxt.config(state="normal")
    with open(fileName,'r') as f:
        text = f.read()
    helpTxt.insert('1.0', text)
    helpTxt.config(state="disabled")
    helpTxt.grid(column=0, row=0, padx=5, pady=5, sticky="NSEW")
    closeBtn = ttk.Button(helpWin, text='Close',
                               command=helpWin.destroy)
    closeBtn.grid(column=0, row=1, padx=5, pady=5, sticky="E")
    helpWin.rowconfigure(0, weight=1)
    helpWin.columnconfigure(0, weight=1)




def donothing():
   x = 0



#-----------------------------------------------------------------------------#
# if __name__ == "__main__":
    
# root = tk.Tk()



# try fiddling with these root.geometry values
# root.title('My tkinter size experiment')
# root.minsize(width=1200, height=500)
# root.geometry('1000x920+0+0')



# Force platform specific colours and fonts
if sys.platform=="darwin":
    bgColour = "#ececec"
    fontSize = 12
else:
    bgColour = ttk.Style().lookup("TFrame", "background")
    fontSize = 10        

ttk.Style().configure("TFrame", background=bgColour)
ttk.Style().configure("TLabelframe", background=bgColour)
ttk.Style().configure("TLabel", background=bgColour)
fontDefault = tkFont.nametofont("TkDefaultFont")
fontDefault.configure(size=fontSize)
fontFixed = tkFont.nametofont("TkFixedFont")
fontFixed.configure(size=fontSize)
# root.option_add("*Font", fontDefault)

# Hack to hide dot files in the Linux tk file dialog
# https://mail.python.org/pipermail/tkinter-discuss/2015-August/003762.html
# try:
#     # call a dummy dialog with an impossible option to initialize the file
#     # dialog without really getting a dialog window; this will throw a
#     # TclError, so we need a try...except :
#     try:
#         root.tk.call('tk_getOpenFile', '-foobarbaz')
#     except:
#         pass
#     # now set the magic variables accordingly
#     root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
#     root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
# except:
#     pass

# Attempt to compensate for high-DPI displays (not working)
#root.tk.call('tk', 'scaling', 4.0)
#root.tk.call('tk', 'scaling', '-displayof', '.', 50)

# Grid the main window and start mainloop
# app = Root(root).pack(side="top", fill="both", expand=True)
root = Root()
root.mainloop()