# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 16:34:06 2020

@author: Josenalde
"""

#http://professor.luzerna.ifc.edu.br/ricardo-antonello/wp-content/uploads/sites/8/2017/02/Livro-Introdu%C3%A7%C3%A3o-a-Vis%C3%A3o-Computacional-com-Python-e-OpenCV-3.pdf

import cv2 as cv
import matplotlib.pyplot as plt
#import numpy as np
import mahotas as mh

# parameters

BLUR = 9
CANNY_TH1 = 10
CANNY_TH2 = 200
MASK_DILATE_ITER = 10
MASK_ERODE_ITER = 10
MASK_COLOR = (0.0, 0.0, 0.0) #black
  
def escreve(img, texto, cor=(255,0,0)):
    fonte = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(img, texto, (10,20), fonte, 0.5, cor, 0, cv.LINE_AA)

imgColor = cv.imread('amostra1.jpeg')
#imgColor[:,:,1] = 0 #without green channel
#converter para tons de cinza
#imgHsv = cv.cvtColor(imgColor, cv.COLOR_BGR2HSV)

# retirar canal verde
#cv.imshow('with HSV', imgHsv)
#cv.waitKey(0)
#cv.destroyAllWindows()
#cv.imshow('img gray', imgGray)
#cv.waitKey(0)
#cv.destroyAllWindows()

#suaviza para facilitar algoritmo detectar cordas
imgSmooth = cv.medianBlur(imgColor, 9)
#imgSmooth = cv.GaussianBlur(imgColor, (9,9), 0)
#converter para tons de cinza
imgGray = cv.cvtColor(imgSmooth, cv.COLOR_BGR2GRAY)

#imgSmooth = cv.medianBlur(imgGray, 9)

#Passo 3: Binarização resultando em pixels brancos e pretos
T = mh.thresholding.otsu(imgSmooth)
bin = imgGray.copy()
bin[bin > T] = 255
bin[bin < 255] = 0
#bin = cv.bitwise_not(bin)

#ret, bin = cv.threshold(imgGray, 178, 255, cv.THRESH_BINARY)
#bin = cv.bitwise_not(bin)
#cv.imshow('mask', bin)
#cv.waitKey(0)
#cv.destroyAllWindows()

#Passo 4: Detecção de bordas com Canny
bordas = cv.Canny(bin, 10, 50) #nao foi observado influencia de th1 e th2

  
#Passo 5: Identificação e contagem dos contornos da imagem
#cv2.RETR_EXTERNAL = conta apenas os contornos externos
# contours – Detected contours. Each contour is stored as a vector of points.

imgC2 = imgColor.copy()

# X contornos encontrados, onde cada contorno tem uma lista de dimensões x, y de um pixel
objetos = cv.findContours(bordas.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
objetos = objetos[0] if len(objetos)==2 else objetos[1]
    
npontos = len(objetos)
i = 0
nRets = 0
listRets = list()
while (i < npontos):
    #print(objetos[i].size)
    if (objetos[i].size <= 1): # como escolher o numero de pontos para descartar?
        listRets.append(i) #insere este objeto parecido com retangulo
        nRets+=1
    i+=1

print(nRets)

# remove retangulos da lista (machos?)

for i in range(len(listRets)):
    objetos.pop(i)

s = 0
for c in objetos:
    s += len(c)
    cv.drawContours(imgC2,[c], -1,(255,0,0),2)
    
print(s)

totPixelsGray = imgGray.shape[0] * imgGray.shape[1]
percentCochonila = (s / totPixelsGray) * 100
print('presence of cochonila: %.2f' % percentCochonila)
    
# escreve(imgGray, "Imagem em tons de cinza", 0)
# escreve(imgSmooth, "Suavizacao com Blur", 0)
# escreve(bin, "Binarizacao com Metodo Otsu", 255)
# escreve(bordas, "Detector de bordas Canny", 255)

# temp = np.vstack([np.hstack([imgGray, imgSmooth]), np.hstack([bin, bordas])])
# cv.imshow("Quantidade de objetos: "+ str(len(objetos)), temp)
# cv.waitKey(0)
# imgC2 = imgColor.copy()
# cv.imshow("Imagem Original", imgColor)

# cv.drawContours(imgC2, objetos, -1, (255, 0, 0), 2)
print(str(len(objetos)) + 'objetos encontrados!')
escreve(imgC2, str(len(objetos))+" objetos encontrados!")
#plt.subplot(2,1,1)
plt.imshow(imgC2)
#plt.subplot(2,1,2)
#plt.imshow(bin)
plt.show()
#cv.imshow("Resultado", imgC2)
cv.waitKey(0)
cv.destroyAllWindows()

#pointPolygonTest()

