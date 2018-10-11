import numpy as np
from uncertainties import ufloat
from uncertainties.umath import *

h = ufloat(4.135667662,0.000000025)*1E-18
U_A = ufloat(50,0.5)
c = 299792458E10

for n in range(1,4):
	print((n*h*c/U_A))
