import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import rc

#Se definen los parametros de la simulacion

L_c = 0.5*np.arcsinh(1)
temperaturas = np.linspace(0.5, 3.2, 1000)
N = 10
nsteps = 1000000
nsteps_equilibrio = 10000

#Se crea una funcion que calcula la energia de un reticulo en unidades de J

def H(sigma):
	E = 0
	for i in range(0, len(sigma)):
		for j in range(0, len(sigma[i])):
			E += sigma[i,j]*(sigma[i, (j+1) % len(sigma[i])] + sigma[i, (j-1) % len(sigma[i])] + sigma[(i+1) % len(sigma), j] + sigma[(i-1) % len(sigma), j])
	E = -0.5*E
	return E

#Se crean las listas de energia y magnetizacion promedio

E_promedio = np.zeros(len(temperaturas))
M_promedio = np.zeros(len(temperaturas))

#Se realiza el método para cada temperatura

for t in range(0,len(temperaturas)):

	L = 1.0/temperaturas[t]

	#Se crea el reticulo de espines 

	reticulo = np.zeros((N, N))

	#Se crea una lista de energias y magnetizaciones

	E = np.zeros(nsteps)
	M = np.zeros(nsteps)

	#Se le asigna un valor aleatorio en {-1,1} a cada sitio en el reticulo

	for i in range(0, N):
		for j in range(0,N):
			reticulo[i,j] = random.randrange(-1,2,2)

	#Se inicializa la lista de energias y magnetizaciones
	E[0] = H(reticulo)
	M[0] = np.sum(reticulo)

	for n in range(1, nsteps):


		#Se selecciona una entrada aleatoria en el reticulo

		i = random.randrange(0, len(reticulo))
		j = random.randrange(0, len(reticulo[i]))

		#Se calcula el cambio en la energia

		Delta_E =2*reticulo[i,j]*(reticulo[i, (j+1) % len(reticulo[i])] + reticulo[i, (j-1) % len(reticulo[i])] + reticulo[(i+1) % len(reticulo), j] + reticulo[(i-1) % len(reticulo), j]) 

		#Se decide si se acepta el cambio

		if (Delta_E <= 0) or (random.uniform(0, 1) < np.exp(-L*Delta_E)):
			reticulo[i,j] = -reticulo[i,j]
		
		#Se calcula la nueva energia
		E[n] = H(reticulo)
		M[n] = np.sum(reticulo)
		

	#Se hacen graficas de la evolucion de la energia

	fig, ax = plt.subplots()
	ax.plot(range(0, nsteps), E/(N*N))
	ax.set_xlabel("Iteración")
	ax.set_ylabel("Energía por sitio ($J$)")
	ax.set_title("$T=%.2f J/K_B$, $N=%d$" % (temperaturas[t], N*N))
	fig.savefig("energia_%f.png" % temperaturas[t])
	plt.close(fig) 

	#Se guarda el valor de la energia promedio y la magnetizacion promedio

	E_promedio[t] = np.mean(E[nsteps_equilibrio:])
	M_promedio[t] = np.mean(M[nsteps_equilibrio:])

#Se grafica la magnetizacion

fig, ax = plt.subplots()
ax.scatter(temperaturas, M_promedio/(N*N), alpha = 0.3)
ax.set_xlabel("Temperatura ($J/K_B$)")
ax.set_ylabel("Magnetización por sitio")
ax.set_title("$N=%d$, $%d$ pasos con $%d$ para estabilizar" % (N*N, nsteps, nsteps_equilibrio))
fig.savefig("magnetizacion.png")
plt.close(fig)


