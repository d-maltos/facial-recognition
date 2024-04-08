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

    # Initialize data structures for faces and ids
    faces = []
    ids = []

    # Store images in a numpy file format
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
                imagePath = os.path.join(path, file)
                image = Image.open(imagePath).convert('L') 
                npImage = np.array(image, 'uint8')
                try:
                    id = int(file.split(name)[0]) 
                    faces.append(npImage)
                    ids.append(id)
                except ValueError:
                    print(f"Error processing file {file}: ID could not be extracted.")
                    continue

    ids = np.array(ids)

    # Train and save the classifier
    classifier = cv2.face.LBPHFaceRecognizer_create()
    classifier.train(faces, ids)
    classifier.write(os.path.join("data", "classifiers", f"{name}_classifier.xml"))

