import numpy as np
import matplotlib.pyplot as plt
from uncertainties import ufloat
import uncertainties.unumpy as unp
from uncertainties.umath import *
from scipy.optimize import curve_fit

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage{physics} \sisetup{round-mode = figures} \sisetup{round-precision = 3}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

k = ufloat(8.6173303,0.0000050)*1E-5

def f(T, sigma_0, E):
	return sigma_0*np.exp(-E/(k.nominal_value*(T+273.15)))	

data = np.genfromtxt("actividad_4_1.txt")

fit, cov = curve_fit(f, data[15:200,0], 30/data[15:200,1], p0=[26,0.265])
err = np.sqrt(np.diag(cov))
print("Se obtuvo [simga_0, E] = [%f, %f] con errores [%f,%f]" % (fit[0], fit[1], err[0], err[1]))

beta = [1/(ufloat(T,1)+213.15) for T in data[:,0]] 
sigma = [ufloat(30,0.1)/ufloat(V,0.001) for V in data[:,1]]

fig, ax = plt.subplots()
ax.errorbar(1/(data[:,0]+273.15), 30/data[:,1], xerr = [b.std_dev for b in beta], yerr = [s.std_dev for s in sigma], fmt = "o", alpha = 0.1)
ax.plot(1/(data[15:200,0]+273.15), f(data[15:200,0], *fit))
ax.set_xlabel(r"$1/T(\si{\per\kelvin})$")
ax.set_ylabel(r"$1/R(\si{\per\ohm})$")
ax.set_title(r"Termoresistencia")
fig.savefig("termoresistencia.png")
plt.close(fig)

data = np.genfromtxt("actividad_4_2.txt")
fit = np.load("calibracion.npy")

B = ufloat(1.87,0.001)*ufloat(fit[0],1)+ufoat(fit[1],1)
print("Se utilizó un campo de %s" % B.format(".1u"))

R_H = [ufloat(data[:,1],0.*0.001/(30*B)
