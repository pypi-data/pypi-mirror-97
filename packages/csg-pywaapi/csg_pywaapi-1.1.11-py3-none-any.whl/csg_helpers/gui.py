import tkinter
from tkinter import  messagebox
from tkinter import filedialog
from tkinter import *
import time



def messageBox(message,title=""):
    root = tkinter.Tk()
    root.withdraw()
    root.update()
    res = messagebox.showinfo(title,message)
    root.update()
    root.destroy()
    return res

def showMessageforXseconds(message,timer):
    root = tkinter.Tk()
    root.withdraw()
    root.update()
    top = tkinter.Toplevel(root)
    #top.title("Copy RTPCs from source to targets")
    tkinter.Message(top,text=message,padx=100,pady=100,font=("Ariel", 20)).pack()
    top.after(timer*1000, top.destroy)
    root.update()
    time.sleep(timer)
    root.destroy()
    return True


def askUserForDirectory():
    root = tkinter.Tk()
    root.withdraw()
    root.update()
    dir = filedialog.askdirectory(title="Choose source directory")
    root.update()
    root.destroy()
    return dir


def askUserForDropDownSelection(title,message,options):
    retVariable = {}
    def GetVariable():
        #global retVariable
        retVariable["name"] = (variable.get())
        #print(retVariable)
        root.destroy()
    root = Tk()
    root.title(title)
    root.geometry("500x200")
    choices = options
    variable = StringVar(root)
    variable.set(options[0])
    wText = Label(root, text=message)
    wText.place(x=20, y=20)
    w = OptionMenu(root, variable, *choices)
    w.place(x= 20,y=50)
    button = Button(root,text="Ok",command=GetVariable)
    button.place(x=175, y=100, height=50, width=150)
    root.mainloop()
    return retVariable

