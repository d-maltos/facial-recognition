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
from tkinter import messagebox

##############################################################################################
#                      Function faceDetector(): Detects a users face                         #  
##############################################################################################

def faceDetector(name, timeout=10):
    # Load Haar cascade for frontal face detection
    faceCascadeClassifier = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
    # Create a face recognizer using Local Binary Pattern Histograms
    faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
    # Load the trained classifier specific to the user
    faceRecognizer.read(f"./data/classifiers/{name}_classifier.xml")
    # Start video capture from the default camera (index 0)
    vidCapture = cv2.VideoCapture(0)
    # Initialize a variable to track if the user is recognized
    recognized = False
    # Record the start time - for the timeout feature
    startTime = time()
    
    try:
        while True:
            # Capture a frame from the camera
            ret, frame = vidCapture.read()
            if not ret:
                print("No frame grabbed")
                break
            
            # Convert the captured frame to grayscale to simplify processing
            grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect faces in the grayscale frame
            faces = faceCascadeClassifier.detectMultiScale(grayscale, 1.3, 5)
            # Predict the ID of the person and the confidence of the prediction
            for (x, y, w, h) in faces:
                grayscaleROI = grayscale[y:y+h, x:x+w]
                id, confidence = faceRecognizer.predict(grayscaleROI)
                # Convert confidence to a more intuitive percentage
                confidence = 100 - int(confidence)

                # If confidence > 80, then user is recognized.
                # Notes: 50 was too low, classifier recognized my mom as me!
                if confidence > 80:
                    recognized = True
                    text = 'Recognized User: ' + name
                    
                # Otherwise user is not recognized
                else:
                    text = 'ERROR: Unknown User'

                # Define the font for text in the frame
                font = cv2.FONT_HERSHEY_PLAIN
                # Draw a rectangle around the face and add the text
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                
            # Display the frame with the detection results
            cv2.imshow("image", frame)
            # Calculate the elapsed time
            totalTime = time() - startTime

            # Break the loop if the specified timeout has been reached
            if totalTime >= timeout:
                print(recognized)
                break
            
            # Allow the user to quit the loop by pressing 'q'.
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
    
    # Release the video capture object and close all OpenCV windows.
    finally:
        vidCapture.release()
        cv2.destroyAllWindows()

    # After the loop, display messages based on whether the user was recognized
    if recognized:
        messagebox.showinfo('User logged in!')
    else:
        messagebox.showinfo('ERROR: Try again!')
        
    # Return the prediction status (True if recognized, False otherwise)
    return recognized

##############################################################################################
#                                                                                            #
##############################################################################################