# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 09:47:51 2020

@author: Paul Vincent Nonat
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


labels = [r'$\sigma=10$', r'$\sigma=20$', r'$\sigma=30$',r'$\sigma=40$', r'$\sigma=50$']
sol1 = [796.75, 1440.5, 1817, 1135.5, 1385.33]
sol2 = [651.5, 913, 941.67, 492.75, 1244.75]
sol3 = [545.25, 1817, 1207.5, 703.5, 1806.25]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/3, sol1, width, label='Sol1')
rects2 = ax.bar(x + width/2, sol2, width, label='Sol2')
rects3 = ax.bar(x + width, sol3, width, label='Sol3')
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Average Time step')
ax.set_title(r' Number of timestep to $\frac{\partial \ln U_{MA} }{\partial t} < \epsilon$')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


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