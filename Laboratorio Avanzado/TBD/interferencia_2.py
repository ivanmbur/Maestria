import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage[version = 4]{mhchem} \usepackage{physics}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

def I(angle, offset, I_0, w, q, phi):
	theta = angle-offset
	return I_0*(1 + np.exp(-2*theta*theta/w)*np.cos(2*q*theta + phi))/2

data = np.genfromtxt("interferencia.txt", usecols = (0, 1))

angles = np.linspace(np.min(data[:,0]),np.max(data[:,0]),1000)
popt, pcov = curve_fit(I, data[:,0], data[:,1], p0 = [0.53, np.max(data[:,1]), 8, 8.7, np.pi])
print(popt)

fig, ax = plt.subplots()
ax.scatter(data[:,0], data[:,1], c = "k", alpha = 0.3)
ax.plot(angles, I(angles, *popt), c = "k")
ax.set_xlabel(r"$\theta(\si{\degree})$")
ax.set_ylabel(r"$I(\si{\micro\watt})$")
ax.set_title(r"Patr\'on de Interferencia")
fig.savefig("interferencia_2.png")
plt.close(fig)
