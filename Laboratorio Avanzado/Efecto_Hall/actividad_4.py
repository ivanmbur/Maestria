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
ax.errorbar(1/(data[:,0]+273.15), 30/data[:,1], xerr = [b.std_dev for b in beta], yerr = [s.std_dev for s in sigma], fmt = "o", alpha = 0.07, c = "k")
ax.plot(1/(data[15:200,0]+273.15), f(data[15:200,0], *fit), c = "k")
ax.set_xlabel(r"$1/T(\si{\per\kelvin})$")
ax.set_ylabel(r"$1/R(\si{\per\ohm})$")
ax.set_title(r"Termoresistencia longitudinal")
fig.savefig("termoresistencia.png")
plt.close(fig)

data = np.genfromtxt("actividad_4_2.txt")
data[:,1] = -data[:,1]
fit = np.load("calibracion.npy")

B = ufloat(1.87,0.001)*ufloat(fit[0],1)+ufloat(fit[1],1)
print("Se utilizó un campo de %s" % B.format(".1u"))

R_H = [ufloat(data[i,1],0.1)*0.001/(ufloat(30,1)*B/1000) for i in range(0,len(data))]
R_H_nom = np.array([r.nominal_value for r in R_H])
R_H_std = np.array([r.std_dev for r in R_H])

fig, ax = plt.subplots()
ax.errorbar(data[:,0]+273.15, R_H_nom*1000, xerr = 0.5, yerr = R_H_std*1000, fmt = "o", alpha = 0.3, c = "k")
ax.set_xlabel(r"$T(\si{\kelvin})$")
ax.set_ylabel(r"$R_H(10^{-3}\si{m^3\per\coulomb})$")
ax.set_title(r"Variaci\'on en portadores")
fig.savefig("concentracion_portadores.png")
plt.close(fig)  

beta = [1/(ufloat(T,0.5)+273.15) for T in data[:,0]]
beta_nom = np.array([b.nominal_value for b in beta])
beta_std = np.array([b.std_dev for b in beta])
Y = [log(R_H[i]*ufloat(data[i,0],0.5)**(3.0/2.0)) for i in range(0,len(R_H))]
Y_nom = np.array([y.nominal_value for y in Y])
Y_std = np.array([y.std_dev for y in Y])

fit, cov = np.polyfit(beta_nom[30:], Y_nom[30:], 1, cov = True)
cov = np.sqrt(np.diag(cov))
E_g = 2*k*ufloat(fit[0], cov[0])

print("Se encontró un gap de %s" % E_g.format(".1uL"))

fig, ax = plt.subplots()
ax.errorbar(beta_nom, Y_nom, xerr = beta_std, yerr = Y_std, fmt = "o", alpha = 0.3, c = "k")
ax.plot(beta_nom[30:], fit[0]*beta_nom[30:]+fit[1], c="k")
ax.set_xlabel(r"$1/T(\si{\per\kelvin})$")
ax.set_ylabel(r"$\ln(R_H T^{3/2})$")
ax.set_title(r"Termoresistencia Hall")
fig.savefig("gap_energia.png")
plt.close(fig)  
