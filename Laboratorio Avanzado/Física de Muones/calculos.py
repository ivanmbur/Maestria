from uncertainties import ufloat
from uncertainties.umath import *
import numpy as np
import matplotlib.pyplot as plt

tau_p = ufloat(2.1969811,0.0000022)*1E-6
tau_m = ufloat(2.043,0.003)*1E-6
m = ufloat(105.6583745,0.0000024)*1E6
h = ufloat(6.582119514,0.000000040)*1E-16

G_F=sqrt(192*np.pi**3*h/(tau_p*m**5))

tau_obs = np.linspace(tau_m.n,tau_p.n,1000,endpoint=False)
delta_tau = 0.025E-6

tau_obs_2 = np.array([ufloat(x,delta_tau) for x in tau_obs])

delta_rho = np.sqrt((tau_obs*(tau_obs-tau_m.n)*tau_p.std_dev/(tau_m.n*(tau_m.n*tau_obs)**2))**2 + (tau_p.n*tau_obs*tau_m.std_dev/(tau_m.n**2*(tau_p.n-tau_obs)))**2 + (tau_p.n*(tau_p.n-tau_m.n)*delta_tau/(tau_m.n*(tau_p.n-tau_obs)**2))**2)

delta_rho_2 = np.array([x.std_dev for x in (tau_p*(tau_obs-tau_m)/(tau_m*(tau_p-tau_obs)))])

fig, ax = plt.subplots()
ax.plot(tau_obs,delta_rho_2)
plt.show()
