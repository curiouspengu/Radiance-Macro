from customtkinter import *
from PIL import ImageTk
root = CTk()

import ctypes

myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

iconpath = ImageTk.PhotoImage(u"C:\Users\Curious Pengu\Documents\Apps\dolphSol\dolphSol-Improvement-Macro\data\main_gui\logo.ico")
root.iconbitmap("")
root.iconphoto(False, iconpath)
root.mainloop()