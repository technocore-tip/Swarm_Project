# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 09:47:51 2020

@author: Paul Vincent Nonat
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


labels = ['Year 1','Year 2','Year 3','Year 4','Year 5']
Sales = [3111069.28,4572138.56,5397138.56,11729872.40,20323005.20]
Expenses = [2002221.39,2031442.77,2047942.77,2174597.45,2346460.10]
investment=[5000000,5000000,5000000,5000000,5000000]
Income=[Sales[0],Sales[0]+Sales[1],Sales[0]+Sales[1]+Sales[2],+Sales[0]+Sales[1]+Sales[2]+Sales[3],+Sales[0]+Sales[1]+Sales[2]+Sales[3]+Sales[4]]
x=[1,2,3,4,5]
net_profit=[Sales[0]-Expenses[0],Sales[1]-Expenses[1],Sales[2]-Expenses[2],Sales[3]-Expenses[3],Sales[4]-Expenses[4]]
x = np.arange(len(labels))  # the label locations
width = 0.3  # the width of the bars

Total_cost=[5000000+2002221.39,5000000+2002221.39+2031442.77,5000000+2002221.39+2031442.77+2047942.77,5000000+2002221.39+2031442.77+2047942.77+2047942.77]
fig, ax = plt.subplots()
rects4 = ax.plot(x,net_profit,label='Net Profit',color='black')
rects4 = ax.scatter(x,net_profit,color='black')


#rects5 = ax.plot(x,Total_cost,color='red',label='Cost')
#rects6 = ax.plot(x,Income,color='blue',label='Income')
ax.bar(x, Sales, width, label='Projected Annual Revenue',color='g')
ax.bar(x, Expenses, width, label='Projected Annual Expenditure',color='grey')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('PHP')
ax.set_title(r'Projected Performance')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc=2)


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    #xy=(rect.get_x() + rect.get_width() / 3, height),
                    #xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


#autolabel(rects1)
#autolabel(rects2)
#autolabel(rects3)
fig.tight_layout()

plt.savefig('Numbe of Timestep.png', dpi=500)
plt.show()
#
#total_profit=[1108847.89,3649543.68,6998739.47,10347935.26]
#ROI=[-77.82,-22.01,39.97,106.96]
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.plot(x,total_profit)
#ax.plot(x,investment)
#
#ax2 = ax.twinx()
#ax2.plot(x, ROI, '-r', label = 'temp')
#ax.legend(loc=0)
#ax.grid()
#ax.set_xlabel("Time (h)")
#ax.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")
#ax2.set_ylabel(r"Temperature ($^\circ$C)")
#ax2.set_ylim(-100,100)
#ax.set_ylim(0,10000000)
#plt.show()