import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import rc

#Se definen los parametros de la simulación

L_c = 0.5*np.arcsinh(1)
temperaturas = np.linspace(0.5, 3.5, 1000)
N = 10
nsteps = 100000
nsteps_equilibrio = 10000
energy_graphs = [0,200,500,700]

#Se crean las listas de energía y magnetización promedio

E_promedio = np.zeros(len(temperaturas))
M_promedio = np.zeros(len(temperaturas))

#Se realiza el método para cada temperatura

for t in range(0,len(temperaturas)):

	print("Temperatura %d de %d" % (t,len(temperaturas)))

	L = 1.0/temperaturas[t]

	#Se crea el retículo de espines 

	reticulo = np.zeros((N, N))

	#Se crea una lista de energías y magnetizaciones

	E = np.zeros(nsteps)
	M = np.zeros(nsteps)

	#Se le asigna un valor aleatorio en {-1,1} a cada sitio en el retículo

	for i in range(0, N):
		for j in range(0,N):
			reticulo[i,j] = random.randrange(-1,2,2)

	#Se inicializan las listas de energias y magnetizaciones
	E[0] = 0
	for i in range(0, len(reticulo)):
		for j in range(0, len(reticulo[i])):
			E[0] += reticulo[i,j]*(reticulo[i, (j+1) % len(reticulo[i])] + reticulo[i, (j-1) % len(reticulo[i])] + reticulo[(i+1) % len(reticulo), j] + reticulo[(i-1) % len(reticulo), j])
	E[0] = -0.5*E[0]
	M[0] = np.sum(reticulo)

	for n in range(1, nsteps):

		#Se selecciona una entrada aleatoria en el retículo

		i = random.randrange(0, len(reticulo))
		j = random.randrange(0, len(reticulo[i]))

		#Se calcula el cambio en la energía

		Delta_E =2*reticulo[i,j]*(reticulo[i, (j+1) % len(reticulo[i])] + reticulo[i, (j-1) % len(reticulo[i])] + reticulo[(i+1) % len(reticulo), j] + reticulo[(i-1) % len(reticulo), j]) 

		#Se decide si se acepta el cambio

		if (Delta_E <= 0) or (random.uniform(0, 1) < np.exp(-L*Delta_E)):
			reticulo[i,j] = -reticulo[i,j]
			E[n] = E[n-1] + Delta_E
			M[n] = M[n-1] + 2*reticulo[i,j]
		else:
			E[n] = E[n-1]
			M[n] = M[n-1]
		

	#Se hacen graficas de la evolución de la energía

	if t in energy_graphs:	

		fig, ax = plt.subplots()
		ax.plot(range(0, nsteps), E/(N*N))
		ax.set_xlabel("Iteración")
		ax.set_ylabel("Energía por sitio ($J$)")
		ax.set_title("$T=%.2f J/K_B$, $N=%d$" % (temperaturas[t], N*N))
		fig.savefig("%.2f_energia.png" % temperaturas[t])
		plt.close(fig) 

	#Se guarda el valor de la energía promedio y la magnetización promedio

	E_promedio[t] = np.mean(E[nsteps_equilibrio:])
	M_promedio[t] = np.mean(M[nsteps_equilibrio:])

#Se grafica la magnetización y la energía promedio

fig, ax = plt.subplots()
ax.scatter(temperaturas, E_promedio/(N*N), alpha = 0.3)
ax.set_xlabel("Temperatura ($J/K_B$)")
ax.set_ylabel("Energía por sitio ($J$)")
ax.set_title("$N=%d$, $%d$ pasos con $%d$ para estabilizar" % (N*N, nsteps, nsteps_equilibrio))
fig.savefig("energia.png")
plt.close(fig)

fig, ax = plt.subplots()
ax.scatter(temperaturas, M_promedio/(N*N), alpha = 0.3)
ax.set_xlabel("Temperatura ($J/K_B$)")
ax.set_ylabel("Magnetización por sitio")
ax.set_title("$N=%d$, $%d$ pasos con $%d$ para estabilizar" % (N*N, nsteps, nsteps_equilibrio))
fig.savefig("magnetizacion.png")
plt.close(fig)


