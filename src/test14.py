# -*- coding: utf-8 -*-
"""
Created on Fri Jul 08 16:34:06 2020

@author: Josenalde
"""

import cv2 as cv
#import matplotlib.pyplot as plt
import mahotas as mh #otsu
import numpy as np

def writeImg(img, text, color=(255,255,255)):
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(img, text, (10,20), font, 0.6, color, 2, cv.LINE_AA)

bgr = cv.imread('amostra1.jpeg') #if male were more white than female, ok

# circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,10,
#                             param1=50,param2=12,minRadius=0,maxRadius=20)

# circles = np.uint16(np.around(circles))
# for i in circles[0,:]:
#     # draw the outer circle
#     cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#     # draw the center of the circle
#     cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

# cv2.imshow('detected circles',cimg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# l = (200,200,255)
# h = (0,0,255)

#bordas = cv.inRange(bgr, h, l)
BLUR = 35
# CANNY_TH1 = 10
# CANNY_TH2 = 70

bgrF = cv.medianBlur(bgr, BLUR) #31 122, 35 125, 39 126, 51 128
# 52 lost females

# bordas = cv.Canny(bgr, CANNY_TH1, CANNY_TH2) 
# bordas = cv.dilate(bordas, None)
# bordas = cv.erode(bordas, None)
# cv.imshow('bordas canny', bordas)
# cv.waitKey(0)
# cv.destroyAllWindows()


hsv = cv.cvtColor(bgrF, cv.COLOR_BGR2HSV)
hsv[:,:,0] = cv.equalizeHist(hsv[:,:,0])
bgr2 = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
gray = cv.cvtColor(bgr2, cv.COLOR_BGR2GRAY)


# cv.imshow('HSV image', bgr)
# cv.waitKey(0)
# cv.destroyAllWindows()

#desaturation - convert bgr to gray

#color systems usually related to plant disease detection - rgb and hsv

# Hue, Saturation, Value
# Hue: dominant wavelength, S: purity, color proportion, V: brightness, intensity of the reflected color

# segmentation based on shape, pixels (color), histogram
# binary segmentation - binarization, thresholding

# moda is a more frequent value in a sequence - unimodal, bimodal etc.

#hist1 = cv.calcHist([gray],[0],None,[256],[0,260]) #unimodal
#manual
#ret, th1 = cv.threshold(gray, 120, 255, cv.THRESH_BINARY)
#auto otsu
#can be applied to uni e bimodal histograms
th2 = mh.thresholding.otsu(gray)
#print(th2)
bin = gray.copy()
bin[bin >= th2] = 255
bin[bin < th2] = 0
bin = cv.bitwise_not(bin)
#hist2 = cv.calcHist([th2],[0],None,[256],[0,260]) #unimodal

masked = cv.bitwise_and(bgr, bgr, mask=bin)

#plt.subplot(1,2,1)
#plt.plot(hist1)
#plt.xlim([0,256])
#plt.subplot(1,2,2)
#plt.plot(hist2)
#plt.xlim([0,256])
#plt.show()

# calculo aproximado estimativa de pixels pretos = cochonila geral
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

# amostra1
#100mm - 780 px : 
wRatio = 780 / 100 #px/mm 
#125mm - 1040 px : 
hRatio = 1040 / 125 #px/mm          
            
print('Area acumulada em Pixels = ' + str(nPixelsPretos))
totalPixels = bin.shape[0] * bin.shape[1]

# counts everything detected - female and male presence all stages
percentCochonila = (nPixelsPretos / totalPixels) * 100

# key info (literature?)
#mRadio = 27 #raio medio das cochonilas na amostra -3 instar
#MRadio =
# ellipse area = mr x Mr x PI
# some cases equals mR = MR = r
# translate to px, considering the zoom
zoom = 5
scales = [wRatio, hRatio]
r1 = (1.5/2) * zoom * np.mean(scales)
r2 = (2.5/2) * zoom * np.mean(scales)

nCochonilas1 = nPixelsPretos / (3.14 * r1*r1)
nCochonilas2 = nPixelsPretos / (3.14 * r2*r2)

contagemManual = 131 #ground truth
#erro = (abs(nCochonilas - contagemManual) / contagemManual) * 100
print(round(nCochonilas1))
print(round(nCochonilas2))
print('presence of cochonila: %.2f' % percentCochonila + '\%')
#print('Erro percentual manual x automatico: %.2f' % erro)

#writeImg(masked, "Cochonilas femeas: " + str(round(nCochonilas)))
#cv.imshow('palmaS - cochonilas femeas', masked)
#cv.waitKey(0)
#cv.destroyAllWindows()
#cv.imwrite('resultados/teste14blur5amostra1.png', masked)




# segmentation by border detection - abrupt variation gray scale (canny)

# segmentation by region (Sobel and Watershed) - group similar pixels

# feature extraction (reduce information to more concise and representative data)
#  cor, forma, tamanho, textura 





