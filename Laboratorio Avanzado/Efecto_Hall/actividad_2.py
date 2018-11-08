import numpy as np
import matplotlib.pyplot as plt
from uncertainties import ufloat

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage{physics} \sisetup{round-mode = figures} \sisetup{round-precision = 3}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

fit = np.load("calibracion.npy")
I_B = np.array([0.6,1,1.6,2,2.4])
data = np.array([np.genfromtxt("actividad_2_%.1f.txt" % I) for I in I_B])
B = [ufloat(fit[0],1)*ufloat(I,0.01) + ufloat(fit[1],1) for I in I_B]
B_nom = np.array([b.nominal_value for b in B])

fit = np.array([np.polyfit(data[i][:,0], data[i][:,1], 1) for i in range(0,len(data))])
sigma_V = np.array([np.sqrt(np.sum((data[i][:,1]-fit[i][1]-fit[i][0]*data[i][:,0])**2)/(len(data[i])-2)) for i in range(0,len(data))])
Delta = np.array([len(data[i])*np.sum(data[i][:,0]**2)-np.sum(data[i][:,0])**2 for i in range(0,len(data))])
sigma_pendiente = np.array([sigma_V[i]*np.sqrt(len(data[i])/Delta[i]) for i in range(0,len(data))])
sigma_intercepto = np.array([sigma_V[i]*np.sqrt(np.sum(data[i][:,0]**2)/Delta[i]) for i in range(0,len(data))])

R = np.array([ufloat(fit[i][0], sigma_pendiente[i])*ufloat(0.001, 0.0005)/(B[i]/1000) for i in range(0,len(B))])

for i in range(0,len(B_nom)):
	print("Se tiene una resistencia de Hall de %s para el campo magnetico %s" % (R[i].format(".2u"), B[i].format(".2u")))

colors = ["b", "r", "g", "y", "m"]
fig, ax = plt.subplots()
for i in range(0,len(data)):
	ax.errorbar(data[i][:,0], data[i][:,1], xerr = 1, yerr = 0.1, fmt = "o", alpha = 0.3, c = colors[i], label = r"$B = \SI{%s}{\milli\tesla}$" % B[i].format(".1uS"))
	ax.plot(data[i][:,0], fit[i][0]*data[i][:,0]+fit[i][1], c = colors[i], alpha = 0.3)
ax.set_xlabel(r"$I_p(\si{\milli\A})$")
ax.set_ylabel(r"$V_H(\si{\milli\volt})$")
ax.set_title(r"Efecto Hall a $B$ constante")
ax.legend()
fig.savefig("Resistencias_Hall_2.png")
plt.close(fig) 

fit = np.load("calibracion.npy")
I_p = np.array([-20,-12,14,22,30])
data = np.array([np.genfromtxt("actividad_2_%d.txt" % I) for I in I_p])
B = [[ufloat(fit[0],1)*ufloat(I_B,0.01) + ufloat(fit[1],1) for I_B in data[i][:,0]] for i in range(0,len(data))]
B_nom = np.array([np.array([b.nominal_value for b in B[i]]) for i in range(0,len(B))])

fit = np.array([np.polyfit(B_nom[i], data[i][:,1], 1) for i in range(0,len(B_nom))])
sigma_V = np.array([np.sqrt(np.sum((data[i][:,1]-fit[i][1]-fit[i][0]*B_nom[i])**2)/(len(B_nom[i])-2)) for i in range(0,len(B_nom))])
Delta = np.array([len(B_nom[i])*np.sum(B_nom[i]**2)-np.sum(B_nom[i])**2 for i in range(0,len(B_nom))])
sigma_pendiente = np.array([sigma_V[i]*np.sqrt(len(B_nom[i])/Delta[i]) for i in range(0,len(B_nom))])
sigma_intercepto = np.array([sigma_V[i]*np.sqrt(np.sum(B_nom[i]**2)/Delta[i]) for i in range(0,len(B_nom))])

R = np.array([ufloat(fit[i][0], sigma_pendiente[i])*ufloat(0.001, 0.0005)/(ufloat(I_p[i], 1)/1000) for i in range(0,len(I_p))])

for i in range(0,len(B_nom)):
	print("Se tiene una resistencia de Hall de %s para la corriente transversal %f" % (R[i].format(".2u"), I_p[i]))

colors = ["b", "r", "g", "y", "m"]
fig, ax = plt.subplots()
for i in range(0,len(B_nom)):
	ax.errorbar(B_nom[i], data[i][:,1], xerr = [b.std_dev for b in B[i]], yerr = 0.1, fmt = "o", alpha = 0.3, c = colors[i], label = r"$I_p = \SI{%f}{\milli\A}$" % I_p[i])
	ax.plot(B_nom[i], fit[i][0]*B_nom[i]+fit[i][1], c = colors[i], alpha = 0.3)
ax.set_xlabel(r"$B(\si{\milli\tesla})$")
ax.set_ylabel(r"$V_H(\si{\milli\volt})$")
ax.set_title(r"Efecto Hall a $I_p$ constante")
ax.legend()
fig.savefig("Resistencias_Hall.png")
plt.close(fig) 
