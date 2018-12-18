import cv2
'''
    This is the third process in ocr!!

    Use before this: skew_correction

    Use after this: word_detector


'''
def line_extractor(deskewed_image):
    '''
        This module will segment the text image into corresponding lines containing text.
        :param deskewed_image: Image contains deskewed text portions with black background and white text having a
        dimension of 600 x 600 pixel.
        :return: A list containing all the segmented lines from the image having a width of 600 pixels.
    '''

    # We Use the morphological process of erosion to erode out any connected components between lines.

    # To maintain the text in proper form we use a 2 x 1 rectangular structuring element to erode out only connected
    # components between lines.

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2))

    #Applying new structuring element to the deskewed_image for 1 iteration.
    eroded_image = cv2.erode(deskewed_image, kernel, iterations=0)

    #-------------------------------------------------------------------------------------------------------------------
    # #This snippet of code is used while testing. Can be skipped or commented!!
    # cv2.imshow('Erosion',eroded_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #-------------------------------------------------------------------------------------------------------------------


    '''
        This is an interesting part in this module. Here we take the advantage of the regularity in the printed text
        to accurately determine the textual line segments in the image.
        We need to set the margins of the image to zero as those may also be detected. We set 1% of both the left and
        right margins to zero.
        Here we make use of the concept of horizontal histogram to determine the average of white pixels per row.
        If a row has 0 white pixels then we can safely assume the row to be a space row.
        The problem however lies in the row with a few rows containing white pixels and being a part of the textual line.
        For example the g y p q j, in many fonts, have few components below the standard line.
        Similarly t i d f h k l b  have a few components above the standard line. Consider a scenario where words with
        these alphabets appear in text in certain fonts where there is no proper distinction between the components
        below and above the standard line. In such cases the row will have some average value and it can not be assumed
        to be a space row.
        In such rows where average is greater than zero but below a pre-determined white_pixel_threshold
        (in our scenario <=20)
        we determine the transition_count of the row.
        transition count measures how many times the value of the pixel intensity changes in a row from black to white
        and white to black. Then we use this transition_count and compare it with the pre determined
        transition_count_threshold to determine if the white pixel is a stray pixel (noise pixel)
        or that of a letter from a word. In our use case the transition_count_threshold value of 4 worked pretty
        accurately as a line may contain more than 2 letters having a component above or below the standard line.

        Using this data we construct a boolean vector hist (a.k.a histogram) containing 600 rows(length of the image)
        If the row contains stray pixels or has a value of zero it is assigned False in the matrix else True.

        We can then segment all the lines using this histogram matrix and basic array manipulation.

        Note:
        Specific functions can be written to calculate the transition_count_threshold, white_pixel_threshold and
        line_thickness_threshold to better suit the use case!This would require a two pass algorithm that may be
        computationally expensive but highly accurate.
    '''


    # Using built in reduce function from opencv to determine the average of all the pixel in a given row.
    x_sum = cv2.reduce(eroded_image, 1, cv2.REDUCE_AVG)
    hist = []


    #Finding the height dimension of the image using shape function.
    height = eroded_image.shape[:2][0]
    white_pixel_threshold = 20
    transition_count_threshold = 4
    line_thickness_threshold = 10


    # during thresholding, it's possible that border pixels were
	# included in the thresholding, so let's set 1% of the left and
	# right borders to zero
    p = int(eroded_image.shape[1] * 0.01)
    eroded_image[:, 0:p] = 0
    eroded_image[:, eroded_image.shape[1] - p:] = 0


    for i in range(0,height):
        if x_sum[i][0]==0:
            hist.append(False)
        elif x_sum[i][0]>0 and x_sum[i][0]<=white_pixel_threshold: #The below/above standard line condition
            l = eroded_image[i]
            transition_count = 0
            for j in range(1,len(l)):
                if l[j]!=l[j-1]:
                    transition_count+=1
            if transition_count>=transition_count_threshold:
                hist.append(True)
            else:
                hist.append(False)
        else:
            hist.append(True)
    #print(hist)


    j=1
    y_start=0                           # Start of the y_coordinate of the line
    y_end = 0                           # End of the y_coordinate of the line
    y_coord=[]                          # List that contains the starting and ending coordinate of all the lines in an image
    i=0                                 # counter variable
    while i<height:
        j=1
        if not(hist[i]):                #If it is a space row
            i=i+1
            continue
        else:
            y_start = i                 # If not i is the starting coordinate of the line
            k = i                       # second counter
            j=0
            while k<height and hist[k]:    # Till k doesn't reach end of image and hist of that row is not a space row
                k+=1
                j+=1
            i = i+j                     # Incrementing the first counter to point to end of detected line
            y_end = y_start+j           # End coordinate of detected line = start coordinate + j
        if y_end-y_start>line_thickness_threshold:
                                        # If the length of the line is greater than the threshold of the line thickness
            if height-y_end>2:          # If y_end is not at the end of the image
                y_coord.append((y_start-2,y_end+2)) # append line coordinates with 2 margin pixels on top and bottom
            else:
                y_coord.append((y_start-2,y_end))   # append line coordinates with only 2 pixel margin on top

    # Once y coordinates of starting and ending of lines are found append the lines into lines list.
    lines = []
    for i in range (0,len(y_coord),1):
        length = y_coord[i][1]-y_coord[i][0]
        roi = eroded_image[y_coord[i][0]:y_coord[i][0]+length,0:height]
        lines.append(roi)
    #-------------------------------------------------------------------------------------------------------------------
    # This snippet of code is used while testing. Can be skipped or commented!!
    display_image=eroded_image.copy()
    for i in range(0,len(y_coord)):
        cv2.rectangle(display_image, (0, y_coord[i][0]), (600, y_coord[i][1]), (255, 255, 255), 1)
    cv2.imshow('Detected Lines', display_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # print(y_coord)
    # for i in range (0,len(y_coord),1):
    #     length = y_coord[i][1]-y_coord[i][0]
    #     roi = eroded_image[y_coord[i][0]:y_coord[i][0]+length,0:600]
    #     cv2.imshow('Line',roi)
    #     cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # for i in lines:
    #     cv2.imshow('Lines',i)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    #-------------------------------------------------------------------------------------------------------------------

    return lines
