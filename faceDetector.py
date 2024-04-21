##############################################################################################
#                            Dylan Maltos | Trevor Christian                                 #
#                                  faceDetector.py                                           #
#                        Contains method to detect a users face                              #
##############################################################################################

##############################################################################################
#                                     Library Imports                                        #
##############################################################################################

import cv2
from time import time
from PIL import Image
from tkinter import messagebox

##############################################################################################
#                      Function faceDetector(): Detects a users face                         #  
##############################################################################################

def faceDetector(name, timeout = 5):
    faceCascadeClassifier = cv2.CascadeClassifier('./data/haarscascade_frontalface_default.xml')
    faceRecognizer = cv2.face.LBPHFacialRecognizer_create()
    faceRecognizer.read(f"./data/classifiers{name}_classifier.xml")
    vidCapture = cv2.VideoCapture(0)
    predict = True
    startTime = time()
    
    while True:
        ret, frame = vidCapture.read()
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = faceCascadeClassifier.detectMultiScale(grey, 1.3, 5)
        
        for (x, y, w, h) in faces:
            greyROI = grey[y:y+h, x:x+w]
            id, confidence = faceRecognizer.predict(greyROI)
            confidence = 100 - int(confidence)
            
            # If confidence > 50, user is recognized
            if confidence > 50:
                predict = True
                text = 'Recognized User:' + name
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                
            # Otherwise, user is not recognized
            else:
                predict = False
                text = 'ERROR: Unknown User'
                font = cv2.FONT_HERSHEY_PLAIN
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                
        cv2.imshow("image", frame)
        totalTime = time() - startTime
        
        if totalTime >= timeout:
            print(predict)
            
            if predict:
                messagebox.showinfo('User logged in!')
            else:
                messagebox.showinfo('ERROR: Try again!')
            break
        
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
        
        vidCapture.release()
        cv2.destroyAllWindows
    
    return

