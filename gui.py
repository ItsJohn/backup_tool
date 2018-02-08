from tkinter import *
from Create_Window import Create_Window

width = 500
height = 500

root = Tk()
root.title("Backup")
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(width, height))

window = Create_Window(root)

root.mainloop()
