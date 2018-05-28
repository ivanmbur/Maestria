import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,10,100)
p = 1/(1/(t*t)+1)

fig, ax = plt.subplots(figsize = (5,5))
ax.plot(t, p, c = "k")
ax.set_xlabel(r"time ($\hbar/3eEa_0$)")
ax.set_ylabel(r"transition probability $2s\rightarrow 2p$")
fig.savefig("transicion_stark.png")
