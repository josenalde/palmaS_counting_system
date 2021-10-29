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
    nb = 5
    if (pi+nb<maxLin and pj+nb<maxCol):
        if (M[pi,pj,2] == 255): #if current pixel is white
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
    
    
#by Josenalde Oliveira 06.07.2020
# def scanList(p, L):
#     nb = 2 #neighboorhood
#     e = 0
#     while e < len(L):
#         # test for np = 3
#         # t = p+nb in L[e] or p+nb-1 in L[e] or p+nb-2 in L[e] or \
#         #     p-nb in L[e] or p-nb+1 in L[e] or p-nb+2 in L[e] or \
#         #     p in L[e]
#         # # test for np = 2
#         t = p+nb in L[e] or p+nb-1 in L[e] or \
#             p-nb in L[e] or p-nb+1 in L[e] or \
#             p in L[e]
#         if (t):
#             return True
#         else:
#             e += 1
#     return False

#by Josenalde Oliveira 06.07.2020
def scanList(p, L):
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

img = cv.imread('amostra1.jpeg')

# HISTOGRAM
# color = ('b','g','r')
# for i,col in enumerate(color):
#     histr = cv.calcHist([img],[i],None,[256],[0,256])
#     plt.plot(histr,color = col)
#     plt.xlim([0,256])
#plt.show()

# a linear threshold on all channels
ret, T = cv.threshold(img, 130, 255, cv.THRESH_BINARY) # 'eyes' in red with 130

# count reds (eyes!!)
nPontosVermelhos = 0
maxLin = T.shape[0] - 1
maxCol = T.shape[1] - 1
#print(maxLin)
#print(maxCol)
cochoMarcadas = []
i = -1
j = 0
x = 0
nMales = 0
flagWalk = False
while i < maxLin:
    i+=1
    j=0
    while j < maxCol:
        if (not isMale(i,j,T, maxLin, maxCol) and not(scanList(i, cochoMarcadas)) and not(scanList(j, cochoMarcadas))):
         
            #print('i: ' + str(i))
            #print('j: ' + str(j))
            #print(j)
            p = [i,j]
            if (T[i,j,2] == 255 and not(scanList(p[0], cochoMarcadas)) and not(scanList(p[1], cochoMarcadas))): # ponto atual é vermelho
                
                #print('entrei pra testar')
                #insere posicao da cochonila na lista
                cochoMarcadas.append(p)
                nPontosVermelhos += 1
                # testa se não algum extremo
                x = j
                #print('i se for cadastrar' + str(i))
                #print('j se for cadastrar' + str(j))
                if flagWalk:
                    while (x <= maxCol and T[i,x,2]==255):
                        testLimites = i+1<=maxLin and i-1>=0 and x+1<=maxCol and x-1>=0
                        if testLimites:
                            x += 1
                            flagWalk = True
                    j = x # reinicia varredura do proximo vermelho com maior chance de ser cochonila
                else:
                    j += 1
                    flagWalk = False
            else:
                nMales += 1
                j+=1
   
        else:
            j+=1
         

print('encontrei ' + str(nPontosVermelhos) + 'e ' + str(nMales) + 'machos ')
# marrom puro é R 128, G 0 B 0, ao usar mascara o marrom passou a 255 0 0

imgG = cv.cvtColor(T, cv.COLOR_BGR2GRAY)
#imgSmooth = cv.medianBlur(imgG.copy(), BLUR)

# R 300000 pixels, G 250000, B  150000
# histr = cv.calcHist([T],[0],None,[256],[0,260])
# plt.plot(histr)
# plt.xlim([0,256])
# plt.show()

ret2, T2 = cv.threshold(imgG, 1, 255, cv.THRESH_BINARY_INV) # 'area preta'
masked = cv.bitwise_and(img, img, mask=T2)



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


cv.imshow('mask', T2)
cv.waitKey(0)
cv.destroyAllWindows()
#cv.imwrite('resultados/result17.png', masked)
