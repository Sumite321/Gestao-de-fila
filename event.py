from Tkinter import *

root = Tk()
sv = StringVar()

def callback():
    print(sv.get())
    return True

e = Entry(root, textvariable=sv, validate="focusout", validatecommand=callback)
e.grid()
e = Entry(root)
e.grid()
root.mainloop()
