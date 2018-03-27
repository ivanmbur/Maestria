import numpy as np
import matplotlib.pyplot as plt

tau_n = 30
n = 100000

tau = np.linspace(0,tau_n,n)
psi = np.zeros(n)
Dpsi = np.zeros(n)
delta = tau[1]-tau[0]

psi[0] = 1
Dpsi[0] = 0

for i in range(1,n):
	psi[i] = psi[i - 1] + Dpsi[i-1]*delta
	Dpsi[i] = Dpsi[i - 1] - psi[i-1]*delta

fig, ax = plt.subplots()
ax.plot(tau, psi)
ax.set_xlabel("$t(1/\omega)$")
ax.set_ylabel("$\zeta(l)$")
ax.set_title("Harmonic Oscillator")
fig.savefig("taller_computacional.png")
plt.close(fig)
