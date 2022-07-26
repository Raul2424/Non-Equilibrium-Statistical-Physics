import math
import matplotlib.pyplot as plt
import numpy as np
import pylab
import sys
import numpy

N=1000
dt=0.001
time2=10
L=100
mu=0
sigma=1
D = [0.01,0.1,1]			#Accounts for the strength of the noise
k=0
Diff = np.zeros(len(D))


#Essentially the same procedure than in project 1.
x_real=np.zeros((int(time2/dt),N))		#x position real value (accounts the Periodic Boundary Conditions)
x_msd=np.zeros((int(time2/dt),N))		#x position to compute msd (no PBC)

for D in D:
	print(D)
	for i in range(N):
		x_real[0,i]=np.random.uniform(0,L)	#Random inizialization of the walkers
		x_msd[0,i]=np.random.uniform(0,L)

	for n in range(N):
			for t in range(int(time2/dt)-1):
				x_real[t+1,n]=(np.sqrt(2*D*dt))*np.random.normal(mu, sigma)+x_real[t,n]		#Change in variables
				x_msd[t+1,n]=(np.sqrt(2*D*dt))*np.random.normal(mu, sigma)+x_msd[t,n]
				
				if x_real[t+1,n] > L:		#PBC
					x_real[t+1,n] = 0

	MSD=np.zeros(int(time2/dt))

	for j in range(int(time2/dt)-1):
			for n in range(N):
					MSD[j] = MSD[j] + ((x_msd[j+1,n]-x_msd[0,n])**2)
				
	Diff[k] = MSD[-2]/(2*int(time2/dt))		#Calculation of the difussion constant at large t. Now is a 2 because the Brownian walker is in 1D.
	globals()['MSD'+str(k)] = MSD/N		#Create a different variable each round of the loop
	k = k+1

time3=np.arange(0,time2,dt)


#Plots
plt.title('MSD vs t')
plt.plot(time3[0:int(time2/dt)-1],MSD0[0:int(time2/dt)-1], label = 'D = 0.01')
plt.plot(time3[0:int(time2/dt)-1],MSD1[0:int(time2/dt)-1],label = 'D = 0.1')
plt.plot(time3[0:int(time2/dt)-1],MSD2[0:int(time2/dt)-1], label = 'D = 1')
plt.xlabel('t')
plt.ylabel('MSD')
plt.yscale('log')
plt.xscale('log')
plt.legend(loc="upper left")
plt.show()

D = [0.01,0.1,1]

plt.title('Difussion constant vs D')
plt.plot(D,Diff,'.')
plt.xlabel('D')
plt.ylabel('Diffusion constant')
plt.show()
