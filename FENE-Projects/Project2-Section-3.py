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
	for i in range(0,len(M)):
		circle1 = plt.Circle(M[i], a, color='r')
		ax.add_patch(circle1)


	plt.xticks([0,25,50])
	plt.yticks([0,25,50])
	ax.set_aspect( 1 )
	plt.show()

Config = 1
L=50
a=1
Mc_steps = 10000
MSD = np.zeros((Config,Mc_steps))
time = np.arange(0,Mc_steps,1)
k = 0
delta = 0.05

"""
φ = 0.05, N = 39		#Number of particles computed according with the formula φ = N*pi*a**2/L**2, with L,a, and φ fixed.
φ = 0.2, N = 159
φ = 0.5, N = 397
φ = 0.7, N = 557
"""
num = math.sqrt(3)/2
N=[557]

for N in N:				#Repeats the experiment with different N each time (diferent system density)
	for m in range(Config):
		print(N)
		M=[()]
		column = 1
		row = 0

		
		while len(M)<N+1:										#Algorithm that places particles in a triangular lattice starting from the bottom.
			if column%2 == 0:
				if row != 0:
					M.append(((2*row+1)*a-a,2*column*a-a))
				row = row + 1
			if column%2 != 0:
				M.append(((2*row)*a+a,2*column*a-a))
				row=row+1
			if row == int(L/(2*a)):
				column = column + 1
				row = 0
		

		M.remove(M[0])
		show_particles()
		M_ini = list(M)

		for i in range(Mc_steps):		#Same metodology as in section 2.
				print(i)
				for jj in range(N):
					randd = random.randint(0, N-2)
					part = list(M[randd])
					part_prov = list(part)
					M.remove(M[randd])
					part[0] = part[0] +delta*(np.random.uniform(0,1)-0.5)
					part[1] = part[1] +delta*(np.random.uniform(0,1)-0.5)
					
					part = tuple(part)
					part_prov = tuple(part_prov)
					min_dist2 = math.sqrt(min((part[0]-x[0])**2+(part[1]-x[1])**2 for x in M))

					if min_dist2 > 2*a:
						M.insert(randd,tuple(part))
					else:
						M.insert(randd,tuple(part_prov))

					for n in range(N-1):
						MSD[m,i] = MSD[m,i] + (M_ini[n][0]-M[n][0])**2 + (M_ini[n][1]-M[n][1])**2
		show_particles()
		plt.title('MSD vs t')
		plt.plot(time,MSD[0]/N,'.', label = 'φ = 0.05')
		plt.yscale('log')
		plt.xscale('log')
		plt.xlabel('t (MC_steps)')
		plt.ylabel('MSD')
		plt.legend(loc="upper left")
		plt.show()
		globals()['MSD'+str(k)] = MSD/N
	k = k + 1



show_particles()
print(MSD0)
MSD_total = np.zeros(Mc_steps)
for j in range(Mc_steps):								#Computtion of the Maggnetization averageed over all the configurations
	for i in range(Config):
		MSD_total[j] = MSD0[i,j] + MSD_total[j]

MSD_total = MSD_total/Config
print(MSD_total)
N=[249,995,2487,3482]

plt.title('MSD vs t')
plt.plot(time,MSD_total, label = 'φ = 0.05')
#plt.plot(time,MSD1, label = 'φ = 0.2')
#plt.plot(time,MSD2, label = 'φ = 0.5')
#plt.plot(time,MSD3, label = 'φ = 0.7')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('t (MC_steps)')
plt.ylabel('MSD')
plt.legend(loc="upper left")
plt.show()
#MSD_all = (MSD[Mc_steps])/N
