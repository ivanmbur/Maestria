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

sigma_y = np.sqrt(np.sum((centroids[:,1]-p[1]-p[0]*centroids[:,0])**2)/(len(centroids[:,0])-2))
Delta = len(centroids[:,0])*np.sum(centroids[:,0]**2)-np.sum(centroids[:,0])**2
sigma_A = sigma_y*np.sqrt(np.sum(centroids[:,0]**2)/Delta)
sigma_B = sigma_y*np.sqrt(len(centroids[:,0])/Delta)

print("sigma_y=%.100f" % sigma_y)
print("sigma_A=%.100f" % sigma_A)
print("sigma_B=%.100f" % sigma_B)

print("y =%.7fx+%.9f" % (p[0],p[1]))

fig, ax = plt.subplots()
ax.scatter(centroids_V[:,0], centroids_V[:,1], c = "b", alpha = 0.3, label = r"$\ket{V}$")
ax.scatter(centroids_H[:,0], centroids_H[:,1], c = "r", alpha = 0.3, label = r"$\ket{H}$")
ax.plot(x, p[0]*x + p[1], c = "k")
ax.set_xlabel("$x(\si{px})$", fontsize = 15)
ax.set_ylabel("$y(\si{px})$", fontsize = 15)
ax.set_title("Eje de movimiento", fontsize = 15)
ax.tick_params(labelsize = 12)
ax.legend(fontsize = 15)
fig.savefig("eje.png")
plt.close(fig)
