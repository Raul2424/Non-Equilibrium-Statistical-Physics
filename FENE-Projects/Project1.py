import math
import matplotlib.pyplot as plt
import numpy as np
import pylab
import sys
import numpy



N=1000
dt=0.01
time2=25
L=100
mu=0
sigma=1
gamma2 = [0.1,1,3,5,10,15]
delta=np.sqrt(2)
k=0

x=np.zeros((int(time2/dt),N))	#Create two arrays of arrays, one for each position variable. N arrays of all the time length.
y=np.zeros((int(time2/dt),N))	#Each array is a particle, and each element is a time-step.

D=np.zeros(6)
for gamma2 in gamma2:			#Loop that repeats all the simulation with a different value of gamma (Γ)
	print(gamma2)
	for i in range(N):
		x[0,i]=np.random.uniform(0,L)	#Initialize all the particles at t=0 (element 0)
		y[0,i]=np.random.uniform(0,L)

	for n in range(N):
		for t in range(int(time2/dt)-1):
			x[t+1,n]=(np.sqrt(2*gamma2*dt)/delta)*np.random.normal(mu, sigma)+x[t,n]	#Let evolve all the particles according to the random walk physics
			y[t+1,n]=(np.sqrt(2*gamma2*dt)/delta)*np.random.normal(mu, sigma)+y[t,n]




	MSD=np.zeros(int(time2/dt))	#MSD has the same length of the time

	for j in range(int(time2/dt)-1):
			for n in range(N):
					MSD[j] = MSD[j] + ((x[j+1,n]-x[0,n])**2+(y[j+1,n]-y[0,n])**2)	#Compute MSD at each t, summing over all particles and comparing to t=0 (x[0,n],y[0,n])

	D[k] = MSD[-2]/(4*int(time2/dt)) #MSD[-2] is the last element of the list MSD. D is computed for each value of Γ
	globals()['MSD'+str(k)] = MSD/N		#Create a different variable each round of the loop
	k=k+1


#The necessary plots:
time3=np.arange(0,time2,dt)
plt.title('MSD vs t')
plt.plot(time3[0:int(time2/dt)-1],MSD0[0:int(time2/dt)-1],label = 'Γ = 0.1')
plt.plot(time3[0:int(time2/dt)-1],MSD1[0:int(time2/dt)-1],label = 'Γ = 1')
plt.plot(time3[0:int(time2/dt)-1],MSD2[0:int(time2/dt)-1],label = 'Γ = 3')
plt.plot(time3[0:int(time2/dt)-1],MSD3[0:int(time2/dt)-1],label = 'Γ = 5')
plt.plot(time3[0:int(time2/dt)-1],MSD4[0:int(time2/dt)-1],label = 'Γ = 10')
plt.plot(time3[0:int(time2/dt)-1],MSD5[0:int(time2/dt)-1],label = 'Γ = 15')
plt.xlabel('t')
plt.ylabel('MSD')
plt.yscale('log')
plt.xscale('log')
plt.legend(loc="upper left")
plt.show()

gamma2 = [0.1,1,3,5,10,15]
m,b = np.polyfit(gamma2, D, 1)
print(m,b)

plt.title('D vs Γ')
plt.plot(gamma2,D,'.', label = 'Simulation Points', markersize=10)
plt.plot(gamma2,np.multiply(gamma2,m), label = 'D = '+str("%0.4f"%m)+' Γ')
plt.xlabel('Γ')
plt.ylabel('D')
plt.legend(loc="upper left")
plt.show()

