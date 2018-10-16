import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import axes3d

plt.rc("text", usetex = True)
plt.rc("text.latex", preamble = r"\usepackage[utf8]{inputenc} \usepackage{siunitx} \usepackage[version = 4]{mhchem} \usepackage{physics}")
plt.rc("font", **{"family": "serif", "serif": ["Computer Modern"]})

angles = np.linspace(-9, 9, 31, endpoint = True)
angles_raw = [("%.1f" % theta).replace(".",",") for theta in angles]
photos = np.array([np.array(Image.open("tercera_calibracion/" + angle + ".tif").convert("L")) for angle in angles_raw])

#We take a naive approach towards the calculation of the centroid by splitting in half the picture. This should work relatively well after the fourth photo.

centroids = np.zeros((len(angles),2))
centroids_L = np.zeros((len(angles), 2))
centroids_R = np.zeros((len(angles), 2))

#for i in range(0,len(angles)):
#
#	#calculate centroid of ith photo
#
#	for n in range(0,len(photos[i,:,:])):
#		for m in range(0,len(photos[i,n,:])):
#			centroids[i,0] += photos[i,n,m]*m
#			centroids[i,1] += photos[i,n,m]*n
#	centroids[i] = centroids[i]/np.sum(photos[i,:,:])
#
#	#split the photo in two and calculate the centroid of each side
#
#	photo_L = photos[i,:,:int(centroids[i,0])]
#	photo_R = photos[i,:,int(centroids[i,0]):]
#	for n in range(0,len(photo_L)):
#		for m in range(0,len(photo_L[n])):
#			centroids_L[i,0] += photo_L[n,m]*m
#			centroids_L[i,1] += photo_L[n,m]*n
#	for n in range(0,len(photo_R)):
#		for m in range(0,len(photo_R[n])):
#			centroids_R[i,0] += photo_R[n,m]*(m+int(centroids[i,0]))
#			centroids_R[i,1] += photo_R[n,m]*n
#	centroids_L[i] = centroids_L[i]/np.sum(photo_L)
#	centroids_R[i] = centroids_R[i]/np.sum(photo_R)

#Now we try to calculate the centroids fitting the image to the superposicion of two gaussian modes

i = 16

positions = np.array([np.array([n,m]) for n in range(0,len(photos[i,:,:])) for m in range(0,len(photos[i,n,:]))])
I = np.array([photos[i,positions[k,0],positions[k,1]] for k in range(0,len(positions))])

fig = plt.figure()
ax = fig.add_subplot(111, projection = "3d")
ax.scatter(positions[:,0], positions[:,1], I, s = 0.1, alpha = 0.1)
plt.show()

def f(k, centroid_1_x, centroid_1_y, centroid_2_x, centroid_2_y, I_1, I_2, sigma):
	centroid_1 = np.array([centroid_1_y, centroid_1_x])
	centroid_2 = np.array([centroid_2_y, centroid_2_x])	
	return I_1*np.exp(-np.linalg.norm(positions[k]-centroid_1)**2/(2*sigma**2))+I_2*np.exp(-np.linalg.norm(positions[k]-centroid_2)**2/(2*sigma**2))


fit_1 = curve_fit(f, range(0,len(positions)), [photos[i,positions[k,0],positions[k,1]] for k in range(0,len(positions))])
print(fit_1)

#distances = np.linalg.norm(centroids_L-centroids_R, axis = 1)
#
#fig, ax = plt.subplots()
#ax.errorbar(angles, distances, xerr = 0.005, yerr = 0.5, fmt = "o", c = "k", ms = 3)
#ax.plot(angles[3:], fit[0]*angles[3:]+fit[1], c = "k", label = r"$d = %.2f \si{px} \theta + %.2f \si{px}$" % (fit[0], fit[1]))
#ax.set_xlabel(r"$\theta(\si{\degree})$")
#ax.set_ylabel(r"$d(\si{px})$")
#ax.legend()
#fig.savefig("calibracion_3.png")
#plt.close(fig)
