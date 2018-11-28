import numpy as np
from uncertainties import ufloat
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage[version = 4]{mhchem} \usepackage{physics}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

#Se definen los parametros experimentales

#Polarización
alpha = 1/np.sqrt(2) 
beta = 1/np.sqrt(2)

#Datos interferencia
w = ufloat(294, 8)
q_0 = ufloat(0.0668,1)
phi = ufloat(1.4,6) 

#Se definen las matrices de Pauli
sx = np.array([[0, 1],[ 1, 0]])
sy = np.array([[0, -1j],[1j, 0]])
sz = np.array([[1, 0],[0, -1]])

#Se definen los parametros de una esfera. Estos se toman de https://stackoverflow.com/questions/31768031/plotting-points-on-the-surface-of-a-sphere-in-pythons-matplotlib
r = 1
pi = np.pi
cos = np.cos
sin = np.sin
varphi, theta = np.mgrid[0.0:pi:100j, 0.0:2.0*pi:100j]
x = r*sin(varphi)*cos(theta)
y = r*sin(varphi)*sin(theta)
z = r*cos(varphi)

#Se define el rango de distancias con las que se hará la simulación (en unidades de micrometros/w)
d_max = 300
N = 1000
d = np.linspace (0, d_max, N)

#Se define el operador densidad
rho = np.array([[[np.abs(alpha)**2, alpha*np.conj(beta)*np.exp(-2*d_c**2/(w.nominal_value**2))*np.exp(1j*(d_c*q_0.nominal_value+phi.nominal_value))],[np.conj(alpha)*beta*np.exp(-2*d_c**2/(w.nominal_value**2))*np.exp(-1j*(d_c*q_0.nominal_value+phi.nominal_value)), np.abs(beta)**2]] for d_c in d])

#Se definen los parametros de Stokes
S = np.array([[np.trace(R @ sx), np.trace(R @ sy), np.trace(R @ sz)] for R in rho])
print(S)

#Se define la pureza
P = (1+(np.abs(alpha)**2-np.abs(beta)**2)+4*np.abs(alpha*np.conj(beta))**2*np.exp(-4*d**2/(w.nominal_value**2)))/2

#Se grafica en la bola de Bloch
fig = plt.figure()
ax = fig.add_subplot(111, projection = "3d")
ax.plot_surface(x, y, z,  rstride=1, cstride=1, color="c", alpha=0.3, linewidth=0)
ax.plot(S[:,0], S[:,1], S[:,2], c = "k")
ax.set_xlim([-1,1])
ax.set_ylim([-1,1])
ax.set_zlim([-1,1])
ax.set_xticks([-1, 0, 1])
ax.set_yticks([-1, 0, 1])
ax.set_zticks([-1, 0, 1])
for t in ax.xaxis.get_major_ticks(): t.label.set_fontsize(12)
for t in ax.yaxis.get_major_ticks(): t.label.set_fontsize(12)
for t in ax.zaxis.get_major_ticks(): t.label.set_fontsize(12)
ax.set_xlabel(r"$S_1$", fontsize = 15)
ax.set_ylabel(r"$S_2$", fontsize = 15)
ax.set_zlabel(r"$S_3$", fontsize = 15)
ax.set_aspect("equal")
ax.set_title("Estado en la esfera de Bloch", fontsize = 15)
fig.savefig("esfera.png")
plt.close(fig)

#Se hace la gráfica
fig, ax = plt.subplots()
ax.plot(d, P, c = "k")
ax.set_xlabel(r"$d(\si{\micro\meter})$", fontsize = 15)
ax.set_ylabel(r"$P$", fontsize = 15)
ax.set_title(r"Simulaci\'on de pureza", fontsize = 15)
ax.tick_params(labelsize = 12)
fig.savefig("pureza.png")
plt.close(fig)
