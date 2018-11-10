import numpy as np
import matplotlib.pyplot as plt
from uncertainties import ufloat
import uncertainties.unumpy as unp

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage{physics} \sisetup{round-mode = figures} \sisetup{round-precision = 3}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

fit = np.load("calibracion.npy")

I_B = [0, 0.32, 0.6, 0.82, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6]
data = np.array([np.genfromtxt("actividad_3_%.1f.txt" % I) for I in I_B])
B = [ufloat(fit[0],1)*ufloat(I,0.01) + ufloat(fit[1],1) for I in I_B]
B_nom = np.array([b.nominal_value for b in B])
R = np.zeros(len(B))
sigma_R = np.zeros(len(B))

for i in range(0,len(B)):
	data[i][:,1] = -data[i][:,1]
	fit = np.polyfit(data[i][:,0], data[i][:,1], 1)
	sigma_V = np.sqrt(np.sum((data[i][:,1]-fit[1]-fit[0]*data[i][:,0])**2)/(len(data[i])-2))
	Delta = len(data[i])*np.sum(data[i][:,0]**2)-np.sum(data[i][:,0])**2
	sigma_pendiente = sigma_V*np.sqrt(len(data[i])/Delta)
	R[i] = fit[0]
	sigma_R[i] = sigma_pendiente 

R = unp.uarray(R, sigma_R)
R = (R-R[0])/R[0]
R_nom = np.array([r.nominal_value for r in R])

fig, ax = plt.subplots()
ax.errorbar(B_nom, R_nom, xerr = [b.std_dev for b in B], yerr = [r.std_dev for r in R], fmt = "o", c = "k")
ax.set_xlabel(r"$B(\si{\milli\tesla})$")
ax.set_ylabel(r"$\frac{R_m-R_0}{R_0}$")
ax.set_title(r"Magnetoresistencia")
fig.savefig("resistencia_longitudinal.png")
plt.close(fig)
