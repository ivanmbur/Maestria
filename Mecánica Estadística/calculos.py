import numpy as np

K = np.log((3-np.sqrt(2))/(np.sqrt(2)-1))/4
print("K = %f" % K)
d1R1 = 1+4*K*((((3.0*np.exp(4.0*K)-1)*(np.exp(4.0*K)+3.0))/((np.exp(4.0*K)+3.0)*(np.exp(4.0*K)+3.0)))-((3.0*np.exp(4.0*K)-3.0)/((np.exp(4.0*K)+3.0)*np.sqrt(2.0))))/np.sqrt(2.0)
print("d1R1 = %f" % d1R1)
y_T = np.log(d1R1)/np.log(np.sqrt(3)) 
print("y_T = %f" % y_T) 
d2R2 = 3.0/np.sqrt(2)
print("d2R2 = %f" % d2R2)
y_h = np.log(d2R2)/np.log(np.sqrt(3))
print("y_h = %f" % y_h)
nu = 1/y_T
print("nu = %f" % nu) 
alpha = 2 - 2/y_T
beta = (2-y_h)/y_T
gamma = (2*y_h - 2)/y_T
eta = 2+2-2*y_h
delta = y_h/(2-y_h)
print("alpha = %f" % alpha) 
print("beta = %f" % beta) 
print("gamma = %f" % gamma) 
print("eta = %f" % eta) 
print("delta = %f" % delta) 
