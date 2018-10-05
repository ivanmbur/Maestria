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

d_LiF = 2.014


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
ax.errorbar([d.nominal_value for d in d_Al], [I.nominal_value for I in log_Al[angulo]], yerr = [I.std_dev for I in log_Al[angulo]], xerr = 0.0005, c = "k", fmt = "o", label = r"\ce{Al}")
ax.plot([d.nominal_value for d in d_Al], [I.nominal_value for I in mu_Al[angulo]*d_Al + b_Al[angulo]], c = "k", label = r"$\SI{%s}{\per\milli\meter}d+\num{%s}$" % (mu_Al[angulo].format("L"), b_Al[angulo].format("L")))
ax.errorbar([d.nominal_value for d in d_Zn], [I.nominal_value for I in log_Zn[angulo]], yerr = [I.std_dev for I in log_Zn[angulo]], xerr = 0.0005, c = "k", fmt = "^", label = r"\ce{Zn}")
ax.plot([d.nominal_value for d in d_Zn], [I.nominal_value for I in mu_Zn[angulo]*d_Zn + b_Zn[angulo]], c = "k", ls = "--", label = r"$\SI{%s}{\per\milli\meter}d+\num{%s}$" % (mu_Zn[angulo].format("L"), b_Zn[angulo].format("L")))
ax.set_xlabel(r"$d(\si{\milli\meter})$", fontsize = 14)
ax.set_ylabel(r"$\ln(I/I_0)$", fontsize = 14)
ax.legend(loc = "lower left", fontsize = 13)
fig.savefig("absorcion.png")
plt.close(fig)

rho_Al = np.array(ufloat(2.69890,0.000005))
rho_Zn = ufloat(7.13300,0.000005)
d_LiF = ufloat(d_LiF, 0.0005)

lambdas = 2*d_LiF*np.array([sin(theta*np.pi/180) for theta in angulos])
y_Al = (np.array(-1)*mu_Al*np.array(10)/rho_Al)**(1/3)
y_Zn = (np.array(-1)*mu_Zn*np.array(10)/rho_Zn)**(1/3)

b_Al = (y_Al[2:].sum()*(lambdas[2:]**2).sum()-lambdas[2:].sum()*(y_Al[2:]*lambdas[2:]).sum())/(9*(lambdas[2:]**2).sum()-lambdas[2:].sum()**2)
m_Al = (((-y_Al[2:].sum())*(lambdas[2:].sum()))+(9*((y_Al[2:]*lambdas[2:]).sum())))/((9*((lambdas[2:]**2).sum()))-((lambdas[2:].sum())**2))
b_Zn = (y_Zn[2:].sum()*(lambdas[2:]**2).sum()-lambdas[2:].sum()*(y_Zn[2:]*lambdas[2:]).sum())/(9*(lambdas[2:]**2).sum()-lambdas[2:].sum()**2)
m_Zn = (((-y_Zn[2:].sum())*(lambdas[2:].sum()))+(9*((y_Zn[2:]*lambdas[2:]).sum())))/((9*((lambdas[2:]**2).sum()))-((lambdas[2:].sum())**2))

fig, ax = plt.subplots()
ax.errorbar([l.nominal_value for l in lambdas], [y.nominal_value for y in y_Al], xerr = [l.std_dev for l in lambdas], yerr = [y.std_dev for y in y_Al], fmt = "o", c = "k", label = r"\ce{Al}")
ax.plot([l.nominal_value for l in lambdas], [y.nominal_value for y in np.array(m_Al)*lambdas + np.array(b_Al)], c = "k", label = r"$\SI{%s}{(\centi\meter^2\per\gram)^{1/3}\per\angstrom^3}\lambda + \num{%s}$" % (m_Al.format("L"), b_Al.format("L")))
ax.errorbar([l.nominal_value for l in lambdas], [y.nominal_value for y in y_Zn], xerr = [l.std_dev for l in lambdas], yerr = [y.std_dev for y in y_Zn], fmt = "^", c = "k", label = r"\ce{Zn}")
ax.plot([l.nominal_value for l in lambdas], [y.nominal_value for y in np.array(m_Zn)*lambdas + np.array(b_Zn)], ls = "--", c = "k", label = r"$\SI{%s}{(\centi\meter^2\per\gram)^{1/3}\per\angstrom^3}\lambda + \num{%s}$" % (m_Zn.format("L"), b_Zn.format("L")))
ax.set_xlabel(r"$\lambda(\si{\angstrom})$", fontsize = 14)
ax.set_ylabel(r"$\qty(\mu/\rho)^{1/3}\qty(\si{(\centi\meter^2\per\gram)^{1/3}})$", fontsize = 14)
ax.legend(loc = "center right", fontsize = 13)
plt.savefig("coeficiente_absorcion.png")
plt.close(fig)

#atenuacion_Al = np.array([np.genfromtxt("Actividad_2_Al_%s.txt" % grosor, skip_header = 3, encoding = "latin-1") for grosor in ["02", "04", "06", "08", "1"]])
#atenuacion_Zn = np.array([np.genfromtxt("Actividad_2_Zn_%s.txt" % grosor, skip_header = 3, encoding = "latin-1") for grosor in ["025", "05", "075", "1"]])
#
#intensidad_Cu = np.genfromtxt("Actividad_2_Cu_025.txt", skip_header = 3, encoding = "latin-1") 
#intensidad_Ni = np.genfromtxt("Actividad_2_Ni_025.txt", skip_header = 3, encoding = "latin-1") 
#
#angulos = np.array([ufloat(theta,0.05) for theta in [6,7,8,9,10,11,12,13,14,15,16]])
#
#fig, ax = plt.subplots()
#ax.plot(2*d_LiF*np.sin(intensidad_Cu[:,0]*np.pi/180), intensidad_Cu[:,1], c = "k", label = r"\ce{Cu}") 
#ax.plot(2*d_LiF*np.sin(intensidad_Ni[:,0]*np.pi/180), intensidad_Ni[:,1], ls = "-.", c = "k", label = r"\ce{Ni}")
#ax.plot([2*d_LiF*np.sin(theta.nominal_value*np.pi/180) for theta in angulos], atenuacion_Al[1,:,1], ls = "--", c = "k", label = r"\ce{Al}")
#ax.plot([2*d_LiF*np.sin(theta.nominal_value*np.pi/180) for theta in angulos], atenuacion_Zn[1,:,1], ls = ":", c = "k", label = r"\ce{Zn}")
#ax.set_xlabel(r"$\lambda(\si{\angstrom})$", fontsize = 14)
#ax.set_ylabel(r"$I$(unidades arbitrarias)", fontsize = 14)
#ax.legend(fontsize = 13)
#fig.savefig("caracteristicos_filtros.png")
#plt.close(fig)
