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

class main(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        