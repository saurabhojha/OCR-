# OCR-
This project implements the classical OCR pipeline using opencv-python.

The code is written in python and uses the following libraries:
* opencv-python for image processing tools and functions
* numpy for image manipulation as an array
* sklearn for svm classifiers
* os for directory manipulation
* pickle for saving and loading the svm model
* scipy for loading the emnist-letters dataset from a mat format file
* subprocess to open the text file into a notepad.

The code takes a text image as input and outputs a txt file with the text in editable form as extracted from the image.
The datasets used are:
* Emnist-letters 
* Char 74k
The images from the char 74k dataset are first converted into a npy file following the mnist dataset format and then sent for training to a linear kernel svm classifier.

This project uses image processing techniques of the spatial domain to segment the given text image into lines,words and finally into characters.
The segmented characters are then sent for recognition to the svm classifier.
Once the characters are recognised they are sent for text reconstruction and then saved into a text file.

Note: The code is not free of errors and exceptions. If the quality of the image is poor then exceptions can occur.
