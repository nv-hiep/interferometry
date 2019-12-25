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
        super(Root, self).__init__()
        root = tk.Tk()
        # self.title("Python Tkinter Dialog Widget")
        # self.minsize(640, 400)
        # self.wm_iconbitmap('icon.ico')

        # self.labelFrame = ttk.LabelFrame(self, text = "Open File")
        # self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)

        # self.button()


        self.menubar = tk.Menu(root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=donothing)
        self.filemenu.add_command(label="Open", command=donothing)
        self.filemenu.add_command(label="Save", command=donothing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=donothing)
        self.helpmenu.add_command(label="About...", command=donothing)
        self.helpmenu.add_command(label="Instructions",
                                      command=lambda fileName="docs/HELP.txt",
                                      title="Vriendly VRI Instructions" :
                                      show_textfile(fileName, self.title))
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        root.config(menu=self.menubar)



    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse A File",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)


    def fileDialog(self):

        self.filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =
        (("jpeg files","*.jpg"),("all files","*.*")) )
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = self.filename)




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

root = Root()
root.mainloop()