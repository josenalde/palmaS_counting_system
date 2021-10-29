# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 16:34:06 2020

@author: Josenalde
"""

#test11 - includes male identification
import cv2 as cv
#import matplotlib.pyplot as plt
#import numpy as np

#by Josenalde Oliveira 06.07.2020
def isMale(pi, pj, M, maxLin, maxCol):
    nb = 4
    if (pi+nb<maxLin and pj+nb<maxCol):
        if (M[pi,pj,2] == 255): #if current pixel is red
            #print(M[pi,pj,2])
            if (M[pi,pj+nb-1,2] != 255 and M[pi,pj+nb,2] != 255):
                # print('pi: ' + str(pi))
                # print('pj: ' + str(pj))
                # print(M[pi,pj+nb-1,2])
                # print(M[pi,pj+nb,2])
                return True
            else:
                return False
    else:
        return False
    
# read image (BGR color)    
img = cv.imread('amostra1.jpeg')    
    
# apply a threshold based on the BGR histogram - more red and less others
ret, T = cv.threshold(img, 130, 255, cv.THRESH_BINARY) # 'eyes' in red with 130 for amostra2.jpg
# now this colored mask has a vivid red
maxLin = T.shape[0] - 1
maxCol = T.shape[1] - 1

#cv.imshow('T', T[:,:,2])
#cv.waitKey(0)
#cv.destroyAllWindows()

i = 0
j = 0
nMales = 0
while i < maxLin:
    #print('i:' + str(i))
    while j < maxCol:
        #print('i: ' + str(i) + 'j: ' + str(j))
        if isMale(i,j,T, maxLin, maxCol):
            print('entrei no macho')
            nMales += 1
        j+=1
    j=0
    i+=1

print('encontrei ' + str(nMales) + 'machos')
