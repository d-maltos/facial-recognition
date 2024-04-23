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
from tkinter import messagebox, font as tkFont, PhotoImage

##############################################################################################
#                                     Global Variables                                       #
##############################################################################################

names = set()

##############################################################################################
#                       Main application class for the Tkinter GUI                           #
##############################################################################################

class appGUI(tk.Tk):
    
    # Initialize the Tkinter application
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        # Set a title font style
        self.titleFont = tkFont.Font(family='Helvetica', size=16, weight="bold")
        # Set the window title
        self.title("FaceRecognizer")
        # Disable window resizing
        self.resizable(False, False)
        # Set the window size
        self.geometry("350x160")
        # Set the behavior for the window's close button
        self.protocol("WM_DELETE_WINDOW", self.onClosing)
        # Active user name set to None initially
        self.activeName = None
        # Create a main container frame
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # Initialize all pages of the Tkinter GUI
        for F in (home, register, login, createDatasetTrainModel, faceVerification):
            pageName = F.__name__
            frame = F(container, self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame("home")

    def showFrame(self, pageName):
            # Raise the specified frame to the top of the stack
            frame = self.frames[pageName]
            frame.tkraise()

    def onClosing(self):
        # Confirmation dialog to ensure the user wants to quit
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names

##############################################################################################
#                                         Home Page                                          #
##############################################################################################

class home(tk.Frame):

        # Load and display an image on the home screen
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            render = PhotoImage(file='home.png')
            img = tk.Label(self, image=render, fg="#000000")
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")
            # Display a label with the application title
            label = tk.Label(self, text="        FaceRecognizer        ", font=self.controller.titleFont, fg="#68FEEF")
            label.grid(row=0, sticky="ew")
            # Buttons for different actions
            button1 = tk.Button(self, text="   Register  ", fg="black", bg="black", command=lambda: self.controller.showFrame("register"))
            button2 = tk.Button(self, text="   Log in  ", fg="black", bg="black", command=lambda: self.controller.showFrame("login"))
            button3 = tk.Button(self, text="Quit", fg="black", bg="black", command=self.onClosing)
            button1.grid(row=1, column=0, ipady=3, ipadx=7)
            button2.grid(row=2, column=0, ipady=3, ipadx=2)
            button3.grid(row=3, column=0, ipady=3, ipadx=32)

        def onClosing(self):
            # Confirmation dialog to quit the application
            if messagebox.askokcancel("Quit", "Are you sure?"):
                global names

##############################################################################################
#                                      Register Page                                         #
##############################################################################################

class register(tk.Frame):
    
    # Username entry field and related buttons
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Username", fg="#68feef", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.userName = tk.Entry(self, borderwidth=3, bg="black", font='Helvetica 11')
        self.userName.grid(row=0, column=1, pady=10, padx=10)
        self.buttonCancel = tk.Button(self, text="Cancel", bg="black", fg="#263942", command=lambda: controller.showFrame("home"))
        self.buttonNext = tk.Button(self, text="Next", fg="black", bg="#263942", command=self.startTraining)
        self.buttonClear = tk.Button(self, text="Clear", command=self.clear, fg="black", bg="#263942")
        self.buttonCancel.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonNext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
        self.buttonClear.grid(row=1, ipadx=5, ipady=4, column=2, pady=10)
    
    # Validate username and proceed to dataset creation / model training 
    def startTraining(self):
        global names
        if self.userName.get() == "None":
            messagebox.showerror("ERROR", "Name can't be 'None'")
            return
        elif self.userName.get() in names:
            messagebox.showerror("ERROR", "User already exists!")
            return
        elif len(self.userName.get()) == 0:
            messagebox.showerror("ERROR", "Name can't be empty!")
            return
        name = self.userName.get()
        names.add(name)
        self.controller.activeName = name
        self.controller.frames["login"].refreshNames()
        self.controller.showFrame("createDatasetTrainModel")
    
    # Clear the username entry field
    def clear(self):
        self.userName.delete(0, 'end')

##############################################################################################
#                                         Login Page                                         #
##############################################################################################

class login(tk.Frame):

    # Create and place labels, entries, and buttons for the login interface
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Username", fg="#68feef", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.userName = tk.Entry(self, borderwidth=3, bg="black", font='Helvetica 11')
        self.userName.grid(row=0, column=1, pady=10, padx=10)
        self.buttonCancel = tk.Button(self, text="Back", command=lambda: controller.showFrame("home"), bg="#ffffff", fg="#263942")
        self.buttonClear = tk.Button(self, text="Clear", command=self.clear, fg="black", bg="#263942")
        self.menuVar = tk.StringVar(self)
        self.buttonNext = tk.Button(self, text="Next", command=self.nextt, fg="black", bg="#263942")
        self.buttonCancel.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonNext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)
        self.buttonClear.grid(row=1, ipadx=5, ipady=4, column=2, pady=10)
    
    # Validates username input and proceeds to the next step
    def next(self):
        if self.userName.get() == 'None':
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.activeName = self.userName.get()
        self.controller.showFrame("faceVerification")  
    
    # Clears the username entry field
    def clear(self):
        self.userName.delete(0, 'end')
    
    # Placeholder function for next steps
    def nextt(self):
        if self.menuVar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.activeName = self.menuVar.get()
        self.controller.showFrame("faceVerification")

    # Refreshes the list of usernames
    def refreshNames(self):
        global names
        self.menuVar.set('')

##############################################################################################
#                            Create Dataset / Train Model Page                               #
##############################################################################################
            
class createDatasetTrainModel(tk.Frame):

    # UI elements for dataset creation and model training
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numImageLabel = tk.Label(self, text="Images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numImageLabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.captureButton = tk.Button(self, text="Create Dataset", fg="black", bg="#263942", command=self.captureImage)
        self.trainButton = tk.Button(self, text="Train Model", fg="black", bg="#263942",command=self.trainModel)
        self.captureButton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainButton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    # Initiates image capture, updates UI to reflect the number of captured images
    def captureImage(self):
        self.numImageLabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "Taking 300 frames of your face..")
        x = datasetCapture(self.controller.activeName)
        self.controller.numImages = x
        self.numImageLabel.config(text=str("Captured Images = "+str(x)))

    # Trains the model with the captured images if enough images have been captured
    def trainModel(self):
        if self.controller.numImages < 300:
            messagebox.showerror("ERROR", "Capture at least 300 images!")
            return
        trainClassifier(self.controller.activeName)
        messagebox.showinfo("SUCCESS", "Model successfully trained!")
        self.controller.showFrame("faceVerification")

##############################################################################################
#                                 User Verification Page                                     #
##############################################################################################

class faceVerification(tk.Frame):

    # Page for verifying the user via face recognition
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Buttons for user verification and navigation
        button1 = tk.Button(self, text="Verify", command=self.openWebcam, fg="black", bg="#263942")
        button4 = tk.Button(self, text="Home", command=lambda: self.controller.showFrame("home"), bg="black", fg="#263942")
        button1.grid(row=1, column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1, column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    # Initiates the webcam for live face verification
    def openWebcam(self):
        faceDetector(self.controller.activeName)
        
if __name__ == "__main__":
    app = appGUI()
    app.mainloop()

##############################################################################################
#                                                                                            #
##############################################################################################