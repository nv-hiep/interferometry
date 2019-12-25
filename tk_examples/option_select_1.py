import tkinter as tk

root = tk.Tk() 

def print_choice(event):
    print(event)# prints selection directly from the event passed by the command in OptionMenu

working_list = ["Option 1", "Option 2", "Option 3", "Option 4"]

for i in range(4):
    tk.OptionMenu(root, tk.StringVar(), *working_list, command=print_choice).pack()

root.mainloop()