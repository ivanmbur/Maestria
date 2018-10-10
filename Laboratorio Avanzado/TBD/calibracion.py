import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage[version = 4]{mhchem} \usepackage{physics}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

angles_raw = ["0", "0,3", "0,6", "1,2", "1,5", "1,8", "2,1", "2,4", "2,7"]
angles = np.array([float(num.replace(",",".")) for num in angles_raw])
photos = np.array([np.array(Image.open("haz("+angle+"grados).tif").convert("L")) for angle in angles_raw])

#We take a naive approach towards the calculation of the centroid by splitting in half the picture. This should work relatively well after the fourth photo.

centroids_L = np.zeros((len(angles), 2))
centroids_R = np.zeros((len(angles), 2))

for i in range(0,len(angles)):

	photo_L = photos[i,:,:640]
	photo_R = photos[i,:,640:]
	for n in range(0,len(photo_L)):
		for m in range(0,len(photo_L[n])):
			centroids_L[i,0] += photo_L[n,m]*m
			centroids_L[i,1] += photo_L[n,m]*n
			centroids_R[i,0] += photo_R[n,m]*(m+640)
			centroids_R[i,1] += photo_R[n,m]*n
	centroids_L[i] = centroids_L[i]/np.sum(photo_L)
	centroids_R[i] = centroids_R[i]/np.sum(photo_R)

distances = np.linalg.norm(centroids_L-centroids_R, axis = 1)

fit = np.polyfit(angles[3:], distances[3:], 1)

fig, ax = plt.subplots()
ax.errorbar(angles, distances, xerr = 0.005, yerr = 0.5, fmt = "o", c = "k", ms = 3)
ax.plot(angles[3:], fit[0]*angles[3:]+fit[1], c = "k", label = r"$d = %.2f \si{px} \theta + %.2f \si{px}$" % (fit[0], fit[1]))
ax.set_xlabel(r"$\theta(\si{\degree})$")
ax.set_ylabel(r"$d(\si{px})$")
ax.legend()
fig.savefig("calibracion.png")
plt.close(fig)
