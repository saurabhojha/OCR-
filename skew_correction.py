import numpy as np
import cv2
'''One of the many problems of digitizing printed documents is the skewness of the given image. An Image that contains
   text maybe rotated to some degree which may cause problems when we try to segment the images into lines.
   This module will help to solve this problem by using the idea of forming a rectangle bounding the tilted text portion
   and then rotating this rectangle to achieve linear text regions'''
'''
        This is the second process in ocr!!

        Use before this: noise_removal

        Use after this: line_detector
'''

def skew_corrector(image):
    '''
        This Module will deal with tilt correction of the text region in an image. It includes:
        1. Thresholding the Image to achieve only two grayscales to deal with (black and white)
        2. Finding all the coordinates of the pixel containing white text portions.
        3. Detecting the minimum area rectangle that encloses all of these pixels.
        4. Finding the angle by which the rectangle is rotated.
           Note: The opencv's minAreaRect() function has a strange implementation for representing the angle of the
           rotated rectangle.
           Refer this site for more information:
           https://stackoverflow.com/questions/15956124/minarearect-angles-unsure-about-the-angle-returned
           https://namkeenman.wordpress.com/2015/12/18/open-cv-determine-angle-of-rotatedrect-minarearect/
        5. Using this angle to form a filter that will deskew the image
        6. Applying this filter to the image to obtained deskewed image
        :param image: A grayscale image of size 600 x 600 pixel
        :return: A binarized deskewed image with text in white and background in black.
    '''

    # Using THRESH_BINARY AND THRESH_OTSU TO ACHIEVE BETTER THRESHOLDING OF THE IMAGE
    thresh = cv2.threshold(image, 0, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #-------------------------------------------------------------------------------------------------------------------
    #This snippet of code is used while testing. Can be skipped or commented!!
    # cv2.imshow('thresh',thresh)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #thresh = cv2.bitwise_not(thresh)
    #erosion = thresh-erosion
    #cv2.imshow('Eroded',erosion)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #-------------------------------------------------------------------------------------------------------------------

    # Find all the coordinates in thresh where the pixel is white ie intensity >0
    white_coordinates = np.column_stack(np.where(thresh > 0))

    # cv2.minAreaRect gives the rectangle with least rotation
    # It has a confusing angle implementation and returns angle from -90 to 0.
    rectangle = cv2.minAreaRect(white_coordinates)

    #since this rectangle contains the center (x,y), the tuple (width,height) and the angle of rotated rectangle and we need
    #only center and the angle
    angle = rectangle[-1]
    #Since the cv2.getRotationMatrix2D() function accepts the angle and forms the affine transform matrix based on the
    #angle given. We need to format the angle returned by the minAreaRect to obtain correct rotation of the image

    # Correcting angle of the image in order to meet the assertions in the affine_matrix function.
    if angle< -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Extracting the dimensions of the image in the tuple (h,w)
    (h, w) = image.shape[:2]

    # Finding the center of the image.
    center = (w // 2, h // 2)
    '''
        Getting affine_matrix from getrotationMatrix2D
        Affine matrix is 2 x 3 matrix that helps to implement the translation and rotation of pixels using the idea of
        Straight Lines and their equations on a 2D plane.
        A line that is inclined to x axis at an angle of 45 degrees and passing through (0,3) has an equation y = x+3.
        If we want to convert this line to a straight line coincident with x axis ( i.e. y = 0) we need to first
        make the line pass through origin. In other words we need to reduce the constant term of the equation to zero.
        Thus we obtain the equation y = x.
        In order to make it co incident with the x axis we need to reduce the slope to zero. This gives us the equation
        y = 0. This 2 Step process can also be implemented using matrices as follows:

        T = [ a00 a01 b00 ] [x] = M . X'
            [ a10 a11 b10 ].[y]
        Here the matrix M is the affine matrix and the elements a00 a01 a10 a11 do the job of rotation while b00 and b10
        does the job of translation.

        Refer This site for more:
        https://docs.opencv.org/3.1.0/d4/d61/tutorial_warp_affine.html
        https://docs.opencv.org/3.1.0/da/d54/group__imgproc__transform.html#gafbbc470ce83812914a70abfb604f4326

        The wrapAffine function then uses this matrix to form the new image and contains following parameters:
        1. src	input image.
        2. dst	output image that has the size dsize and the same type as src .
        3. M	2×3 transformation matrix.
        4. dsize	size of the output image.
        5.flags	combination of interpolation methods (see cv::InterpolationFlags)
        and the optional flag WARP_INVERSE_MAP that means that M is the inverse transformation ( dst→src )
        6.borderMode	pixel extrapolation method (see cv::BorderTypes);
        when borderMode=BORDER_TRANSPARENT, it means that the pixels in the destination image corresponding
        to the "outliers" in the source image are not modified by the function.
        7.borderValue	value used in case of a constant border; by default, it is 0.
    '''
    # The getRotationMatrix2D function needs the center of the image , the angle to be rotated and the isotropic scale
    # factor in order to return a 2 x 3 affine matrix.

    affine_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    #making the deskewed image by applying the affine_matrix on the image using warpAffine function
    rotated = cv2.warpAffine(thresh, affine_matrix, (w,h),
	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    rotated = cv2.threshold(rotated, 0, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    #-------------------------------------------------------------------------------------------------------------------
    #This snippet of code is used while testing. Can be skipped or commented!!
    cv2.imshow('Deskewed Image',rotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #-------------------------------------------------------------------------------------------------------------------

    return rotated
#skew_corrector(noise_removed_image)
