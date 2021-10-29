# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 16:34:06 2020

@author: Josenalde
"""

#24.06.2020 - ideia: identify redish (brown-red) zones and count them based on some neighborhood

import cv2 as cv
import numpy as np

def writeImg(img, text, color=(255,255,255)):
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(img, text, (10,20), font, 0.6, color, 2, cv.LINE_AA)
    
#by Josenalde Oliveira 24.06.2020
def consultaLista(p, L):
    nb = 2 #neighboorhood
    e = 0
    while e < len(L):
        # test for np = 3
        # t = p+nb in L[e] or p+nb-1 in L[e] or p+nb-2 in L[e] or \
        #     p-nb in L[e] or p-nb+1 in L[e] or p-nb+2 in L[e] or \
        #     p in L[e]
        # # test for np = 2
        t = p+nb in L[e] or p+nb-1 in L[e] or \
            p-nb in L[e] or p-nb+1 in L[e] or \
            p in L[e]
        if (t):
            return True
        else:
            e += 1
    return False
##################################################################
# read image (BGR color)    
img = cv.imread('amostra4.jpg')

# channel equalization does not improve
# img[:,:,0] = cv.equalizeHist(img[:,:,0])
# img[:,:,1] = cv.equalizeHist(img[:,:,1])
# img[:,:,2] = cv.equalizeHist(img[:,:,2])

# apply a threshold based on the BGR histogram - more red and less others
ret, T = cv.threshold(img, 130, 255, cv.THRESH_BINARY) # 'eyes' in red with 130 for amostra2.jpg
# now this colored mask has a vivid red

cv.imshow('T', T)
cv.waitKey(0)
cv.destroyAllWindows()

# desired ranges (only third instar)
rMin = np.array([0, 0, 120]) # B, G, R brown-like
rMax = np.array([0, 0, 255]) # pure red

# apply a binary mask - if v < rMin or v > rMax goes 0, otherwise, goes 255
mask = cv.inRange(T, rMin, rMax)
# invert mask to merge with the original image to plot and save
mask = cv.bitwise_not(mask)

#algorithm to count (estimate) blacks (top of cochonilas)
#by Josenalde Oliveira
nPontosVermelhos = 0
maxLin = T.shape[0] - 1
maxCol = T.shape[1] - 1
cochoMarcadas = []
i = 0
j = 0
x = 0
flagWalk = False #flag to identify if it is 'walking' on a row
while i < maxLin:
    while j < maxCol:
        p = [i,j]
        # check if the current point is 0 (black) and check if the row-nb (up, down) and col-nb (left, right) have not been visited so far
        if (mask[i,j] == 0 and not(consultaLista(p[0], cochoMarcadas)) and not(consultaLista(p[1], cochoMarcadas))): # ponto atual é vermelho
            #insert this point (cochonila into the list)
            cochoMarcadas.append(p)
            nPontosVermelhos += 1
            x = j
            if flagWalk:
                while (x <= maxCol and mask[i,x]==0):
                    testLimits = i+1<=maxLin and i-1>=0 and x+1<=maxCol and x-1>=0
                    if testLimits:
                        x += 1
                        flagWalk = True
                j = x # goes to the next probable red eye (cochonila)
            else:
                j += 1
                flagWalk = False
        else:
            j += 1
    i+=1
    j=0
         

print('Found: ' + str(nPontosVermelhos) + ' cochonilas')

#merge figures (mask and original image) to plot and save
masked = cv.bitwise_and(img, img, mask=mask)
writeImg(masked, "Cochonilas: " + str(nPontosVermelhos))
cv.imshow('palmaS project - UFRN-EMPARN-IB', masked)
#cv.imwrite('resultados/result16.png', masked)
cv.waitKey(0)
cv.destroyAllWindows()
