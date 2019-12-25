from tkinter import *


class Buttons:
	
	def __init__(self, master):
		self.master = master
		self.frame = Frame(self.master)
		self.b1 = Button(self.master, text="Button1", command=self.display)
		self.b2 = Button(self.master, text="Button2", command=self.new_window)
		self.b1.pack()
		self.b2.pack()
		self.frame.pack()

	def display(self):
		print ('Hello Button1')

	def new_window(self):
		self.master.withdraw()
		self.newWindow = Toplevel(self.master)
		bb = Buttons1(self.newWindow)



class Buttons1():
	
	def __init__(self, master):
		self.master = master
		self.frame = Frame(self.master)
		self.b3 = Button(self.master, text="Button3", command=self.display3)
		self.b3.pack()
		self.frame.pack()
		

	def display3(self):
		print ('hello button3'
		)
	
if __name__ == '__main__':
	root = Tk()
	b = Buttons(root)
	root.mainloop()