import random
import math
import matplotlib.pyplot as plt
import numpy as np
import pylab
import itertools
import pandas as pd
from skimage.draw import disk
import random


def show_particles():
	fig, ax = plt.subplots()
	for i in range(0,N):
		circle1 = plt.Circle(M[i], a, color='r')
		ax.add_patch(circle1)


	plt.xticks([0,25,50])
	plt.yticks([0,25,50])
	ax.set_aspect( 1 )
	plt.show()	#Function that plots 	#Function that plots a certain configuration of the system given M.

L=50
a=0.2 #Radius of the particle needed to reach φ = 0.05, according to the formula: φ = N*pi*a**2/L**2. There is no 4 in the denominator because i'm using the radius instead of the diameter.
N = 10	
Mc_steps = 100

MSD = np.zeros(Mc_steps)
time = np.arange(0,Mc_steps,1)
#print(M_ini)
delta = [0.001,0.003,0.01,0.03,0.1,0.3]
D = np.zeros(len(delta))
k = 0    #dumb counter

for delta in delta:															#Loop that repeats the simulation varying the value of delta.
	print(delta)																#Here, the first particle is placed
	M = [(np.random.uniform(a,L-a),np.random.uniform(a,L-a))]					#M is an array of tuples of two values. Each tuple is a particle. The first element of each tuple is position x.The second element of each tuple is position y.
	while len(M) < N:															#Loop keeps going until all particles are placed
		c = (np.random.uniform(a,L-a),np.random.uniform(a,L-a))					#Put another particle with uniform distribution inside the box.
		min_dist = math.sqrt(min((c[0]-x[0])**2+(c[1]-x[1])**2 for x in M))		#we calculate the minimum distance between the particle placed and all the others
		if min_dist < 2*a:														#If thhat distance is less than 2 times the radius, the particle is not placed, and another try is made
				#condition = False
				#break
				pass
		else:																	#If that distance is more than 2 times the radius, the particle is placed.
			M.append(c)
	#show_particles()
	M_ini = list(M)																#I freeze the initial state of the system in M_ini
	for i in range(Mc_steps):													#Loop that goes over all the Montecarlo steps
		print((i/Mc_steps)*100,'% ')
		for jj in range(N):														#Each MC step consists in N trials of change
			randd = random.randint(0, N-1)										#Select on particle at random
			part = list(M[randd])												#Convert to list to make changes
			part_prov = list(part)												#Store in part_prov the position of this particle
			M.remove(M[randd])													#I remove the particle from the matrix M (later this will have sense)
			part[0] = part[0] +delta*(np.random.uniform(0,1)-0.5)				#Modifications in the positions
			part[1] = part[1] +delta*(np.random.uniform(0,1)-0.5)
			"""																	#Periodic boundary conditions, not used in this simulation
			if part[0] > 50-a:
				#break
				part[0] = a
			if part[0] < a:
				#break
				part[0] = L - a
			if part[1] > 50-a:
				#break
				part[1] = a
			if part[1] < a:
				#break
				part[1] = L - a
			"""
			part = tuple(part)
			part_prov = tuple(part_prov)
			min_dist2 = math.sqrt(min((part[0]-x[0])**2+(part[1]-x[1])**2 for x in M))	#Minimum distance between the particle changed and all the other particles.

			if min_dist2 > 2*a:															#If the distance is greater than 2*a (there is no overlap). Insert the tuple(positions of the particle changed) just in the place where was removed
				M.insert(randd,tuple(part))
			else:																		#If the distance is greater than 2*a (there IS overlap). Insert the tuple(positions of the particle NOT changed) just in the place where was removed
				M.insert(randd,tuple(part_prov))


			for n in range(N):
				MSD[i] = MSD[i] + (M_ini[n][0]-M[n][0])**2 + (M_ini[n][1]-M[n][1])**2

	D[k] = MSD[Mc_steps-1]/(4*Mc_steps)
	#D[k] = MSD[Mc_steps]/N
	globals()['MSD'+str(k)] = MSD/N    		#New variable with different name at each round.
	
	k = k + 1
	#MSD_all = (MSD[Mc_steps])/N


#Plots
delta = [0.001,0.003,0.01,0.03,0.1,0.3]
#print(delta)
plt.title('MSD vs t')
plt.plot(time,MSD0, label = 'δ=0.001')
plt.plot(time,MSD1, label = 'δ=0.003')
plt.plot(time,MSD2, label = 'δ=0.01')
plt.plot(time,MSD3, label = 'δ=0.03')
plt.plot(time,MSD4, label = 'δ=0.1')
plt.plot(time,MSD5, label = 'δ=0.3')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('t (MC_steps)')
plt.ylabel('MSD')
plt.legend(loc="upper left")
plt.show()


delta_por = np.multiply(delta,1.1)
m,b = np.polyfit(delta, D, 1)
plt.title('D vs δ')
plt.xlabel('δ')
plt.ylabel('D')
plt.plot(delta,D,'.', markersize = 10, label='Simulation')
plt.plot(delta,np.exp(delta_por)-1, label = 'D = '+str("%0.4f"%m)+' δ')
plt.legend(loc="upper left")
plt.show()
show_particles()