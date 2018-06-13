import Tkinter as tk
import random

COLORS =["red", "orange", "yellow", "green", "blue", "violet"]

class Application(tk.Frame):
    
    def __init__(self,master):
        self.master = master
        tk.Frame.__init__(self)
        self.pack()
        
        self._after_id = None
        self.entry = tk.Entry(self)
        self.entry.pack()
        self.entry.bind('<Key>',self.handle_wait)
        self.entry.focus()
    def handle_wait(self,event):
        # cancel the old job
        if self._after_id is not None:
            self.after_cancel(self._after_id)
        
        # create a new job
        self._after_id = self.after(1000, self.change_color)
    
    def change_color(self):
        random_color = random.choice(COLORS)
        self.entry.config(background=random_color)
        print("butao")

root = tk.Tk()
app = Application(root)
app.mainloop()
