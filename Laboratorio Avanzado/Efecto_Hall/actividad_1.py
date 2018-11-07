import numpy as np
import matplotlib.pyplot as plt

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage{physics} \sisetup{round-mode = figures} \sisetup{round-precision = 3}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

data = np.genfromtxt("actividad_1.txt")
data[:,1] = -data[:,1]

fit = np.polyfit(data[:,0],data[:,1],1)
sigma_B = np.sqrt(np.sum((data[:,1]-fit[1]-fit[0]*data[:,0])**2)/(len(data)-2))
Delta = len(data)*np.sum(data[:,0]**2)-(np.sum(data[:,0]))**2
sigma_pendiente = sigma_B*np.sqrt(len(data)/Delta)
sigma_intercepto = sigma_B*np.sqrt(np.sum((data[:,0])**2)/Delta)
print("se obtuvo B = %f I + %f con incertidumbres %f en los campos magneticos, %f en la pendiente y %f en el intercepto." % (fit[0], fit[1], sigma_B, sigma_pendiente, sigma_intercepto))
I = np.array([np.amin(data[:,0]),np.amax(data[:,0])])
np.save("calibracion", fit)

fig, ax = plt.subplots()
ax.errorbar(data[:,0], data[:,1], xerr = 0.01, yerr = 10, c = "k", fmt = "o")
ax.plot(I, fit[0]*I + fit[1], c = "k")
ax.set_xlabel(r"$I_B(\si{\A})$")
ax.set_ylabel(r"$B(\si{\milli\tesla})$")
ax.set_title(r"Curva de calibraci\'on")
fig.savefig("calibracion.png")
plt.close(fig)
