import numpy as np
import matplotlib.pyplot as plt
from uncertainties import ufloat

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage{physics} \sisetup{round-mode = figures} \sisetup{round-precision = 3}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

fit = np.load("calibracion.npy")
I_p = np.array([-20,-12,14,22,30])
data = np.array([np.genfromtxt("actividad_2_%d.txt" % I) for I in I_p])
print(data.shape)
B = [[-ufloat(fit[0],1)*ufloat(I_B,0.01) - ufloat(fit[1],1) for I_B in data[i][:,0]] for i in range(0,len(data))]
B_nom = np.array([np.array([b.nominal_value for b in B[i]]) for i in range(0,len(B))])

fit = np.array([np.polyfit(B_nom[i], data[i][:,1], 1) for i in range(0,len(B))])
sigma_V = sigma_B
