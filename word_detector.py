import cv2
import numpy as np

'''
    This is the fourth process in ocr!!

        Use before this: line_detector

        Use after this:  character_detector


'''
def word_extractor(lines):

    '''
        We make use of morphological operations such as dilation to find the words in given lines.
        :param lines: A list containing all the lines extracted from the image
        :return: A 2d list of all the words extracted from every line.words[i][] represents the ith line and words[i][j]
        represent the jth word in the ith line
    '''
    '''
        This is an interesting module and has a lot of basic mathematics used. Here we use the concept of average width
        between two words in order to find the words in the lines. The average width is used in order to
        minimise the false positives obtained in form of space between two  characters of the same word.
        In this two pass algorithm we first detect all the spaces in the given line images using the vertical histogram.
        Then we compute the average width of the given spaces. Then in the second pass we remove all those spaces Si
        whose width does not satisfy the following equation:
                                Si/average width >threshold;
        The threshold is determined using trial and error and the threshold used here is 0.4.
        This two pass algorithm is fairly accurate to meet the criterion needed in a standard ocr.

    '''

    words = []                      #Declare a list that will store all the words in given line image array
    for i in range(0,len(lines)):
        raw_line = lines[i].copy()
        raw_line = cv2.resize(raw_line,(900,300))              #Resize the image for dilation to work better
        kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(2,2)) #A 2x2 square used as kernel
        copy_line=cv2.dilate(raw_line,kernel,iterations=2)     #Dilating the raw_line to get copy_line
        y_sum = cv2.reduce(copy_line, 0, cv2.REDUCE_AVG)       #generating vertical histogram of dilated lines image
        y_sum=y_sum[0]                                         #y_sum would be of form a[[]] we need a[]
        pass_1_count = []                                      #Stores thickness of all detected spaces in pass 1
        j=1
        i=0
        x_start=0
        x_end=0
        x_coord=[]                                            #Stores the starting and ending coordinates of spaces
        while i<len(y_sum):
            j=1
            if y_sum[i]!=0:
                i=i+1
                continue
            else:                                            #If Space is detected
                x_start=i
                k=i
                j=0
                while k<len(y_sum) and y_sum[k]==0:         #While the space is continuously detected
                    k+=1
                    j+=1
                i=i+j
                x_end=x_start+j                             #The end of space = start of space+width of space
                x_coord.append([x_start,x_end])             #Append this coordinate list in x_coord
                pass_1_count.append(j)                      #Append the thickness of the space in pass_1_count
        pass_1_count=pass_1_count[1:-1]                     #Removing first and last spaces which are basically margins
        x_coord=x_coord[1:-1]                               #Removing the coordinates of margins
        average=5
        if(len(pass_1_count)!=0):
            average = sum(pass_1_count)//len(pass_1_count)      #Average width of all spaces
        loc=[]                                              #Stores all the coordinates that don't satisfy threshold
        i=0
        threshold = 0.4                                     #Threshold determined after trial and error
        for i in range(0,len(x_coord)):
            difference = x_coord[i][1]-x_coord[i][0]        #Thickness of the space
            if difference/average<threshold:
                loc.append(x_coord[i])
        for i in range(0,len(loc)):
            x_coord.remove(loc[i])                          #Remove all invalid spaces from x_coord

        word_line=[]                                        #Stores the words of given line. Helps in later process
        height = raw_line.shape[:2][0]                      #Stores the height of raw_line image
        roi = raw_line[0:height,0:x_coord[0][0]]            #roi aka Region of interest extracting first word in line
        y_sum = cv2.reduce(roi, 0, cv2.REDUCE_AVG)
        y_sum=y_sum[0]
        i=0
        while(y_sum[i]<=0):                                 #Removing the margin from word using vetical histogram
            i+=1
        roi = raw_line[0:height,i:x_coord[0][0]]            #Extracting marginless word
        roi = cv2.resize(roi,(500,500))                     #Resize first word to 300x300 pixels
        word_line.append(roi)                               #Append it to the word_line

        #The segment below appends the intermediate words of the line to word_line
        for i in range(1,len(x_coord)):
            roi=raw_line[0:height,x_coord[i-1][1]:x_coord[i][0]]
            roi = cv2.resize(roi,(500,500))
            word_line.append(roi)

        #Repeating the first word process to the last word as it may also contain margin
        roi = raw_line[0:height,x_coord[len(x_coord)-1][1]:900]
        y_sum = cv2.reduce(roi, 0, cv2.REDUCE_AVG)
        y_sum=y_sum[0]
        i=len(y_sum)-1
        while(y_sum[i]<=0):
            i-=1
        roi = raw_line[0:height,x_coord[len(x_coord)-1][1]:x_coord[len(x_coord)-1][1]+i]
        roi = cv2.resize(roi,(500,500))
        word_line.append(roi)

    #-------------------------------------------------------------------------------------------------------------------
    # This snippet of code is used while testing. Can be skipped or commented!!
    #     for i in range(len(word_line)):
            # cv2.imshow('lol',word_line[i])
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
    #-------------------------------------------------------------------------------------------------------------------
        words.append(word_line)
    return words














