##############################################################################################
#                              Dylan Maltos | Trevor Christian                               #
#                                         app.py                                             #
#                 Initializes the Facial Recognition program when run by user.               #
##############################################################################################

##############################################################################################
#                                     Library Imports                                        #
##############################################################################################

from faceDetector import faceDetector
from createClassifier import trainClassifier
from createDataset import datasetCapture
import tkinter as tk
from tkinter import messagebox, PhotoImage
from tkinter import font as tkfont

##############################################################################################
#                                     Global Variables                                       #
##############################################################################################

names = set()

##############################################################################################
#                          Tkinter User Interface Configuration                              #
##############################################################################################

class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open("nameslist.txt", "r") as f:
            x = f.read().rstrip().split(" ")
            for i in x:
                names.add(i)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Face Recognizer")
        self.resizable(True, True)
        self.geometry("500x250")  
        self.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.activeName = None
        self.configure(bg="#e9ebef")
        container = tk.Frame(self, bg="#e9ebef")
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage,):
            pageName = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame("StartPage")

    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

    def onClosing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            with open("nameslist.txt", "a+") as f:
                for i in names:
                    f.write(i + " ")
            self.destroy()

# First page, start page/home page
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        render = PhotoImage(file='homepage.png')
        img = tk.Label(self, image=render, bg="#e9ebef")
        img.image = render
        img.grid(row=0, column=4, rowspan=4, sticky="nsew")
        label = tk.Label(self, text="        Home Page        ", font=controller.title_font, fg="#000000", bg="#e9ebef")
        label.grid(row=0, sticky="ew")
        button1 = tk.Button(self, text="   Sign up  ", fg="#000000", bg="#e9ebef", command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="   Check a User  ", fg="#000000", bg="#e9ebef", command=lambda: controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Quit", fg="#263942", bg="#e9ebef", command=self.onClosing)
        button1.grid(row=1, column=0, ipady=3, ipadx=7)
        button2.grid(row=2, column=0, ipady=3, ipadx=2)
        button3.grid(row=3, column=0, ipady=3, ipadx=32)

    def onClosing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            with open("nameslist.txt", "w") as f:
                for i in names:
                    f.write(i + " ")
            self.controller.destroy()

# PageOne - Creates user

# PageTwo - Facial Recognition to very user


app = MainUI()
app.configure(bg="#e9ebef")
#app.iconphoto(True, tk.PhotoImage(file='icon.ico'))
app.mainloop()