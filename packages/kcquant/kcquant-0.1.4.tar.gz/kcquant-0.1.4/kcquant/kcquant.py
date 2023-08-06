import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
from PIL import Image
import time

def get_colors(img, figsize=(15,5), columns=5, color='BGR', top=10):
    ''' Input an image in the format of a np.array and return
    subplots of each pixel color plotted with the RGB color value and number
    of pixels in the image that are that color.'''
    
    try:
        # reshape img pixels to be unrolled into one single column
        img = img.reshape((-1, 3))
    except:
        print('input image must be converted to np.array')
        img = np.array(img)
        img = img.reshape((-1, 3))
    
    # get the unique pixel values and their counts
    value, counts = np.unique(img, axis=0, return_counts=True)
    # create a list containing pairs of pixel values and their counts
    data = list(zip(value, counts))
    # sort list in reverse order from high to low counts
    data = sorted(data, reverse=True, key=lambda x: x[1])
    
    if top == None:
        # calculate how many subplot rows
        if len(data) % columns != 0:
            rows = int((len(data) // columns) + 1)
        else:
            rows = int(len(data) // columns)
    else:
        # assign the number of plots to make to be equal to top
        if top % columns != 0:
            rows = int(int(top // columns) + 1)
        else:
            rows = int(top // columns)
    
    
    
    # create a new figure for each row
    for row in range(rows):
        # plot figure
        plt.figure(figsize=figsize)
        # iterate through each unique color
        for i in range(columns):
            plt.subplot(1, columns, i+1)
            # turn off axes since it is 1 px by 1 px
            plt.axis('off')
            # calculate percentage of image that each pixel color makes up
            prc = round((data[(row*columns)+i][1]/len(img))*100,2)
            if color == 'BGR':
                
                plt.title(f'RGB: {data[(row*columns)+i][0][::-1]}\nTotal num pixels: {data[(row*columns)+i][1]}\n{prc}% of total pixels')
                # Reverse assuming image is in BGR color format
                plt.imshow([[list(data[(row*columns)+i][0])[::-1]]])
            elif color == 'RGB':
                plt.title(f'RGB: {data[(row*columns)+i][0]}\nTotal num pixels: {data[(row*columns)+i][1]}\n{prc}% of total pixels')
                # Reverse assuming image is in BGR color format
                plt.imshow([[list(data[(row*columns)+i][0])]])
            else:
                plt.title('Color not RGB')
            
        plt.tight_layout()
        
    return