##############################################################################################
#                            Dylan Maltos | Trevor Christian                                 #
#                                createClassifier.py                                         #
#  Contains method to train a custom classifier to a beable to recognize a face from dataset #
##############################################################################################

##############################################################################################
#                                     Library Imports                                        #
##############################################################################################

import numpy as np
import os, cv2
from PIL import Image

##############################################################################################
#    Function trainClassifier(): Trains a custom classifier to recognize face from dataset   #
##############################################################################################

def trainClassifier(name):
    # Define our path to custom dataset in the data folder
    path = os.path.join(os.getcwd(), "data", name)

    # Initialize list data structures for faces and ids
    faces = []
    ids = []

    # Store images in a numpy array
    # Walk through the directory structure starting from the specified path
    for root, dirs, files in os.walk(path):
    # Loop over each file in the directory and subdirectories
        for file in files:
            # Check if the file is an image with extensions png, jpg, or jpeg
            if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
                # Construct the full path to the image file
                imagePath = os.path.join(path, file)
                # Open the image and convert it to grayscale (L mode in PIL).
                image = Image.open(imagePath).convert('L') 
                # Convert the PIL image into a numpy array with data type uint8.
                npImage = np.array(image, 'uint8')
                
                try:
                    # Extract the ID from the filename, assuming the ID is before the 
                    # name in the filename separated by the dataset name
                    id = int(file.split(name)[0]) 
                    # Append the numpy image array to the faces list
                    faces.append(npImage)
                    ids.append(id)
                except ValueError:
                    # Handle case where ID extraction fails by printing an error message
                    print(f"Error processing file {file}: ID could not be extracted.")
                    continue
                
    # Convert list of IDs into a numpy array
    ids = np.array(ids)

    # Create an instance of the LBPH (Local Binary Patterns Histograms) Face Recognizer
    classifier = cv2.face.LBPHFaceRecognizer_create()
    # Train and save the classifier
    classifier.train(faces, ids)
    classifier.write(os.path.join("data", "classifiers", f"{name}_classifier.xml"))

##############################################################################################
#                                                                                            #
##############################################################################################