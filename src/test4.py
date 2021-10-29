# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 16:34:06 2020

@author: Josenalde
"""

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

  
bgrImg = cv.imread('cocho.jpeg')
grayImg = cv.cvtColor(bgrImg, cv.COLOR_BGR2GRAY)
#avgImg = cv.medianBlur(grayImg, 1)
# plt.imshow(bgrImg) # branco fica azulado e o marrom azul mais escuro
# plt.show()

# plt.subplot(3,3,1)
# plt.imshow(grayImg)
# plt.subplot(3,3,2)
# plt.hist(grayImg.ravel(),256,[0,256])
# plt.subplot(3,3,3)
# plt.imshow(avgImg)
# plt.show()

# detect circles in the image
circles = cv.HoughCircles(grayImg, cv.HOUGH_GRADIENT, 1.5, 50)
print(circles)
# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		cv.circle(output, (x, y), r, (0, 255, 0), 4)
		cv.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
	# show the output image
	cv.imshow("output", np.hstack([image, output]))
	cv.waitKey(0)
