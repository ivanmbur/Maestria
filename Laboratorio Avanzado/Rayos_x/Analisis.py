import numpy as np 
import matplotlib.pyplot as plt
from uncertainties import ufloat
from uncertainties.umath import *
from scipy.signal import savgol_filter

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage[version = 4]{mhchem} \usepackage{physics}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

h = ufloat(4.135667662,0.000000025)*1E-15
c = 299792458E10

data_LiF = np.genfromtxt("Actividad_1_LiF.txt", skip_header = 3, encoding = "latin-1")
data_KBr = np.genfromtxt("Actividad_1_KBr.txt", skip_header = 3, encoding = "latin-1")
d_LiF = 2.014
d_KBr = 3.290

alpha_LiF_1 = h*c/(2*ufloat(d_LiF,0.0005)*sin(ufloat(22.7,0.05)*np.pi/180))
alpha_LiF_2 = h*c/(ufloat(d_LiF,0.0005)*sin(ufloat(50.1,0.05)*np.pi/180))
beta_LiF_1 = h*c/(2*ufloat(d_LiF,0.0005)*sin(ufloat(20.4,0.05)*np.pi/180))
beta_LiF_2 = h*c/(ufloat(d_LiF,0.0005)*sin(ufloat(43.9,0.05)*np.pi/180))

alpha_KBr_1 = h*c/(2*ufloat(d_KBr,0.0005)*sin(ufloat(13.1,0.05)*np.pi/180))
alpha_KBr_2 = h*c/(ufloat(d_KBr,0.0005)*sin(ufloat(27.8,0.05)*np.pi/180))
alpha_KBr_3 = h*c/(2*ufloat(d_KBr,0.0005)*sin(ufloat(44.4,0.05)*np.pi/180)/3)
beta_KBr_1 = h*c/(2*ufloat(d_KBr,0.0005)*sin(ufloat(11.8,0.05)*np.pi/180))
beta_KBr_2 = h*c/(ufloat(d_KBr,0.0005)*sin(ufloat(24.9,0.05)*np.pi/180))
beta_KBr_3 = h*c/(2*ufloat(d_KBr,0.0005)*sin(ufloat(39.2,0.05)*np.pi/180)/3)

alpha_LiF = (alpha_LiF_1+alpha_LiF_2)/2
beta_LiF = (beta_LiF_1+beta_LiF_2)/2
alpha_KBr = (alpha_KBr_1+alpha_KBr_2+alpha_KBr_3)/3
beta_KBr = (beta_KBr_1+beta_KBr_2+beta_KBr_3)/3

fig, ax = plt.subplots(2, 1, sharex = True)
fig.subplots_adjust(hspace = 0)
ax[0].plot(2*d_LiF*np.sin(data_LiF[:,0]*np.pi/180), data_LiF[:,1], c = "k", label = r"\ce{LiF} \\$K_\alpha = \SI{%s}{\electronvolt}$\\$K_\beta = \SI{%s}{\electronvolt}$" % (alpha_LiF.format("L"),beta_LiF.format("L")))
ax[1].plot(2*d_KBr*np.sin(data_KBr[:,0]*np.pi/180), data_KBr[:,1], c = "k", label = r"\ce{KBr} \\$K_\alpha = \SI{%s}{\electronvolt}$\\$K_\beta = \SI{%s}{\electronvolt}$" % (alpha_KBr.format("L"),beta_KBr.format("L")))
ax[1].set_xticks(np.linspace(0,5,8))
ax[1].set_xlabel(r"$\lambda(\si{\angstrom})$")
ax[0].set_ylabel(r"$I$(unidades arbitrarias)")
ax[0].legend()
ax[1].legend()
fig.savefig("Caracteristicos_Cu.png")
plt.close(fig)


voltajes = ["11","14","17","20","23","26", "29", "32", "35"]
corriente_cte = np.array([np.genfromtxt("Actividad_3_%s.txt" % voltaje, skip_header = 3, encoding = "latin-1") for voltaje in voltajes])

fig, ax = plt.subplots()
for i in range(0,len(corriente_cte)):
	ax.plot(2*d_LiF*np.sin(corriente_cte[i,:,0]*np.pi/180), corriente_cte[i,:,1], c = "k")
ax.set_xlabel(r"$\lambda(\si{\angstrom})$", fontsize = 14)
ax.set_ylabel(r"$I$(unidades arbitrarias)", fontsize = 14)
fig.savefig("corriente_cte.png")
plt.close(fig)

voltaje_cte = np.array([np.genfromtxt("Actividad_3_%s.txt" % voltaje, skip_header = 3, encoding = "latin-1") for voltaje in ["1","2","3","4","5","6", "7", "8"]])

fig, ax = plt.subplots()
for i in range(0,len(voltaje_cte)):
	ax.plot(2*d_LiF*np.sin(voltaje_cte[i,:,0]*np.pi/180), voltaje_cte[i,:,1], c = "k")
ax.plot(2*d_LiF*np.sin(corriente_cte[len(corriente_cte)-1,:,0]*np.pi/180), corriente_cte[len(corriente_cte)-1,:,1], c = "k")
ax.set_xlabel(r"$\lambda(\si{\angstrom})$")
ax.set_ylabel(r"$I$(unidades arbitrarias)")
ax.set_title("Perfil de intensidades a voltaje constante")
fig.savefig("voltaje_cte.png")
plt.close(fig)

voltajes_2 = np.array([ufloat(float(v),0.5) for v in voltajes])
intensidad_alpha = np.array([ufloat(I,0.5) for I in corriente_cte[:,40,1]]) 
intensidad_beta = np.array([ufloat(I,0.5) for I in corriente_cte[:,14,1]]) 
voltajes_3 = np.array([v for v in (voltajes_2-9.979)**(3/2)])

b_alpha = (intensidad_alpha.sum()*(voltajes_3**2).sum()-voltajes_3.sum()*(intensidad_alpha*voltajes_3).sum())/(9*(voltajes_3**2).sum()-voltajes_3.sum()**2)
m_alpha = (((-intensidad_alpha.sum())*(voltajes_3.sum()))+(9*((intensidad_alpha*voltajes_3).sum())))/((9*((voltajes_3**2).sum()))-((voltajes_3.sum())**2))
b_beta = (intensidad_beta.sum()*(voltajes_3**2).sum()-voltajes_3.sum()*(intensidad_beta*voltajes_3).sum())/(9*(voltajes_3**2).sum()-voltajes_3.sum()**2)
m_beta = (((-intensidad_beta.sum())*(voltajes_3.sum()))+(9*((intensidad_beta*voltajes_3).sum())))/((9*((voltajes_3**2).sum()))-((voltajes_3.sum())**2))

fig, ax = plt.subplots()
ax.errorbar(np.array([(float(v)-9.979)**(3/2) for v in voltajes]), corriente_cte[:,40,1], yerr = 0.5, xerr = [v.std_dev for v in (voltajes_2-9.979)**(3/2)], c = "k", fmt = "o", label = r"$K_\alpha$")
ax.plot(np.array([(float(v)-9.979)**(3/2) for v in voltajes]), m_alpha.nominal_value*np.array([(float(v)-9.979)**(3/2) for v in voltajes]) + b_alpha.nominal_value, c = "k", label = r"$\SI{%s}{(\kilo\electronvolt)^{-3/2}}+\num{%s}$" % (m_alpha.format("L"), b_alpha.format("L")))
ax.errorbar(np.array([(float(v)-9.979)**(3/2) for v in voltajes]), corriente_cte[:,14,1], yerr = 0.5, xerr = [v.std_dev for v in (voltajes_2-9.979)**(3/2)], c = "k", fmt = "^", label = r"$K_\beta$")
ax.plot(np.array([(float(v)-9.979)**(3/2) for v in voltajes]), m_beta.nominal_value*np.array([(float(v)-9.979)**(3/2) for v in voltajes]) + b_beta.nominal_value, ls = "--", c = "k", label = r"$\SI{%s}{(\kilo\electronvolt)^{-3/2}}+\num{%s}$" % (m_beta.format("L"), b_beta.format("L")))
ax.set_xlabel(r"$(U_A-U_K)^{3/2}(\si{\kilo\electronvolt})$", fontsize = 14)
ax.set_ylabel(r"$I$(Intensidad)", fontsize = 14)
ax.legend(loc = "upper left", fontsize = 13)
plt.savefig("perfil_intensidad_potencial.png")
plt.close(fig)

duane = np.genfromtxt("Actividad_4.txt", skip_header = 3, encoding = "latin-1")

print(h*c/(2*ufloat(d_LiF,0.0005)*sin(ufloat(17,0.05)*np.pi/180)))

#fig, ax = plt.subplots()
#ax.plot(2*d_LiF*np.sin(duane[:-10,0]*np.pi/180), savgol_filter(duane[:-10,len(duane[0])-10], 51, 3), c = "k")
#plt.show()
#plt.close(fig)
