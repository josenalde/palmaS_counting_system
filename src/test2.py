# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 11:52:47 2020

@author: Josenalde
"""
# channels B, G, R (0, 1, 2)

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

def scatter3d():

    
    r, g, b = cv.split(rgbImg)
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1, projection="3d")
    
    pixel_colors = rgbImg.reshape((np.shape(rgbImg)[0]*np.shape(rgbImg)[1], 3))
    norm = colors.Normalize(vmin=-1.,vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()
    
    axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Red")
    axis.set_ylabel("Green")
    axis.set_zlabel("Blue")
    plt.show()
    
bgrImg = cv.imread('amostra1.jpeg')
rgbImg = cv.cvtColor(bgrImg, cv.COLOR_BGR2RGB)
#plt.imshow(rgbImg)
#plt.show()
# segmentation process based on color
#scatter3d()

# HUE, SATURATION, VALUE (BRIGHTNESS) - better to segment by color
# value from 0 dark to light at the top
# lower s - more gray, higher s, more pure
# hue tonality, shade 0 to 360 13 values
hsvImg = cv.cvtColor(rgbImg, cv.COLOR_RGB2HSV)
plt.imshow(hsvImg)
plt.show()

# btnImg = cv.imread('botao.jpg')
# btnrgb = cv.cvtColor(btnImg, cv.COLOR_BGR2RGB)
# btnhsv = cv.cvtColor(btnrgb, cv.COLOR_RGB2HSV)
# plt.imshow(btnhsv)
# plt.show()

#https://toolstud.io/color/rgb.php

r1 = (240, 100, 100)
r2 = (240, 100, 78)

#mask = cv.inRange(hsvImg, r2, r1)


ret, mask = cv.threshold(hsvImg, 200, 240, cv.THRESH_BINARY)
#mask_inv = cv.bitwise_not(mask)
#result = cv.bitwise_and(rgbImg, rgbImg, mask=mask)
plt.subplot(1, 2, 1)
plt.imshow(mask, cmap='gray')
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()

# # Combine the two masks
#     final_mask = mask + mask_white
#     result = cv2.bitwise_and(image, image, mask=final_mask)

#     # Clean up the segmentation using a blur
#     blur = cv2.GaussianBlur(result, (7, 7), 0)
#     return blur


# scatter plot HSV
# h, s, v = cv.split(hsvImg)
# fig = plt.figure()
# axis = fig.add_subplot(1, 1, 1, projection="3d")

# pixel_colors = hsvImg.reshape((np.shape(hsvImg)[0]*np.shape(hsvImg)[1], 3))
# norm = colors.Normalize(vmin=-1.,vmax=1.)
# norm.autoscale(pixel_colors)
# pixel_colors = norm(pixel_colors).tolist()
    
# axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
# axis.set_xlabel("Hue")
# axis.set_ylabel("Saturation")
# axis.set_zlabel("Value")
# plt.show()