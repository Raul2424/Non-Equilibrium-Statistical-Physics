import random
import numpy as np
import matplotlib.pyplot as plt
import math


#Function that makes the plot of the system, given a matrix M, which contains the position and the spin value of each spin.
def show_particles(M):
	fig, ax = plt.subplots()
	for i in range(0,len(M)):
		if M[i][2] == 1:									#If the spins value is +1, is coloured in red
			circle1 = plt.Circle(M[i], a/2.5, color='r')
		if M[i][2] == -1:									#If the spins value is +1, is coloured in blue
			circle1 = plt.Circle(M[i], a/2.5, color='b')
		ax.add_patch(circle1)


	plt.xticks([-1,25,50,75])
	plt.yticks([-1,25,50])
	ax.set_aspect( 1 )
	plt.show()


#Function that returns the magnetization of the system, given M 
def magnetization(M):
	magg=0

	for i in range(len(M)):
		magg = magg + M[i][2]
	return magg

#Function that returns a list, which is all the positions of the 6 neighbours from the spin given (randd).More detail inside the comments of the function.
def bc(randd,L,M):
	if 1 <= randd <= L-2:						#Spines de la de arista de abajo menos los vértices
		a = randd+1
		b=L*(L-1)+2
		c=L*(L-1)+1
		d=randd-1
		e=randd+L-1
		f=randd+L

	elif L*(L-1)+1 <= randd <= len(M)-2:			#Spines de la arista de arriba menos vértices
		a = randd+1
		b=randd-L+1
		c=randd-L
		d=randd-1
		e=len(M)-randd-3
		f=len(M)-randd-2

	elif randd in [L,2*L]:						#Spines de la arista izquierda menos vértices
		a = randd+1
		b=randd-L+1
		c=randd-L
		d=randd+L-1
		e=randd+2*L-1
		f=randd+L

	elif randd in [2*L-1,3*L-1]:					#Spines de la arista derecha menos vértices
		a = randd-L+1
		b=randd-2*L+1
		c=randd-L
		d=randd-1
		e=randd+L-1
		f=randd+L

	elif randd == 0:								#Vértice de abajo a la izquierda
		a = 1
		b=L*(L-1)+1
		c=L*(L-1)
		d=L-1
		e=2*L-1
		f=L

	elif randd == L-1:							#Vértice de abajo a la derecha
		a = 0
		b= len(M)-L
		c=L*L-1
		d=L-2
		e=2*L-2
		f=2*L-1

	elif randd == len(M)-L:						#Vértice de arriba a la izquierda
		a = len(M)-L
		b= len(M)-2*L+1
		c=L*(L-2)
		d=len(M)-1
		e=L-1
		f=0

	elif randd == len(M)-1:						#Vértice de arriba a la derecha
		a = len(M)-L
		b= L*(L-2)
		c=L*L-L-1
		d=len(M)-2
		e=L-2
		f=0

	else:										#Todos los otros spines
		a = randd+1
		b= randd-L+1
		c=randd-L
		d=randd-1
		e=randd+L-1
		f=randd+L

	return [a,b,c,d,e,f]

#Function that returns the energy of interaction with the 6 NN (lista1), given a particular spin (randd), and the Matrix M.
def energy(randd,lista1,M):
	energia = -J*M[randd][2]*(M[lista1[0]][2]+M[lista1[1]][2]+M[lista1[2]][2]+M[lista1[3]][2]+M[lista1[4]][2]+M[lista1[5]][2])
	return energia


a=1
L=50	#Number of spins per edge
steps=300
J=1
num=math.sqrt(3)/2   #Parameter of the triangular lattice: gives the height of the next file respect the present one.
M=[()]
M_prov=[()]
Config=1
Magg = np.zeros( (Config,steps+1) )
Magg_total=np.zeros(steps+1)

for m in range(Config):						#Loop that goes over all the different Configurations
	print(m)
	i,k,k2,k4,column,total=0,0,0,0,0,0    #Parameters needed to build the rhombus figure made of a triangular lattice
	k3=1
	M=[()]
	M_prov=[()]
	while total<L:
		if i%2==0:	# if the file is even
			while column<(int(L/a)):	
				M.append((a*column+k2*a,num*a*i,[-1,1][random.randrange(2)]))	#Append to M, a tuple with: (position x, position y, spin value). The spin value is chosen at random between -1 and +1.
				column = column+1
			column = 0
			k2=k2+1
			i=i+1
			k=k+2
			total=total+1

		if i%2!=0:	#if the file is odd
			while column<int(L/a):
				M.append((k4*a+(2*column+1)/2,num*a*i,[-1,1][random.randrange(2)]))
				column = column+1
			column=0
			k3=k3+2
			i=i+1
			k4=k4+1
			total=total+1
	M.remove(M[0])
	print(magnetization(M))


	for i in range(steps):
		for n in range(L*L):
			randd = random.randint(0, len(M)-1)		#Spin choosen at random
			lista=bc(randd,L,M)						#The 6 Nearest Neighbours are found.

			energia = energy(randd,lista,M)			#Energy of that interaction

			M_prov = list(M)						#A provisional(virtual) change is made
			M_prov[randd]=list(M[randd])
			M_prov[randd][2] = M_prov[randd][2]*(-1)
			M_prov[randd]=tuple(M_prov[randd])

			energia_cambio = energy(randd,lista,M_prov)		#Energy of the virtual change
			delta_energ = (energia_cambio-energia)			#Change in energy between the virtual change and the current state.
			#show_particles(M)

			M[randd]=list(M[randd])
			if delta_energ <= 0:							#If the change in energy is negative or zero (if it lowers the energy or remains the same), the change in the spin value is accepted
				M[randd][2] = M[randd][2]*(-1)

			
			if delta_energ > 0:								#If the change in energy is positive (raises the energy) the change is not made.
				M[randd][2] = M[randd][2]

			#Little digression here: This is the actual Metropolis algorithm when the energy of the system in the virtual change is raised:
			#It is compared with a random number between 0 and 1. In this section, the simulation is made at T=0. The exponential is "infinity", so the change would be never accepted.
			"""
			if delta_energ > 0:								#This is the actual 
				r=np.random.rand()
				if np.exp(-delta_energ/0.01) > r:
					M[randd][2]=M[randd][2]*(-1)
				if np.exp(-delta_energ/0.01) < r:
					M[randd][2]=M[randd][2]*(1)
			"""

		Magg[m,i+1] = math.sqrt((magnetization(M)**2))/(L*L)	#The value of the magnetization is computed at each time step. Here, the magnetization is
															#taken in absolute value because we are interested to see ordering of the system (magg raises),
															#we don't care if it ends all spins up or down.
	show_particles(M)

#print(Magg)
for k in range(steps+1):								#Computtion of the Maggnetization averageed over all the configurations
	for i in range(Config):
		Magg_total[k] = Magg[i,k] + Magg_total[k]

Magg_total=Magg_total/Config
#print(Magg_total)
show_particles(M)
#Plots
time = np.arange(0,steps+1,1)
plt.title('MSD vs t')
plt.xlabel('t (MC_steps)')
plt.ylabel('MSD^2/N')
plt.plot(time,Magg_total)
plt.show()
