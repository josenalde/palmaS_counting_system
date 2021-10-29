# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 16:34:06 2020

@author: Josenalde
"""

#Histogram is a graphical representation of the intensity distribution of an image
#It quantifies the number of pixels for each intensity value considered.

import cv2 as cv
#import matplotlib.pyplot as plt
#import numpy as np

#simple test to remove background greenish
img = cv.imread('amostra6.jpg')
imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)

#ret, T = cv.threshold(imgG, 130, 255, cv.THRESH_BINARY) # 'olhos' em vermelho com 130



imgGray = cv.cvtColor(imgHSV, cv.COLOR_BGR2GRAY)

#ret2, T2 = cv.threshold(imgG, 70, 255, cv.THRESH_BINARY_INV) # 'area preta'
#masked = cv.bitwise_and(img, img, mask=T2)

cv.imshow('circles', imgGray)
cv.waitKey(0)
cv.destroyAllWindows()


# color = ('b','g','r')
# for i,col in enumerate(color):
#     histr = cv.calcHist([T],[i],None,[256],[0,256])
#     plt.plot(histr,color = col)
#     plt.xlim([0,256])
#plt.show()

#cv.imshow('mask', masked)
#cv.waitKey(0)
#cv.destroyAllWindows()
#cv.imwrite('resultados/result17.png', masked)
