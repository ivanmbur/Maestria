from uncertainties import ufloat
from uncertainties.umath import *
import numpy as np

tau = ufloat(2.1969811,0.0000022)*1E-6
tau_- = ufloat(2.043,0.003)*1E-6
m = ufloat(105.6583745,0.0000024)*1E6
tau_obs = ufloat(2.154,0.026)
h = ufloat(6.582119514,0.000000040)*1E-16

G_F=sqrt(192*np.pi**3*h/(tau_obs*m**5))

print(G_F)
