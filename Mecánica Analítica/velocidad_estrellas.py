import numpy as np
import matplotlib.pyplot as plt

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage[version = 4]{mhchem} \usepackage{physics}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

G = 6.67408E-11
m_sol = 1988500E24
m_c = 4.1E6*m_sol
m_g = 1E12*m_sol
r_0 = 5E4*9.4607E15

def v(r):
	if r > r_0:
		return np.sqrt(G*(m_c+m_g)/r)
	else:
		return np.sqrt(G*(m_c+m_g*(r/r_0)**3)/r)

r = np.linspace(0.001*r_0, 5*r_0, 10000)

fig, ax = plt.subplots()
ax.plot(r/r_0, [v(u)/1E3 for u in r], c = "k")
ax.set_xlabel("$r(r_0)$")
ax.set_ylabel("$v(\si{\kilo\meter\per\second})$")
fig.savefig("distribucion_velocidades.png")
plt.close(fig)
