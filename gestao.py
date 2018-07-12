from Tkinter import *
import Tkinter as tk
import MySQLdb
import random
from PIL import ImageTk, Image
#import RPi.GPIO as GPIO
import time
import threading
import os.path



global a
tmp = [] # lista de espera
tmp1 = [] # sua vez
COLORS =["red", "orange", "green"]
tmp2 = [] #imagens
counter = 0
lastWait = ["null"]


def callback():
    global counter
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
        print(row[0],row[1])
        if(a.get() == row[0]):
            nameOfStudent = row[1]
            found = True

    for name in tmp:
        if (nameOfStudent == name.cget("text")):
            Notduplicate = False

    if (Notduplicate) and found:
        counter += 1
        a.addLabel(nameOfStudent)
        a.updateCounter(len(tmp),counter)

    db.close()
    print(a.get().lower())
    a.clearText()


def destroy():
   
    if(len(tmp)) > 0:
        if(len(tmp1)>0):
            a.updatePreviousTurn(tmp1[0].cget("text"))
            tmp1[0].destroy()
            tmp2[0].destroy()
            tmp1.pop(0)
            tmp2.pop(0)
            a.updateCounter(len(tmp),counter)
        a.addToMyTurn(tmp[0].cget("text"))
        tmp[0].destroy()
        tmp.pop(0)
        a.updateCounter(len(tmp),counter)
    elif(len(tmp1)>0):
        a.updatePreviousTurn(tmp1[0].cget("text"))
        tmp1[0].destroy()
        tmp2[0].destroy()
        tmp1.pop(0)
        tmp2.pop(0)
        a.updateCounter(len(tmp),counter)



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

        Label(self.frame1, text="Lista de espera", font=('Verdana', '30', 'bold'), bg='lightblue', height=3).pack()
        
        self.counterUpdate = Label(self.frame1, text="0/2", font=('Verdana', '30', 'bold'), bg='lightblue', height=2)
        self.counterUpdate.pack()
        
        
        
        Label(self.frame2, text="Sua vez", font=('Verdana', '30', 'bold'), bg='lightgreen', height=3).pack()

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
    
        self.previous = Label(self.frame2, text="previous", font=('Verdana', '30', 'bold'), bg='lightgreen', height=3)
        self.previous.pack(side = BOTTOM)

    def get(self):
        return self.nomef.get()
    
    def set_path(self,path):
        self.path = path
    
    def get_path(self):
        return self.path
    
    def addLabel(self,name):
        fonte2 = ('Verdana', '25')
        tmp.append(Label(self.frame1, text=name, bg='lightblue', font=fonte2 ,  height=3))
        for x in tmp:
            x.pack()

    def addToMyTurn(self,name):
        fonte3 = ('Verdana', '25')
        tmp1.append(Label(self.frame2, text=name, bg='lightgreen',font=fonte3, height=3))

        for x in tmp1:
            x.pack()

        path = "Fotos/"
        path += name
        path += ".png"
        os.path.isfile(path)
        if os.path.isfile(path):
            path = path
        else:
            path = "unknow.png"

        img = ImageTk.PhotoImage(Image.open(path).resize((500, 500)))
                    
                    
        tmp2.append(tk.Label(a.frame2, image = img))
                    
        for photo in tmp2:
            photo.photo = img
            photo.pack()
    
    def clearText(self):
        self.nomef.delete(0, END)

    def handle_wait(self,event):
    
        if self._after_id is not None:
            self.level.after_cancel(self._after_id)
        
        self._after_id = self.level.after(1000, self.change_color)
    
    def change_color(self):
        random_color = random.choice(COLORS)
        self.nomef.config(background=random_color)
        print("butao")
        self.b.invoke()

    def updateCounter(self,inQueue,total):

        #self.counterUpdate.config(text=total)
        self.counterUpdate["text"]= str(inQueue) + "/" + str(total)

    def updatePreviousTurn(self,text):

        self.previous["text"] = text

class ThreadingExample(object):
    """ Threading example class
        The run() method will be started and it will run in the background
        until the application exits.
        """
    
    def __init__(self, interval=0.2):
        """ Constructor
            :type interval: int
            :param interval: Check interval, in seconds
            """
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.interval = interval
        
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
    
    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            input_state = GPIO.input(18)
            if input_state == False:
                print('Button Pressed')
                destroy()
            
            
            time.sleep(self.interval)

#example = ThreadingExample()

root = Tk()
a = Menu(root, "Lista")
root.geometry("640x480")
root.mainloop()







