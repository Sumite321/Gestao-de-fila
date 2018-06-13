from Tkinter import *
import Tkinter as tk
import MySQLdb
import random

global a
tmp = []
tmp1 = []
COLORS =["red", "orange", "yellow", "green", "blue", "violet"]

def callback():
    nameOfStudent = ""
    Notduplicate = True
    found = False
    db = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="",
                         db="gestao_bar")
        
    cur = db.cursor()
                         
    cur.execute("SELECT * FROM dados_cartao")
 
    for row in cur.fetchall():
        if(a.get() == row[0]):
            nameOfStudent = row[1]
            found = True

    for name in tmp:
        if (nameOfStudent == name.cget("text")):
            Notduplicate = False

    if (Notduplicate) and found:
        a.addLabel(nameOfStudent)

    db.close()
    print(a.get().lower())
    a.clearText()


def destroy():
    if len(tmp1)>0:
        tmp1[0].destroy()
    if len(tmp1)>0:
        tmp1.pop(0)
    a.addToMyTurn(tmp[0].cget("text"))
    tmp[0].destroy()
    tmp.pop(0)

class Menu:
    def __init__(self, toplevel, title):
        
        self.level = toplevel
        self._after_id = None
        self.frame1 = tk.Frame(root, bg = 'lightblue')
        self.frame2 = tk.Frame(root, bg = 'lightgreen')

        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame2.grid(row=0, column=1, sticky="nsew")

        root.grid_columnconfigure(0, weight=1, uniform="group1")
        root.grid_columnconfigure(1, weight=1, uniform="group1")
        root.grid_rowconfigure(0, weight=1)

        Label(self.frame1, text="Lista de espera", font=('Verdana', '14', 'bold'), bg='lightblue', height=3).pack()
        Label(self.frame2, text="Sua vez", font=('Verdana', '14', 'bold'), bg='lightgreen', height=3).pack()

        fonte1 = ('Verdana', '10', 'bold')
        self.nomef = Entry(self.frame1, width=10, font=fonte1)
        self.nomef.pack()
        self.nomef.bind('<Key>',self.handle_wait)
        self.nomef.focus()
        self.b = Button(self.frame1, text="Adicionar", command=callback)
        self.b.pack()
        self.b.pack_forget()
        c = Button(self.frame2, text=">>", command=destroy)
        c.pack()

    def get(self):
        return self.nomef.get()
    
    def addLabel(self,name):
        fonte2 = ('Verdana', '15')
        tmp.append(Label(self.frame1, text=name, bg='lightblue', font=fonte2 ,  height=3))
        for x in tmp:
            x.pack()

    def addToMyTurn(self,name):
        fonte3 = ('Verdana', '15')
        tmp1.append(Label(self.frame2, text=name, bg='lightgreen',font=fonte3, height=3))
        for x in tmp1:
            x.pack()
    
    def clearText(self):
        self.nomef.delete(0, END)

    def handle_wait(self,event):
    
        if self._after_id is not None:
            self.level.after_cancel(self._after_id)
        
        # create a new job
        self._after_id = self.level.after(1000, self.change_color)
    
    def change_color(self):
        random_color = random.choice(COLORS)
        self.nomef.config(background=random_color)
        print("butao")
        self.b.invoke()

root = Tk()
a = Menu(root, "Lista")
root.geometry("640x480")
root.mainloop()
