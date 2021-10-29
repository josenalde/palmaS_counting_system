# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 16:34:06 2020

@author: Josenalde
"""

import cv2 as cv
import numpy as np

def writeImg(img, text, color=(255,255,255)):
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(img, text, (10,20), font, 0.6, color, 2, cv.LINE_AA)

#read from filesystem - glade 
bgr = cv.imread('amostra1_5.png') #if male were more white than female, ok
bgr = cv.resize(bgr, (780, 1040)) #restrict area

BLUR = 17

bgrF = cv.medianBlur(bgr, BLUR) # filter

#color systems usually related to plant disease detection - rgb and hsv
# Hue, Saturation, Value
# Hue: dominant wavelength, S: purity, color proportion, V: brightness, intensity of the reflected color

hsv = cv.cvtColor(bgrF, cv.COLOR_BGR2HSV) #convert to HSV
hsv[:,:,0] = cv.equalizeHist(hsv[:,:,0])  #equalization H channel
bgr2 = cv.cvtColor(hsv, cv.COLOR_HSV2BGR) #back conversion to BGR

#desaturation - convert bgr to gray
gray = cv.cvtColor(bgr2, cv.COLOR_BGR2GRAY)



#auto otsu
#can be applied to uni e bimodal histograms
# segmentation based on shape, pixels (color), histogram
# binary segmentation - binarization, thresholding

ret,th = cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

bin = gray.copy()
bin[bin >= ret] = 255
bin[bin < ret] = 0
bin = cv.bitwise_not(bin)
masked = cv.bitwise_and(bgr, bgr, mask=bin)

# sum all black pixels (integral)
nPixelsPretos = 0
for i in range(bin.shape[0]):
    for j in range(bin.shape[1]):
        if bin[i,j] == 0:
            nPixelsPretos += 1

#according to Bouché 1833
#16.07.2020 retrieved
#https://diaspididae.linnaeus.naturalis.nl/linnaeus_ng/app/views/species/taxon.php?id=113071&epi=155
#scale cover of adult female (3. instar) 1.5-2.5 mm diameter
#The first instar female and first and second instar male nymphs were described by Howell, 1975, and Howell and Tippins, 1977.
# elliptical
# first stage - female 258-308 long, 168-199 wide um
# second stage - Length of slide-mounted specimens 378-607, width 263-378.
#Descriptions of Some Immature Stages in Two Diaspis Species, 1975 Howell
            
#Descriptions of First Instars of Nominal Type-Species of Eight Diaspidid Tribes
#Howell, J. O., Tippins, H. H., 1977

#from https://www.unitconverters.net/typography/pixel-x-to-millimeter.htm
pxBase = 0.2645833333 #mm

# amostra1 - zoom and size must be controlled
 
wmm = bin.shape[1] * pxBase
hmm = bin.shape[0] * pxBase
wRatio = bin.shape[1] / wmm #px/mm 
hRatio = bin.shape[0] / hmm #px/mm        
#same scale H and V  
            
totalPixels = bin.shape[0] * bin.shape[1]

# counts everything detected - female and male presence all stages
percentCochonila = (nPixelsPretos / totalPixels) * 100

zoom = 9 #IT IS NONLINEAR (fixed, depends on the camera etc.)

scales = [wRatio, hRatio]

# using the lower diameter range 1.5 mm of an adult female (3. stage) 
r1 = (1.5/2) * zoom * np.mean(scales) # convert mm to px, considering zoom

# here it is an approximation, since only the third instar is considered
nCochonilas = nPixelsPretos / (3.14 * r1*r1)

print(round(nCochonilas))
print('presence of cochonila: %.2f' % percentCochonila + '\%')

writeImg(masked, "Cochonilas femeas: " + str(round(nCochonilas)))
cv.imshow('palmaS - cochonilas femeas', masked)
cv.waitKey(0)
cv.destroyAllWindows()
cv.imwrite('resultados/teste15amostra1_5.png', masked)







