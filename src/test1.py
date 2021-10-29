# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 11:52:47 2020

@author: Josenalde
"""
# channels B, G, R (0, 1, 2)


import cv2 as cv

image = cv.imread('amostra1.jpeg')
#imageGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
#cv.imshow('contagem de cochonilas', image[:,:,0]) # 780 x 1040, 24 bits deep, 96 dpi
#cv.waitKey(0)
#cv.destroyAllWindows()

#img.itemset((10,10,2),100) - chance specific pixel or R channel to 100
#img.item(10,10,2) - get pixel of specific x, y pos of R channels

print(image.shape) # (r, c, channels) - tuple
# if it is grayscale, only (r, c)

resolution = image.size
print(resolution) # 2.5 MP

#b,g,r = cv.split(image)


# image.dtype - uint8

# select a region and copy it
#ball = img[280:340, 330:390]
#img[273:333, 100:160] = ball

# separate channels - costly operation
#b,g,r = cv.split(img)
#img = cv.merge((b,g,r))