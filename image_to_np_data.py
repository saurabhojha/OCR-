# import cv2
# import os
# import numpy as np
# '''
# This module will take the test data directory and train data directory and convert it into a numpy array and save it as
# a numpy file for feeding to the convolution neural network
# '''
# main_directory = r'C:\Users\Acer\Desktop\test data\Sample0'
# i = 1
# count =0
# final_array = []
# input_array = []
# output_array=[]
# while(i<63):
#     directory = main_directory
#     if i<10:
#         directory = directory+str(0)+str(i)
#     else:
#         directory = directory+str(i)
#     for file_name in os.listdir(directory):
#         print("Processing %s" % file_name)
#         y_value = np.zeros((62))
#         y_value[i-1]=1
#         image = cv2.imread(os.path.join(directory, file_name),cv2.IMREAD_GRAYSCALE)
#         flat = image
#         flat = flat.flatten('F')
#         flat = flat/255
#         input_array.append(flat)
#         output_array.append(y_value)
#     i+=1
# final_array.append(input_array)
# final_array.append(output_array)
# final_array = np.array(final_array)
# np.save('testing_data.npy',final_array)
# print('ALL DONE')
