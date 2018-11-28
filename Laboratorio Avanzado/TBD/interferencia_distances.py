import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage[version = 4]{mhchem} \usepackage{physics}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

def I(distances, offset, I_0, w, q, phi):
	distances = distances-offset
	return I_0*(1 + np.exp(-2*distances*distances/(w*w))*np.cos(2*q*distances + phi))/2

data = np.genfromtxt("interferencia.txt", usecols = (0, 1))
data[:,0] = (70.955968+57.606900)*data[:,0]-(28.513237+42.203264)

distances = np.linspace(np.min(data[:,0]),np.max(data[:,0]),1000)
popt, pcov = curve_fit(I, data[:,0], data[:,1], p0 = [40, np.max(data[:,1]), np.sqrt(100000), 0.065, np.pi])
print("[offset, I_0, w, q, phi]= ",popt," con incertidumbres ",np.sqrt(np.diag(pcov)))

fig, ax = plt.subplots()
ax.scatter(data[:,0]-popt[0], data[:,1], c = "k", alpha = 0.3)
ax.plot(distances-popt[0], I(distances, *popt), c = "k")
ax.set_xlabel(r"$d(\si{\micro\meter})$", fontsize = 15)
ax.set_ylabel(r"$I(\si{\micro\watt})$", fontsize = 15)
ax.set_title(r"Patr\'on de interferencia", fontsize = 15)
ax.tick_params(labelsize = 12)
fig.savefig("interferencia_distances.png")
plt.close(fig)
