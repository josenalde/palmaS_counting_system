# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 11:52:47 2020

@author: Josenalde
"""
# channels B, G, R (0, 1, 2)

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

  
bgrImg = cv.imread('botao.jpg')
rgbImg = cv.cvtColor(bgrImg, cv.COLOR_BGR2RGB)

#plt.hist(rgbImg.ravel(),256,[0,256]); plt.show()

color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv.calcHist([rgbImg],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.show()

#plt.imshow(rgbImg)
#plt.show()
# segmentation process based on color

# HUE, SATURATION, VALUE (BRIGHTNESS) - better to segment by color
# value from 0 dark to light at the top
# lower s - more gray, higher s, more pure
# hue tonality, shade 0 to 360 13 values
hsvImg = cv.cvtColor(rgbImg, cv.COLOR_RGB2HSV)
#plt.imshow(hsvImg)
#plt.show()

#https://toolstud.io/color/rgb.php

r1 = (180, 180, 180)
r2 = (255, 255, 255)
#mask = cv.inRange(rgbImg, r1, r2)
#mask_inv = cv.bitwise_not(mask)
grayImg = cv.cvtColor(rgbImg, cv.COLOR_RGB2GRAY)
#blurImg = cv.GaussianBlur(grayImg, (7, 7), 0)
#blurImg = cv.medianBlur(grayImg, 5)
#plt.imshow(blurImg)
#plt.show()
#ret, mask = cv.threshold(blurImg, 160, 255, cv.THRESH_BINARY)
mask = cv.adaptiveThreshold(grayImg,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,5,2)
result = cv.bitwise_and(rgbImg, rgbImg, mask=mask)
# https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
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

# img = cv.imread('gradient.png',0)
# ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
# ret,thresh2 = cv.threshold(img,127,255,cv.THRESH_BINARY_INV)
# ret,thresh3 = cv.threshold(img,127,255,cv.THRESH_TRUNC)
# ret,thresh4 = cv.threshold(img,127,255,cv.THRESH_TOZERO)
# ret,thresh5 = cv.threshold(img,127,255,cv.THRESH_TOZERO_INV)
# titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
# images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
# for i in xrange(6):
#     plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()

# img = cv.imread('home.jpg',0)
# # create a mask
# mask = np.zeros(img.shape[:2], np.uint8)
# mask[100:300, 100:400] = 255
# masked_img = cv.bitwise_and(img,img,mask = mask)
# # Calculate histogram with mask and without mask
# # Check third argument for mask
# hist_full = cv.calcHist([img],[0],None,[256],[0,256])
# hist_mask = cv.calcHist([img],[0],mask,[256],[0,256])
# plt.subplot(221), plt.imshow(img, 'gray')
# plt.subplot(222), plt.imshow(mask,'gray')
# plt.subplot(223), plt.imshow(masked_img, 'gray')
# plt.subplot(224), plt.plot(hist_full), plt.plot(hist_mask)
# plt.xlim([0,256])
# plt.show()