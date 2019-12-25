#!/usr/bin/env python
__author__ = 'Hiep Nguyen'
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




# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(tk.Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        tk.Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master     = master

        self.bg_colour  = '#ececec'
        self.txtfont    = 'TkFixedFont'


        # changing the title of our master widget      
        self.master.title('Radio Arrays')
        
        # Set the grid expansion properties
        # self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)
        # self.rowconfigure(2, weight=1)



        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    





    #Creation of init_window
    def init_window(self):

        # Add a grid
        mainframe = ttk.Frame(self.master)
        mainframe.grid(row=0, column=0, sticky='NWES' )
        mainframe.columnconfigure(0, weight = 1)
        mainframe.rowconfigure(0, weight = 1)
        mainframe.pack(side='left', fill="both", expand=True, pady = 10, padx = 10)

        # for r in range(3):
        #     for c in range(4):
        #         tk.Label(mainframe, text='R%s/C%s'%(r,c),
        #         borderwidth=1 ).grid(row=r,column=c)

        # allowing the widget to take the full space of the root window
        # self.pack(fill='both', expand=1)
        # self.pack(side="top", fill="both", expand=True)

        # creating a menu instance
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        


        # create the file object)
        file = tk.Menu(menu, tearoff=True)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label='Exit', command=self.client_exit)

        #added "file" to our menu
        menu.add_cascade(label='File', menu=file)

        



        # create the file object)
        edit = tk.Menu(menu, tearoff=True)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label='Undo')

        #added "file" to our menu
        menu.add_cascade(label='Edit', menu=edit)




        # create the file object)
        help = tk.Menu(menu, tearoff=True)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        help.add_command(label='Undo')

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        help.add_command(label='Guide',
            command=lambda filename='docs/HELP.txt',
            title='Radio Array Instructions': self.show_textfile(filename, title) )

        #added "file" to our menu
        menu.add_cascade(label='Help', menu=help)



        # Create a Tkinter variable
        # tkvar = tk.StringVar(self.master)

        # Dictionary with options
        # choices = { 'Pizza','Lasagne','Fries','Fish','Potatoe'}
        # tkvar.set('Pizza') # set the default option

        # popupMenu = tk.OptionMenu(mainframe, tkvar, *choices)
        # tk.Label(mainframe, text="Choose a dish").grid(row = 0, column = 0)
        # popupMenu.grid(row = 0, column =1)
        # mainframe.pack(pady = 10, padx = 10)


        # Set the grid expansion properties
        mainframe.columnconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=4)
        # mainframe.rowconfigure(0, weight=1)
        # mainframe.rowconfigure(1, weight=1)
        # mainframe.rowconfigure(2, weight=1)



        tree = ttk.Treeview(mainframe, selectmode='browse')
        # tree.pack(side='left', fill="both", expand=True)

        vsb = ttk.Scrollbar(mainframe, orient="vertical", command=tree.yview)
        # vsb.pack(side='right', fill='both')

        tree.configure(yscrollcommand=vsb.set)

        tree["columns"] = ("1", "2")
        tree['show'] = 'headings'
        tree.column("1", width=15, anchor='c', minwidth=0, stretch=True)
        tree.column("2", width=15, anchor='c', minwidth=0, stretch=True)
        tree.heading("1", text="Account")
        tree.heading("2", text="Type")
        tree.insert("",'end',text="L1",values=("Big1","Best"))
        tree.insert("",'end',text="L2",values=("Big2","Best"))
        tree.insert("",'end',text="L3",values=("Big3","Best"))
        tree.insert("",'end',text="L4",values=("Big4","Best"))
        tree.insert("",'end',text="L5",values=("Big5","Best"))
        tree.insert("",'end',text="L6",values=("Big6","Best"))
        tree.insert("",'end',text="L7",values=("Big7","Best"))
        tree.insert("",'end',text="L8",values=("Big8","Best"))
        tree.insert("",'end',text="L9",values=("Big9","Best"))
        tree.insert("",'end',text="L10",values=("Big10","Best"))
        tree.insert("",'end',text="L11",values=("Big11","Best"))
        tree.insert("",'end',text="L12",values=("Big12","Best"))
        tree.grid(row=0, column=0, padx=5, pady=5, sticky="EW")



        # Create the canvas and grid
        # canvas = tk.Canvas(self, background="white", width=100,
        #                         height=100, highlightthickness=0)
        # canvas.grid(column=0, row=0, padx=0, pady=0)
        # canvas.columnconfigure(0, weight=1)
        # canvas.rowconfigure(0, weight=1)

        x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        v= np.array ([16,16.31925, 17.6394, 16.003,17.2861, 17.3131, 19.1259, 18.9694, 22.0003, 22.81226])
        p= np.array ([16.23697, 17.31653, 17.22094, 17.68631, 17.73641, 18.6368, 19.32125, 19.31756,
                      21.20247, 22.41444, 22.11718, 22.12453])

        fig = Figure(figsize=(4, 4))
        a = fig.add_subplot(111)
        a.scatter(v,x,color='red')
        a.plot(p, range(2 + max(x)),color='blue')
        a.invert_yaxis()

        a.set_title ("Estimation Grid", fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("X", fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master=mainframe)
        # canvas.get_tk_widget().pack()
        canvas.get_tk_widget().grid(row=0, column=1, padx=5, pady=5, sticky="EW")
        canvas.draw()







        # canvas = FigureCanvasTkAgg(fig, master=mainframe)
        # # canvas.get_tk_widget().pack()
        # canvas.get_tk_widget().grid(row=0, column=2, padx=5, pady=5, sticky="EW")
        # canvas.draw()


        # canvas = FigureCanvasTkAgg(fig, master=mainframe)
        # # canvas.get_tk_widget().pack()
        # canvas.get_tk_widget().grid(row=0, column=3, padx=5, pady=5, sticky="EW")
        # canvas.draw()






        # tree = ttk.Treeview(mainframe, selectmode='browse')
        # # tree.pack(side='left', fill="both", expand=True)

        # vsb = ttk.Scrollbar(mainframe, orient="vertical", command=tree.yview)
        # # vsb.pack(side='right', fill='both')

        # tree.configure(yscrollcommand=vsb.set)

        # tree["columns"] = ("1", "2")
        # tree['show'] = 'headings'
        # tree.column("1", width=15, anchor='c', minwidth=0, stretch=True)
        # tree.column("2", width=15, anchor='c', minwidth=0, stretch=True)
        # tree.heading("1", text="Account")
        # tree.heading("2", text="Type")
        # tree.insert("",'end',text="L1",values=("Big1","Best"))
        # tree.insert("",'end',text="L2",values=("Big2","Best"))
        # tree.insert("",'end',text="L3",values=("Big3","Best"))
        # tree.insert("",'end',text="L4",values=("Big4","Best"))
        # tree.insert("",'end',text="L5",values=("Big5","Best"))
        # tree.insert("",'end',text="L6",values=("Big6","Best"))
        # tree.insert("",'end',text="L7",values=("Big7","Best"))
        # tree.insert("",'end',text="L8",values=("Big8","Best"))
        # tree.insert("",'end',text="L9",values=("Big9","Best"))
        # tree.insert("",'end',text="L10",values=("Big10","Best"))
        # tree.insert("",'end',text="L11",values=("Big11","Best"))
        # tree.insert("",'end',text="L12",values=("Big12","Best"))
        # tree.grid(row=1, column=0, padx=5, pady=5, sticky="EW")


        # canvas = FigureCanvasTkAgg(fig, master=mainframe)
        # # canvas.get_tk_widget().pack()
        # canvas.get_tk_widget().grid(row=1, column=1, padx=5, pady=5, sticky="EW")
        # canvas.draw()







        # canvas = FigureCanvasTkAgg(fig, master=mainframe)
        # # canvas.get_tk_widget().pack()
        # canvas.get_tk_widget().grid(row=1, column=2, padx=5, pady=5, sticky="EW")
        # canvas.draw()


        # canvas = FigureCanvasTkAgg(fig, master=mainframe)
        # # canvas.get_tk_widget().pack()
        # canvas.get_tk_widget().grid(row=1, column=3, padx=5, pady=5, sticky="EW")
        # canvas.draw()





        











        # tree = ttk.Treeview(mainframe, selectmode='browse')
        # # tree.pack(side='left', fill="both", expand=True)

        # vsb = ttk.Scrollbar(mainframe, orient="vertical", command=tree.yview)
        # # vsb.pack(side='right', fill='both')

        # tree.configure(yscrollcommand=vsb.set)

        # tree["columns"] = ("1", "2")
        # tree['show'] = 'headings'
        # tree.column("1", width=15, anchor='c', minwidth=0, stretch=True)
        # tree.column("2", width=15, anchor='c', minwidth=0, stretch=True)
        # tree.heading("1", text="Account")
        # tree.heading("2", text="Type")
        # tree.insert("",'end',text="L1",values=("Big1","Best"))
        # tree.insert("",'end',text="L2",values=("Big2","Best"))
        # tree.insert("",'end',text="L3",values=("Big3","Best"))
        # tree.insert("",'end',text="L4",values=("Big4","Best"))
        # tree.insert("",'end',text="L5",values=("Big5","Best"))
        # tree.insert("",'end',text="L6",values=("Big6","Best"))
        # tree.insert("",'end',text="L7",values=("Big7","Best"))
        # tree.insert("",'end',text="L8",values=("Big8","Best"))
        # tree.insert("",'end',text="L9",values=("Big9","Best"))
        # tree.insert("",'end',text="L10",values=("Big10","Best"))
        # tree.insert("",'end',text="L11",values=("Big11","Best"))
        # tree.insert("",'end',text="L12",values=("Big12","Best"))
        # tree.grid(row=2, column=0, padx=5, pady=5, sticky="EW")


        # canvas = FigureCanvasTkAgg(fig, master=mainframe)
        # # canvas.get_tk_widget().pack()
        # canvas.get_tk_widget().grid(row=2, column=1, padx=5, pady=5, sticky="EW")
        # canvas.draw()







        # canvas = FigureCanvasTkAgg(fig, master=mainframe)
        # # canvas.get_tk_widget().pack()
        # canvas.get_tk_widget().grid(row=2, column=2, padx=5, pady=5, sticky="EW")
        # canvas.draw()


        # canvas = FigureCanvasTkAgg(fig, master=mainframe)
        # # canvas.get_tk_widget().pack()
        # canvas.get_tk_widget().grid(row=2, column=3, padx=5, pady=5, sticky="EW")
        # canvas.draw()

    
    




    def client_exit(self):
        exit()



    def show_textfile(self, filename, title=''):
        """Show a text file in a new window."""

        win = tk.Toplevel(background=self.bg_colour)
        win.title(title)
        txt = tkScrolledText(win, width=80,font=self.txtfont)
        txt.config(state="normal")
        with open(filename,'r') as f:
            text = f.read()
        txt.insert('1.0', text)
        txt.config(state="disabled")
        txt.grid(column=0, row=0, padx=5, pady=5, sticky="NSEW")
        xbtn = ttk.Button(win, text='Close',
                                   command=win.destroy)
        xbtn.grid(column=0, row=1, padx=5, pady=5, sticky="E")
        win.rowconfigure(0, weight=1)
        win.columnconfigure(0, weight=1)

        



# Force platform specific colours and fonts
# if sys.platform=="darwin":
#     bgColour = "#ececec"
#     fontSize = 12
# else:
#     bgColour = ttk.Style().lookup("TFrame", "background")
#     fontSize = 10        

# ttk.Style().configure("TFrame", background=bgColour)
# ttk.Style().configure("TLabelframe", background=bgColour)
# ttk.Style().configure("TLabel", background=bgColour)
# fontDefault = tkFont.nametofont("TkDefaultFont")
# fontDefault.configure(size=fontSize)
# fontFixed = tkFont.nametofont("TkFixedFont")
# fontFixed.configure(size=fontSize)
# root.option_add("*Font", fontDefault)





# root window created. Here, that would be the haveonly window, but
# you can later have windows within windows.
root = tk.Tk()

# root.minsize(640, 100)

root.geometry('900x600')
# root.geometry('1600x900')
root.resizable(0, 0)

#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()  