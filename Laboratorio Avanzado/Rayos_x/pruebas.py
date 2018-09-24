import numpy as np
from uncertainties import ufloat

x = np.array([ufloat(x,np.random.random()) for x in np.linspace(1,10,10)])
y = np.array([3*x+1 for i in range(0,5)])
b = [((x*x).sum()*y[i].sum()-x.sum()*(x*y[i]).sum())/(np.array(10)*(x*x).sum()-x.sum()**2) for i in range(0,5)]
m = [(np.array(10))
print(b)
