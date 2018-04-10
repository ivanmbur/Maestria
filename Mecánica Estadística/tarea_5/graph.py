import numpy as np
import matplotlib.pyplot as plt

a = 1.0
b = 1.0
R = 100.0

theta = np.linspace(0, 2*np.pi, 1000)
f = np.exp(-R*b*np.sin(theta))/(R*R*R*R+a*a*a*a+2*a*a*R*R*np.sin(2*theta))

fig, ax = plt.subplots()
ax.plot(theta, f, c = "k")
plt.show()
plt.close(fig)
