import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage{physics} \sisetup{scientific-notation = true} \sisetup{round-mode = places} \sisetup{round-precision = 2}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

centroids_V = np.load("centroids_V.npy")
centroids_H = np.load("centroids_H.npy")

centroids = np.concatenate((centroids_V, centroids_H))
p = np.polyfit(centroids[:,0], centroids[:,1], 1)
print(p)
x = np.array([np.amin(centroids[:,0]),np.amax(centroids[:,0])])

print("y =%fx+%f" % (p[0],p[1]))

fig, ax = plt.subplots()
ax.scatter(centroids_V[:,0], centroids_V[:,1], c = "b", alpha = 0.3, label = r"$\ket{V}$")
ax.scatter(centroids_H[:,0], centroids_H[:,1], c = "r", alpha = 0.3, label = r"$\ket{H}$")
ax.plot(x, p[0]*x + p[1], c = "k")
ax.set_xlabel("$x(\si{px})$")
ax.set_ylabel("$y(\si{px})$")
ax.set_title("Eje de movimiento")
ax.legend()
fig.savefig("eje.png")
plt.close(fig)
