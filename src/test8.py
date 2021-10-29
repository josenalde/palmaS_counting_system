# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 14:24:35 2020

@author: Josenalde
"""

def consultaLista(p, L):
    print(p)
    print(len(L))
    e = 0
    while e < len(L):
        print(e)
        if p in L[e]:
            return True
        else:
            e += 1
    return False
        
L = []
p1 = [1,2]
p2 = [3,4]
p3 = [1,5]
p4 = [6,7]
p5 = [8,4]

L.append(p1)
L.append(p2)
print(L)
if p1 in L:
    print('p1 is in L')
else:
    print('not found')
    
if consultaLista(p5[1], L):
    print('found p1 row in L')
else:
    print('not found in L')
