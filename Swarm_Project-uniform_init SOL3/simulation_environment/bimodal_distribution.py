# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 03:12:01 2020

@author: Paul Vincent Nonat
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
def bimodal_distribution(rho_bar1,sigma1,rho_bar2,sigma2,N,split1,split2):
    dist1=list()
    dist2=list()

        
    while(len(dist1)!=N*split1):
        s=np.random.normal(rho_bar1,sigma1)
        if s>=0:
            dist1.append(s)
    
    while(len(dist2)!=N*split2):
        s=np.random.normal(rho_bar2,sigma2)
        if s>=0:
            dist2.append(s)
    
    rho_k =dist1 +dist2
    plt.hist(rho_k,30,density=True)
    sns.distplot(rho_k, hist=False)
    plt.show()
    return rho_k