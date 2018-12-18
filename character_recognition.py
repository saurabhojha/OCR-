import cv2
import numpy as np
from sklearn import svm
import pickle
'''
    This is the seventh process in ocr!!

        Use before this: pre_recognition_processing

        Use after this:  text_generator


'''
'''
    This module converts the entire segmented character images stored in the 3D array to a 784 * 1 vector list for
    recogntion using the model learnt from the svm.

    This is the seventh process in ocr!!

        Use before this: pre_recognition_processing

        Use after this:  character_recognition_phase_2
'''

def character_prediction(test_data):
    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    predictions =  loaded_model.predict(test_data)
    print('Prediction Matrix is:')
    print(predictions)
    return predictions
