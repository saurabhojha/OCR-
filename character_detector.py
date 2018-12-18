import cv2
'''
    This is the fifth process in ocr!!

        Use before this: word_detector

        Use after this:  character_detector


'''
def character_detector(words):
    '''
    This function takes the segmented words and further segments them into individual characters.
    :param words: A 2D list of word images from the segmented image. Words[i][j] represent the jth word in the ith line.
    :return: A 3D list of letters from the words. all_characters[i][j][k] represents the kth character of the jth word
     of the ith line.
    '''
    all_characters=[]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    for i in words:
        line_character=[]
        j=i
        for p in j:
            word_character=[]
            s=p
            s = cv2.threshold(p,100,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)[1]
            s = cv2.erode(s, kernel, iterations=2)
            x_sum = cv2.reduce(s, 0, cv2.REDUCE_AVG)       #generating horizontal histogram of  word image
            x_sum=x_sum[0]
            x_avg = sum(x_sum)//500
            hist =[]
            for i in range(0,500):
                if(x_sum[i]==0):
                    hist.append(False)
                else:
                    hist.append(True)
            j=1
            x_start=0                           # Start of the x_coordinate of the character
            x_end = 0                           # End of the x_coordinate of the character
            x_coord=[]                          # List that contains the starting and ending coordinate of all the characters in an image
            i=0                                 # counter variable
            while i<500:
                j=1
                if not(hist[i]):                #If it is a space column
                    i=i+1
                    continue
                else:
                    x_start = i                 # If not i is the starting coordinate of the character
                    temp = i                       # second counter
                    j=0
                    while temp<500 and hist[temp]:    # Till k doesn't reach end of image and hist of that column is not a space row
                        temp+=1
                        j+=1
                    i= i+j                     # Incrementing the first counter to point to end of detected character
                    x_end = x_start+j           # End coordinate of detected character = start coordinate + j
                    x_coord.append((x_start,x_end))
            for i in range (0,len(x_coord),1):
                roi = s[0:500,x_coord[i][0]:x_coord[i][1]]
                word_character.append(roi)
            line_character.append(word_character)
        all_characters.append(line_character)
    return all_characters
