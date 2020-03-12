# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 17:30:13 2020

@author: Paul Vincent Nonat
"""

#prefered distance from truncated normal distribution about 0 to infinity
import numpy as np
import matplotlib.pyplot as plt

N=1000
mu, sigma = 10, 20
rho_k=list()

while (len(rho_k)!=N):
    
    s= np.random.normal(sigma,mu)
    if s > 0:
        rho_k.append(s)


plt.hist(rho_k,30,density = True)

plt.show()