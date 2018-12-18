import cv2
'''
        This is the first process in ocr!!

        Use before this: None!

        Use after this: skew_correction

'''
def image_noise_removal(path):
    '''
        Module used to remove noise from the image using built in cv2 functions such as canny edge detection.
        Since canny edge detector already has a method to remove noise from the image so applying gaussian filter
        Would be a redundant process.
        :param path: Specifies the given path of the image and is used by imread function to access image from the drive
        :return:image as a 600 x 600 matrix containig grayscale image.
    '''

    #The path of the image on disk is passed as a parameter to the function
    # which is used to load the image in raw_image

    raw_image = cv2.imread(path)

    #Most of the images we will work with must be resized. After trial and error a height of 600px was chosen
    #Resize the image to a dimension of 600 x 600 pixel

    # The raw image may have a RGB profile which must be converted to grayscale image for efficient computing
    raw_gray = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)

    # Inverting the gray pixels
    raw_gray = cv2.bitwise_not(raw_gray)

    #-------------------------------------------------------------------------------------------------------------------
    #This snippet of code is used while testing. Can be skipped or commented!!
    #Command to show the Original image in a new window named Original Image
    cv2.imshow("Original Image", raw_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #-------------------------------------------------------------------------------------------------------------------

    #Remove noise and achieve the outline of the text.
    canny = cv2.Canny(raw_gray,100,200)

    #use this canny image to smooth out the image.
    smoothened_gray_image = raw_gray-canny

    #-------------------------------------------------------------------------------------------------------------------
    #This snippet of code is used while testing. Can be skipped or commented!!
    #Command to show the smoothened_gray_image in a new window named Smoothened Gray Image
    # cv2.imshow("Smoothened Gray Image", smoothened_gray_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #-------------------------------------------------------------------------------------------------------------------
    #Return the smoothened_gray_image
    smoothened_gray_image = cv2.resize(smoothened_gray_image,(600,600))
    return smoothened_gray_image

#image_noise_removal(r'C:\Users\Acer\PycharmProjects\Image_processing-1\noise.png')
