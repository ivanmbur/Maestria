import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

angles = np.linspace(-6, 6, 21, endpoint = True)
angles_raw = ["%.1f" % theta for theta in angles]
photos_V = np.array([np.array(Image.open("cuarta_calibracion/Imagenes_PTBD(Vertical)/" + angle + ".tif").convert("L")) for angle in angles_raw])
photos_H = np.array([np.array(Image.open("cuarta_calibracion/Imagenes_PTBD(Horizontal)/" + angle + ".tif").convert("L")) for angle in angles_raw])

#We take a naive approach towards the calculation of the centroid by splitting in half the picture. This should work relatively well after the fourth photo.

rangex = len(photos_V[0,:,:])
rangey = len(photos_V[0,0,:])
centroids_V = np.zeros((len(angles), 2))
centroids_H = np.zeros((len(angles), 2))

for i in range(0,len(angles)):

	#calculate centroid of ith photo

	for n in range(0,rangex):
		for m in range(0,rangey):
			centroids_V[i,0] += photos_V[i,n,m]*m
			centroids_V[i,1] += photos_V[i,n,m]*n
			centroids_H[i,0] += photos_H[i,n,m]*m
			centroids_H[i,1] += photos_H[i,n,m]*n
	centroids_V[i] = centroids_V[i]/np.sum(photos_V[i,:,:])
	centroids_H[i] = centroids_H[i]/np.sum(photos_H[i,:,:])

np.save("centroids_V", centroids_V)
np.save("centroids_H", centroids_H)
