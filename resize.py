# import cv2
# import os
#
# '''
#     This module is used to resize the images from 128*128 pixels to 28*28 pixels for efficiency.
#
# '''
# main_directory = r'C:\Users\Acer\Desktop\test\fnt\Sample0'
# i = 1
# destination = r'C:\Users\Acer\Desktop\test\Sample0'
# while(i<63):
#     directory = main_directory
#     new_directory = destination
#     if i<10:
#         directory = directory+str(0)+str(i)
#         new_directory = new_directory+str(0)+str(i)
#     else:
#         directory = directory+str(i)
#         new_directory = new_directory+str(i)
#
#     # if not os.path.exists(new_directory):
#     #     os.makedirs(new_directory)
#     for file_name in os.listdir(directory):
#         print("Processing %s" % file_name)
#         image = cv2.imread(os.path.join(directory, file_name))
#         new_dimensions = (28,28)
#         output = cv2.resize(image,new_dimensions)
#
#         output_file_name = os.path.join(new_directory,file_name)
#         cv2.imwrite(output_file_name,output)
#     i+=1
# print("All done")
