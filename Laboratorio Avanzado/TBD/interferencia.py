import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage[version = 4]{mhchem} \usepackage{physics}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

data = np.genfromtxt("DatosInterferencia_limpio.txt")

def I(theta, I_0, q, w):
	return I_0*(1+np.exp(-2*theta*theta/(w*w))*np.cos(2*q*theta+np.pi))/2

popt, pcov = curve_fit(I, data[:,0], data[:,1])
print(popt)

fig, ax = plt.subplots()

ax.errorbar(data[:,0], data[:,1], xerr = 0.005, yerr = 5, fmt = "o", c = "k", ms = 3)
ax.set_xlabel(r"$\theta(\si{\degree})$")
ax.set_ylabel(r"$I(\text{A.U.})$")

theta = np.linspace(-1.5,1.5,1000)
ax.plot(theta, I(theta, *popt))

fig.savefig("interferencia.png")
plt.close(fig)
