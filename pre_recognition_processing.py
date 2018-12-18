import cv2
import numpy as np

'''
    This is the sixth process in ocr!!

        Use before this: character_detector

        Use after this:  pre_recognition processing


'''
def pre_recognition(all_characters):
    '''
    This function takes the segmented characters and converts them into the format used by dataset for recognition.
    On every character it perfroms the following:
    1. Resize the image to 28*28 pixels for recognition
    2. Normalize white pixels value from 255 to 1 for faster computation
    :param all_characters:  a 3D matrix/list with all the segmented characters obtained from character_detector module
    :return: a 3d matrix/list with resized and rescaled characters for recognition usig neural networks
    '''
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    modified_characters=[]
    i=0
    for lines in all_characters:
        for words in lines:
            for characters in words:
                copy = characters
                # copy	=  cv2.ximgproc.thinning(copy,thinningType = THINNING_ZHANGSUEN )
                # copy = cv2.dilate(copy,kernel,iterations = 5)
                copy = cv2.resize(copy,(24,24))
                copy= cv2.copyMakeBorder(copy,2,2,2,2,cv2.BORDER_CONSTANT,value=[0,0,0])
                copy = cv2.bitwise_not(copy)
                copy =  copy/ 255
                if(i<11):
                    cv2.imshow('Copy',copy)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    i+=1
                copy = copy.flatten('F')
                modified_characters.append(copy)
    modified_characters = np.array(modified_characters)
    print('No of characters detected:' +str(modified_characters.shape[0]))
    return modified_characters


