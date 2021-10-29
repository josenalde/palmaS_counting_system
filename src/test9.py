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

# parameters

BLUR = 9
CANNY_TH1 = 10
CANNY_TH2 = 200
MASK_DILATE_ITER = 2
MASK_ERODE_ITER = 10
#MASK_COLOR = (0.0, 0.0, 0.0) #black

#by Josenalde Oliveira 23.06.2020
def consultaLista(p, L):
    nb = 3 #neighboorhood
    e = 0
    while e < len(L):
        #print(e)
       # for t in range(nb):
        #if p in L[e]:    
        t = p+nb in L[e] or p+nb-1 in L[e] or p+nb-2 in L[e] or \
            p-nb in L[e] or p-nb+1 in L[e] or p-nb+2 in L[e] or \
            p in L[e]
        if (t):
            return True
        else:
            e += 1
    return False
        

img = cv.imread('amostra4.jpg')

# bordas = cv.Canny(imgSmooth, CANNY_TH1, CANNY_TH2) 
# bordas = cv.dilate(bordas, None)
# bordas = cv.erode(bordas, None)
# cv.imshow('bordas canny', bordas)
# cv.waitKey(0)
# cv.destroyAllWindows()

#bordas_info = []

# contornos = cv.findContours(bordas, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# contornos = contornos[0] if len(contornos)==2 else contornos[1]
# areaContornos = 0
# for c in contornos:
#     #bordas_info.append((c, cv.isContourConvex(c), cv.contourArea(c)))
#     areaContornos += cv.contourArea(c)   

# areaContornos = areaContornos / len(contornos)
# print(areaContornos)    

#img = cv.medianBlur(img, BLUR)
# color = ('b','g','r')
# for i,col in enumerate(color):
#     histr = cv.calcHist([img],[i],None,[256],[0,256])
#     plt.plot(histr,color = col)
#     plt.xlim([0,256])
#plt.show()

ret, T = cv.threshold(img, 130, 255, cv.THRESH_BINARY) # 'olhos' em vermelho com 130

#conta os vermelhos (olhos!!)
# nPontosVermelhos = 0
# maxLin = T.shape[0] - 1
# maxCol = T.shape[1] - 1
# cochoMarcadas = []
# i = 0
# j = 0
# x = 0
# flagWalk = False
# while i < maxLin:
#     while j < maxCol:
#         #print(cochoMarcadas)
#         #print('i fora' + str(i))
#         #print('j fora' + str(j))
#         p = [i,j]
#         #print(consultaLista(i, cochoMarcadas))
#         #print(cochoMarcadas)
#         if (T[i,j,2] == 255 and not(consultaLista(p[0], cochoMarcadas)) and not(consultaLista(p[1], cochoMarcadas))): # ponto atual é vermelho
#             #insere posicao da cochonila na lista
#             cochoMarcadas.append(p)
#             nPontosVermelhos += 1
#             # testa se não algum extremo
#             x = j
#             #print('i se for cadastrar' + str(i))
#             #print('j se for cadastrar' + str(j))
#             if flagWalk:
#                 while (x <= maxCol and T[i,x,2]==255):
#                     testLimites = i+1<=maxLin and i-1>=0 and x+1<=maxCol and x-1>=0
#                     if testLimites:
#                         x += 1
#                         flagWalk = True
#                 j = x # reinicia varredura do proximo vermelho com maior chance de ser cochonila
#             else:
#                 j += 1
#                 flagWalk = False
#                 # ve vizinhos para tras e para frente
#                 #vE = T[i, j-1, 2] #esquerda
#                 #vD = T[i, j+1, 2] #direita
#                 #vC = T[i-1, j, 2] #cima
#                 #vB = T[i+1, j, 2] #baixo
#                 #if (vE==255 or vD==255 or vC==255 or vB==255):
#                 #     nPontosVermelhos += 1
#                 #else:
#                 #    continue
#         else:
#             j += 1
#     i+=1
#     j=0
         

# print('encontrei ' + str(nPontosVermelhos))
# marrom puro é R 128, G 0 B 0, ao usar mascara o marrom passou a 255 0 0

imgG = cv.cvtColor(T, cv.COLOR_BGR2GRAY)
#imgSmooth = cv.medianBlur(imgG.copy(), BLUR)

# R 300000 pixels, G 250000, B  150000
# histr = cv.calcHist([T],[0],None,[256],[0,260])
# plt.plot(histr)
# plt.xlim([0,256])
# plt.show()

#circles = cv.HoughCircles(imgSmooth, cv.HOUGH_GRADIENT, 50, 100, param1=10, param2=200,minRadius=0, maxRadius=0)

# print(circles.size / 3)
# for i in circles[0,:]:
#     # outer 
#     cv.circle(img, (i[0], i[1]), i[2], (0,255,0), 2)
#     # center
#     cv.circle(img, (i[0], i[1]), 2, (0,0,255), 5)


    
ret2, T2 = cv.threshold(imgG, 70, 255, cv.THRESH_BINARY_INV) # 'area preta'
masked = cv.bitwise_and(img, img, mask=T2)

cv.imshow('circles', T2)
cv.waitKey(0)
cv.destroyAllWindows()

# calculo aproximado estimativa de pixels pretos = cochonila geral
nPixelsPretos = 0
for i in range(T2.shape[0]):
    for j in range(T2.shape[1]):
        if T2[i,j] == 0:
            nPixelsPretos += 1

print('Area acumulada em Pixels = ' + str(nPixelsPretos))
totalPixels = T2.shape[0] * T2.shape[1]
percentCochonila = (nPixelsPretos / totalPixels) * 100
area = (2 * 2.5 * percentCochonila)/100 # area da captura da amostra
raio = 27 #raio medio das cochonilas na amostra
nCochonilas = nPixelsPretos / (3.14 * raio*raio)
contagemManual = 131
erro = (abs(nCochonilas - contagemManual) / contagemManual) * 100
print('numero estimado de cochonilas: %d' % nCochonilas)
print('presence of cochonila: %.2f' % percentCochonila + '\%')
print('equivalente a area da amostra de: %.2f' % area + ' centimetros quadrados')
print('Erro percentual manual x automatico: %.2f' % erro)
# eliminando em 50 botao, coloca o vermelho e verde em 255 - fica amarelo o campo
# eliminando em 180 botao, campo fica verde bem escuro

# color = ('b','g','r')
# for i,col in enumerate(color):
#     histr = cv.calcHist([T],[i],None,[256],[0,256])
#     plt.plot(histr,color = col)
#     plt.xlim([0,256])
#plt.show()

cv.imshow('mask', masked)
cv.waitKey(0)
cv.destroyAllWindows()
#cv.imwrite('resultados/result17.png', masked)
