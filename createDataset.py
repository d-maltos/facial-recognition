##############################################################################################
#                              Dylan Maltos | Trevor Christian                               #
#                                    createDateset.py                                        #
#                   Creates a custom dataset from images of the users face                   #
##############################################################################################

##############################################################################################
#                                     Library Imports                                        #
##############################################################################################

import cv2
import os

##############################################################################################
#                     Function datasetCapture(): Starts video capture                        #
##############################################################################################

def datasetCapture(name):
    # Define the filepath for the images to be saved to
    path = "./data/" + name 
    # Initialize a counter for the number of images captured
    numImages = 0
    
    # Load the Haar cascade for face detection from the specified file path 
    detector = cv2.CascadeClassifier("./data/haarcascade_frontalface_default.xml")
    
    # Try to create the directory for storing images, if it does not already exist
    try:
        os.makedirs(path)
    # If the directory already exists, inform the user
    except:
        print('Directory Already Exists')
    
    # Start video capture from default camera
    vidCapture = cv2.VideoCapture(0)
    
    while True:
        # Capture a frame from the video for the dataset
        ret, image = vidCapture.read()
        # Initialize variable to store the cropped face image for the dataset
        newImage = None
        # Convert the captured image to grayscale to simplify processing
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detect faces in the grayscale image
        faceRectangles = detector.detectMultiScale(image=grayImage, scaleFactor=1.1, minNeighbors=5)
        
        for x, y, w, h in faceRectangles:
            # Draw a rectangle around each detected face in the original image
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), 2)
            # Display a text label indicating that a face has been detected
            cv2.putText(image, "Face has been detected", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            # Display the number of images captured below each detected face for the dataset
            cv2.putText(image, str(str(numImages) + "images captured"), (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            # Crop the face from the grayscale image before saving as part of the dataset
            newImage = image[y:y+h, x:x+w]
        
        # Show the original image with annotations in a window titled 'Face Detection'
        cv2.imshow("Face Detection", image)
        # Listen for key presses
        key = cv2.waitKey(1) & 0xFF
        
        # Try: to save the cropped face image to the specified directory
        try:
            cv2.imwrite(str(path + "/" + str(numImages) + name + ".jpeg"), newImage)
            # Increment the count of captured images. 
            numImages += 1
        # Exception: if saving fails
        except:
            # Skip this iteration
            pass
        
        # Exit the loop if the user presses 'q' or 'ESC', or if 300 images have been captured
        if key == ord("q") or key == 27 or numImages > 300: 
            break
        
    # Release video capture and close all OpenCV windows
    cv2.destroyAllWindows()
    
    # Return the number of images captured
    return numImages

##############################################################################################
#                                                                                            #
##############################################################################################  

    

