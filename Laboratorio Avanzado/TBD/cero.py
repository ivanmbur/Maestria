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

print(centroids_V)
centroids_V = 4.65*centroids_V
centroids_H = 4.65*centroids_H

distances = np.abs(centroids_V-centroids_H)
argmin = np.argmin(distances)
origin = (centroids_V[argmin]+centroids_H[argmin])/2
centroids_V = centroids_V - origin
centroids_H = centroids_H - origin

p_V = np.polyfit(angles, centroids_V, 1)
p_H = np.polyfit(angles, centroids_H, 1)
correr = (p_V[1]-p_H[1])/(p_V[0]-p_H[0])

print("Vertical: d=%ftheta+%f" % (p_V[0],p_V[1]))
print("Horizontal: d=%ftheta+%f" % (p_H[0],p_H[1]))

sigma_d_V = np.sqrt(np.sum(centroids_V-p_V[1]-p_V[0]*angles)**2/(len(centroids_V)-2))
sigma_d_H = np.sqrt(np.sum(centroids_H-p_H[1]-p_H[0]*angles)**2/(len(centroids_H)-2))

print("sigma_d_V=%.10f" % sigma_d_V)
print("sigma_d_H=%.10f" % sigma_d_H)

fig, ax = plt.subplots()
ax.scatter(angles, centroids_V, c = "b", alpha = 0.3, label = r"$\ket{V}$")
ax.scatter(angles, centroids_H, c = "r", alpha = 0.3, label = r"$\ket{H}$")
ax.plot(angles, p_V[0]*angles + p_V[1], c = "b")
ax.plot(angles, p_H[0]*angles + p_H[1], c = "r")
ax.set_xlabel(r"$\theta(\si{\degree})$", fontsize = 15)
ax.set_ylabel(r"$d(\si{\micro\meter})$", fontsize = 15)
ax.set_title(r"Curva de calibraci\'on: Correr \ang[scientific-notation=false]{%f}" % correr, fontsize = 15)
ax.tick_params(labelsize = 12)
ax.legend(fontsize = 15)
fig.savefig("curva_calibracion.png")
plt.close(fig)
