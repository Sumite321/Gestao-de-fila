from tkinter import *
import tkinter as tk
import datetime
import MySQLdb

global a
tmp = []
tmp1 = []

def callback():
    nameOfStudent = ""
    duplicate = True
    db = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="",
                         db="gestao_bar")
        
    cur = db.cursor()
                         
    cur.execute("SELECT * FROM dados_cartao")
 
    for row in cur.fetchall():
        print(row[0], row[1])
        if(a.get() == row[0]):
            nameOfStudent = row[1]
            print("Student found")
            print(nameOfStudent)

    for name in tmp:
        print("Nome: " + nameOfStudent)
        print("Nome2: " + name.cget("text"))
        if (nameOfStudent == name.cget("text")):
            duplicate = False
            print("Duplicate value found")

    if (duplicate):
        a.addLabel(nameOfStudent)

    db.close()
    print(a.get().lower())
    
    
    #a.addLabel(a.get())

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
        self.frame1 = tk.Frame(root, bg = 'white')
        self.frame2 = tk.Frame(root, bg = 'white')

        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame2.grid(row=0, column=1, sticky="nsew")

        root.grid_columnconfigure(0, weight=1, uniform="group1")
        root.grid_columnconfigure(1, weight=1, uniform="group1")
        root.grid_rowconfigure(0, weight=1)

        Label(self.frame1, text="Lista de espera", font=('Verdana', '14', 'bold'), height=3).pack()
        Label(self.frame2, text="Sua vez", font=('Verdana', '14', 'bold'), height=3).pack()

        fonte1 = ('Verdana', '10', 'bold')
        self.nomef = Entry(self.frame1, width=10, font=fonte1)
        self.nomef.pack()
        b = Button(self.frame1, text="Adicionar", command=callback)
        b.pack()

        c = Button(self.frame2, text=">>", command=destroy)
        c.pack()

    def get(self):
        return self.nomef.get()
    
    def addLabel(self,name):
        tmp.append(Label(self.frame1, text=name, height=3))
        for x in tmp:
            x.pack()

    def addToMyTurn(self,name):
        tmp1.append(Label(self.frame2, text=name, height=3))
        for x in tmp1:
            x.pack()

root = Tk()
a = Menu(root, "Lista")
root.geometry("640x480")
root.mainloop()

