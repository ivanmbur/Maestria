import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import axes3d

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage[version = 4]{mhchem} \usepackage{physics}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

angles = np.linspace(-6, 6, 21, endpoint = True)
angles_raw = ["%.1f" % theta for theta in angles]
photos_V = np.array([np.array(Image.open("cuarta_calibracion/Imagenes_PTBD(Vertical)/" + angle + ".tif").convert("L")) for angle in angles_raw])
photos_H = np.array([np.array(Image.open("cuarta_calibracion/Imagenes_PTBD(Horizontal)/" + angle + ".tif").convert("L")) for angle in angles_raw])

#We take a naive approach towards the calculation of the centroid by splitting in half the picture. This should work relatively well after the fourth photo.

rangex = len(photos_V[0,:,:])
rangey = len(photos_V[0,0,:])
centroids_V = np.zeros((len(angles), 2))
centroids_H = np.zeros((len(angles), 2))

for i in range(0,len(angles)):

	#calculate centroid of ith photo

	for n in range(0,rangex):
		for m in range(0,rangey):
			centroids_V[i,0] += photos_V[i,n,m]*m
			centroids_V[i,1] += photos_V[i,n,m]*n
			centroids_H[i,0] += photos_H[i,n,m]*m
			centroids_H[i,1] += photos_H[i,n,m]*n
	centroids_V[i] = centroids_V[i]/np.sum(photos_V[i,:,:])
	centroids_H[i] = centroids_H[i]/np.sum(photos_H[i,:,:])

distances = np.linalg.norm(centroids_V-centroids_H, axis = 1)

minarg = np.argmin(distances)

origin = (centroids_V[minarg]+centroids_H[minarg])/2

centroids_V = centroids_V-origin
centroids_H = centroids_H-origin

fig, ax = plt.subplots()
ax.errorbar(angles, np.linalg.norm(centroids_V, axis = 1), xerr = 0.005, yerr = 0.5, fmt = "o", c = "k", ms = 3, label = "$d_V$")
ax.errorbar(angles, np.linalg.norm(centroids_H, axis = 1), xerr = 0.005, yerr = 0.5, fmt = "o", c = "k", ms = 3, label = "$d_H$")
#ax.plot(angles[3:], fit[0]*angles[3:]+fit[1], c = "k", label = r"$d = %.2f \si{px} \theta + %.2f \si{px}$" % (fit[0], fit[1]))
ax.set_xlabel(r"$\theta(\si{\degree})$")
ax.set_ylabel(r"$d(\si{px})$")
ax.legend(loc = "lower left")
fig.savefig("calibracion_4.png")
plt.close(fig)
