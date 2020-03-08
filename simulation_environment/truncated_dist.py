# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 14:22:02 2020

@author: Paul Vincent Nonat
"""

from scipy.stats import truncnorm
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1)

a, b = 0, np.inf
mean, var, skew, kurt = truncnorm.stats(a, b, moments='mvsk')

x = np.linspace(truncnorm.ppf(0, a, b),truncnorm.ppf(0.99, a, b), 100)

ax.plot(x, truncnorm.pdf(x, a, b),'r-', lw=5, alpha=1, label='truncnorm pdf')
mean=2
rv = truncnorm(a, b)

ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

vals = truncnorm.ppf([0.1, 0.1,b], a, b)

np.allclose([0.0001, 1.5, 2], truncnorm.cdf(vals, a, b))

r = truncnorm.rvs(a, b, size=1000)

ax.hist(r, density=True, histtype='stepfilled', alpha=1)
ax.legend(loc='best', frameon=False)
plt.show()
plt.plot(r)

mu,sigma = 10, 0.1
s= np.random.normal(mu,0,1000)