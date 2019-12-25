# from tkinter import ttk
# import tkinter as tk

# win = tk.Tk()
# win.resizable(width=0, height=0)

# tree = ttk.Treeview(win, selectmode='browse')
# tree.pack(side='left')

# vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
# vsb.pack(side='right', fill='y')

# tree.configure(yscrollcommand=vsb.set)

# tree["columns"] = ("1", "2")
# tree['show'] = 'headings'
# tree.column("1", width=100, anchor='c')
# tree.column("2", width=100, anchor='c')
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

# win.mainloop()







import tkinter
from tkinter import ttk

class App(tkinter.Frame):
    def __init__(self,parent):
        tkinter.Frame.__init__(self, parent, relief=tkinter.SUNKEN, bd=2)
        self.parent = parent        

        self.menubar = tkinter.Menu(self)
        self.parent.winfo_toplevel().configure(menu=self.menubar)

        self.tree = ttk.Treeview(self)

        self.yscrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.yscrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.yscrollbar.grid(row=0, column=1, sticky='nse')
        self.yscrollbar.configure(command=self.tree.yview)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("MyApp")
    app = App(root)
    app.pack(fill="both", expand=False)
    app.mainloop()