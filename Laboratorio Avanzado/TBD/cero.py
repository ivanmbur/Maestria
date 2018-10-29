import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage{physics} \sisetup{round-mode = figures} \sisetup{round-precision = 3}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

cutoff = 5

angles = np.linspace(-6, 6, 21, endpoint = True)[5:]

centroids_V = np.load("centroids_V.npy")[5:,0]
centroids_H = np.load("centroids_H.npy")[5:,0]

distances = np.abs(centroids_V-centroids_H)
argmin = np.argmin(distances)
origin = (centroids_V[argmin]+centroids_H[argmin])/2
centroids_V = centroids_V - origin
centroids_H = centroids_H - origin

p_V = np.polyfit(angles, centroids_V, 1)
p_H = np.polyfit(angles, centroids_H, 1)
correr = (p_V[1]-p_H[1])/(p_V[0]-p_H[0])

fig, ax = plt.subplots()
ax.scatter(angles, centroids_V, c = "b", alpha = 0.3, label = r"$\ket{V}$")
ax.scatter(angles, centroids_H, c = "r", alpha = 0.3, label = r"$\ket{H}$")
ax.plot(angles, p_V[0]*angles + p_V[1], c = "b", label = r"$d=\theta\times\num{%f}\si{px/\degree}\num{%f}\si{px}$" % (p_V[0],p_V[1]))
ax.plot(angles, p_H[0]*angles + p_H[1], c = "r", label = r"$d=\theta\times\num{%f}\si{px/\degree}+\num{%f}\si{px}$" % (p_H[0],p_H[1]))
ax.set_xlabel(r"$\theta(\si{\degree})$")
ax.set_ylabel(r"$d(\si{px})$")
ax.set_title(r"Curva de calibraci\'on: Correr \ang[scientific-notation=false]{%f}" % correr)
ax.legend()
fig.savefig("curva_calibracion.png")
plt.close(fig)
