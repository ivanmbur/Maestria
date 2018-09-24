import numpy as np
import matplotlib.pyplot as plt
from uncertainties import ufloat
from uncertainties.umath import *

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage[version = 4]{mhchem} \usepackage{physics}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

h = ufloat(4.135667662,0.000000025)*1E-15
c = 299792458E10

#data_LiF = np.genfromtxt("Actividad_1_LiF.txt", skip_header = 3, encoding = "latin-1")
#data_KBr = np.genfromtxt("Actividad_1_KBr.txt", skip_header = 3, encoding = "latin-1")
d_LiF = 2.014
d_KBr = 3.290
#
#alpha_LiF_1 = h*c/(2*ufloat(d_LiF,0.0005)*sin(ufloat(22.7,0.05)*np.pi/180))
#alpha_LiF_2 = h*c/(ufloat(d_LiF,0.0005)*sin(ufloat(50.1,0.05)*np.pi/180))
#beta_LiF_1 = h*c/(2*ufloat(d_LiF,0.0005)*sin(ufloat(20.4,0.05)*np.pi/180))
#beta_LiF_2 = h*c/(ufloat(d_LiF,0.0005)*sin(ufloat(43.9,0.05)*np.pi/180))
#
#alpha_KBr_1 = h*c/(2*ufloat(d_KBr,0.0005)*sin(ufloat(13.1,0.05)*np.pi/180))
#alpha_KBr_2 = h*c/(ufloat(d_KBr,0.0005)*sin(ufloat(27.8,0.05)*np.pi/180))
#alpha_KBr_3 = h*c/(2*ufloat(d_KBr,0.0005)*sin(ufloat(44.4,0.05)*np.pi/180)/3)
#beta_KBr_1 = h*c/(2*ufloat(d_KBr,0.0005)*sin(ufloat(11.8,0.05)*np.pi/180))
#beta_KBr_2 = h*c/(ufloat(d_KBr,0.0005)*sin(ufloat(24.9,0.05)*np.pi/180))
#beta_KBr_3 = h*c/(2*ufloat(d_KBr,0.0005)*sin(ufloat(39.2,0.05)*np.pi/180)/3)
#
#alpha_LiF = (alpha_LiF_1+alpha_LiF_2)/2
#beta_LiF = (beta_LiF_1+beta_LiF_2)/2
#alpha_KBr = (alpha_KBr_1+alpha_KBr_2+alpha_KBr_3)/3
#beta_KBr = (beta_KBr_1+beta_KBr_2+beta_KBr_3)/3
#
#fig, ax = plt.subplots(2, 1, sharex = True)
#fig.subplots_adjust(hspace = 0)
#ax[0].plot(2*d_LiF*np.sin(data_LiF[:,0]*np.pi/180), data_LiF[:,1], c = "k", label = r"\ce{LiF} \\$K_\alpha = \SI{%s}{\electronvolt}$\\$K_\beta = \SI{%s}{\electronvolt}$" % (alpha_LiF.format("L"),beta_LiF.format("L")))
#ax[1].plot(2*d_KBr*np.sin(data_KBr[:,0]*np.pi/180), data_KBr[:,1], c = "k", label = r"\ce{KBr} \\$K_\alpha = \SI{%s}{\electronvolt}$\\$K_\beta = \SI{%s}{\electronvolt}$" % (alpha_KBr.format("L"),beta_KBr.format("L")))
#ax[1].set_xticks(np.linspace(0,5,8))
#ax[1].set_xlabel(r"$\lambda(\si{\angstrom})$")
#ax[0].set_ylabel(r"$I$(unidades arbitrarias)")
#ax[0].set_title(r"Perfiles de intensidad $U_A=\SI{35}{\kilo\volt}$")
#ax[0].legend()
#ax[1].legend()
#fig.savefig("Caracteristicos_Cu.png")
#plt.close(fig)

atenuacion_Al = np.array([np.genfromtxt("Actividad_2_Al_%s.txt" % grosor, skip_header = 3, encoding = "latin-1") for grosor in ["02", "04", "06", "08", "1"]])
atenuacion_Zn = np.array([np.genfromtxt("Actividad_2_Zn_%s.txt" % grosor, skip_header = 3, encoding = "latin-1") for grosor in ["025", "05", "075", "1"]])
normalizacion_Al = np.genfromtxt("Actividad_2_35V.txt", skip_header = 3, encoding = "latin-1")

angulos = np.array([ufloat(theta,0.05) for theta in [6,7,8,9,10,11,12,13,14,15,16]])
intensidades_Al = np.array([np.array([ufloat(I, 0.5) for I in atenuacion_Al[:,angulo,1]]) for angulo in range(0,11)])
normalizacion_Al = np.array([ufloat(I, 0.5) for I in normalizacion_Al[:,1]])
intensidades_Al = np.array([intensidades_Al[angulo]/np.array(normalizacion_Al[angulo]) for angulo in range(0,11)])
d_Al = np.array([ufloat(d, 0.0005) for d in [0.02,0.04,0.06,0.08,0.1]])
log_Al = np.array([np.array([log(I) for I in intensidades_Al[angulo]]) for angulo in range(0,11)])
b_Al = [(log_Al[angulo].sum()*(d_Al**2).sum()-d_Al.sum()*(log_Al[angulo]*d_Al).sum())/(5*(d_Al**2).sum()-d_Al.sum()**2) for angulo in range(0,11)]
mu_Al = [(((-log_Al[angulo].sum())*(d_Al.sum()))+(5*((log_Al[angulo]*d_Al).sum())))/((5*((d_Al**2).sum()))-((d_Al.sum())**2)) for angulo in range(0,11)]

intensidades_Zn = np.array([np.array([ufloat(I, 0.5) for I in atenuacion_Zn[:,angulo,1]]) for angulo in range(0,11)])
intensidades_Zn = np.array([intensidades_Zn[angulo]/np.array(normalizacion_Al[angulo]) for angulo in range(0,11)])
d_Zn = np.array([ufloat(d, 0.0005) for d in [0.025,0.05,0.075,0.1]])
log_Zn = np.array([np.array([log(I) for I in intensidades_Zn[angulo]]) for angulo in range(0,11)])
b_Zn = [(log_Zn[angulo].sum()*(d_Zn**2).sum()-d_Zn.sum()*(log_Zn[angulo]*d_Zn).sum())/(4*(d_Zn**2).sum()-d_Zn.sum()**2) for angulo in range(0,11)]
mu_Zn = [(((-log_Zn[angulo].sum())*(d_Zn.sum()))+(4*((log_Zn[angulo]*d_Zn).sum())))/((4*((d_Zn**2).sum()))-((d_Zn.sum())**2)) for angulo in range(0,11)]

angulo = 9

fig, ax = plt.subplots()
ax.errorbar([d.nominal_value for d in d_Al], [I.nominal_value for I in log_Al[angulo]], yerr = [I.std_dev for I in log_Al[angulo]], xerr = 0.0005, c = "k", fmt = ".", label = r"\ce{Al}")
ax.plot([d.nominal_value for d in d_Al], [I.nominal_value for I in mu_Al[angulo]*d_Al + b_Al[angulo]], c = "k", label = r"$\SI{%s}{\per\milli\meter}d+\num{%s}$" % (mu_Al[angulo].format("L"), b_Al[angulo].format("L")))
ax.errorbar([d.nominal_value for d in d_Zn], [I.nominal_value for I in log_Zn[angulo]], yerr = [I.std_dev for I in log_Zn[angulo]], xerr = 0.0005, c = "k", fmt = "x", label = r"\ce{Zn}")
ax.plot([d.nominal_value for d in d_Zn], [I.nominal_value for I in mu_Zn[angulo]*d_Zn + b_Zn[angulo]], c = "k", ls = "--", label = r"$\SI{%s}{\per\milli\meter}d+\num{%s}$" % (mu_Zn[angulo].format("L"), b_Zn[angulo].format("L")))
ax.set_xlabel(r"$d(\si{\milli\meter})$")
ax.set_ylabel(r"$\ln(I/I_0)$")
ax.set_title(r"Absorci\'on a $\theta=\SI{%d}{\degree}$" % (6+angulo))
ax.legend(loc = "lower left")
fig.savefig("absorcion.png")
plt.close(fig)

rho_Al = np.array(ufloat(2.69890,0.000005))
rho_Zn = ufloat(7.13300,0.000005)
d_LiF = ufloat(d_LiF, 0.0005)
lambdas = 2*d_LiF*np.array([sin(theta*np.pi/180) for theta in angulos])
#y_Al = (np.array(-1)*mu_Al*np.array(10)/rho_Al)**(1/3)
y_Al = np.array([log(y) for y in np.array(-1)*mu_Al*np.array(10)/rho_Al])

#fig, ax = plt.subplots()
#ax.errorbar([l.nominal_value for l in lambdas], [y.nominal_value for y in y_Al], xerr = [l.std_dev for l in lambdas], yerr = [y.std_dev for y in y_Al], fmt = "o", c = "k")
#ax.set_xlabel(r"$\lambda(\si{\angstrom})$")
#ax.set_ylabel(r"$\qty(\mu/\rho)^{1/3}\qty(\si{(\centi\meter^4\per\gram)^{1/3}})$")
#plt.show()
#plt.close(fig)

fig, ax = plt.subplots()
ax.errorbar([l.nominal_value for l in lambdas], [y.nominal_value for y in y_Al], xerr = [l.std_dev for l in lambdas], yerr = [y.std_dev for y in y_Al], fmt = "o", c = "k")
ax.set_xlabel(r"$\lambda(\si{\angstrom})$")
ax.set_ylabel(r"$\ln(\mu/\rho)$")
plt.show()
plt.close(fig)


