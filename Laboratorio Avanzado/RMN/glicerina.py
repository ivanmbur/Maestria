import numpy as np
from uncertainties.umath import *
from uncertainties import ufloat
from uncertainties import unumpy
import matplotlib.pyplot as plt

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage{siunitx}")
plt.rc("font", family =  "cmr")

x=[575*1E-3,565*1E-3,560*1E-3,540*1E-3]
y=[17.6097,17.4269,17.2590,16.9554]
x=np.array(x)
y=np.array(y)

n=len(y)
sumx=sum(x)
sumy=sum(y)
sumx2=sum(x*x)
sumy2=sum(y*y)
sumxy=sum(x*y)
promx=sumx/n
promy=sumy/n
m=(sumx*sumy-n*sumxy)/(sumx**2-n*sumx2)
b=promy-m*promx

plt.plot(x,y,'o',label='Datos')
plt.plot(x,m*x+b,label='Ajuste')
plt.xlabel(r'$B(\si{mT})$', fontsize = 15)
plt.ylabel(r'$f(\si{MHz})$', fontsize = 15)
plt.title(r'Frecuencia de resonancia Vs Campo magn\'etico', fontsize = 15)
plt.legend(loc=4)
plt.text(0.5, 19, r'$f=mB+c$',fontsize=15)
plt.text(0.5425, 17.6,r'$m=19(7)MHz/T$',fontsize=15)
plt.text(0.5425, 17.5,r'$c=7(4)MHz$',fontsize=15)
plt.text(0.5425, 17.4,r'$R^2=0.98(10)$',fontsize=15)
plt.tick_params(labelsize =15)

sigmax=sqrt((sumx2/n)-promx**2)
sigmay=sqrt((sumy2/n)-promy**2)
sigmaxy=((sumxy/n)-(promx*promy))
R=sigmaxy/(sigmax*sigmay)
R2=R*R
m1=2*np.pi*m
print(R2)
print(m)
print(b)
plt.savefig("glicerina.png")
