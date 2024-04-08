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
    
    numImages = 0
    
    # Intialize face detector using haar cascade classfier, 
    detector = cv2.CascadeClassifier("./data/haarcascade_frontalface_default.xml")
    
    try:
        os.makedirs(path)
    except:
        print('Directory Already Exists')
    
    # 
    vidCapture = cv2.VideoCapture(0)
    
    while True:
        ret, image = vidCapture.read()
        newImage = None
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faceRectangles = detector.detectMultiScale(image=grayImage, scaleFactor=1.1, minNeighbors=5)
        
        for x, y, w, h in faceRectangles:
            cv2.rectangle(image, (x, y), (x + w), (y + w), (0, 0, 0), 2)
            cv2.putText(image, "Face has been detected", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            cv2.putText(image, str(str(numImages) + "images captured"), (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            newImage = image[y:y+h, x:x+w]
        cv2.imshow("Face Detection, image")
        key = cv2.waitKey(1) & 0xFF
        
        try:
            cv2.imwrite(str(path + "/" + str(numImages) + name + ".jpeg"), newImage)       
            numImages += 1
        except:
            pass
        
        if key == ord("q") or key == 27 or numImages > 300: # Take 300 frames
            break
        
    cv2.destroyAllWindows()
    
    return numImages   
        
    

