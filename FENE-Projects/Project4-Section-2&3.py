import math
import matplotlib.pyplot as plt
import numpy as np
import pylab
import sys
import numpy
import random
#numpy.set_printoptions(threshold=np.inf)
#with open("C:/Users/alexl/OneDrive/Escritorio/Datis.txt","w") as f:

N=1000
dt=0.1
time2=2
L=100
gamma = [0.1,1,10]		#Values of the strength of the force
D = [0.01,0.1,1]		#Values of the strength of the noise
k=0
divisions=10000			#Divisions of the system
#F=np.zeros(n)
deltax = L/divisions
x=np.arange(0,L,deltax)	#Discretization of the system in boxes of length deltax
M=5				#Configurations of the random force

MSD =np.zeros( (M,int(time2/dt)) )

for gamma, D in zip(gamma,D):		#This loop runs over the two lists at the same time
	for m in range(M):
		print(m)
		F= (np.sqrt(2*gamma))*np.random.normal(0, 1,divisions)	#Creation of the random force
		plt.title('Γ = '+str(gamma))
		plt.plot(x,F)
		plt.xlabel('L')
		plt.show()
		x_real=np.zeros((int(time2/dt),N))
		x_msd=np.zeros((int(time2/dt),N))
		for i in range(N):
			x_real[0,i]=np.random.uniform(0,L)
			x_msd[0,i]=np.random.uniform(0,L)

		for n in range(N):
				for t in range(int(time2/dt)-1):
					if x_real[t,n] > L:
						Fi=F[int(x_real[t,n]-L)]
						Fi=F[int(x_msd[t,n]-L)]
					elif x_real[t,n] < 0:
						Fi=F[int(x_real[t,n]+L)]
						Fi=F[int(x_msd[t,n]+L)]
					else:
						Fi = F[int(x_real[t,n])]
						Fi = F[int(x_real[t,n])]

					x_real[t+1,n]=(np.sqrt(2*D*dt))*np.random.normal(0, 1)+(np.sqrt(dt))*Fi+x_real[t,n]
					x_msd[t+1,n]=(np.sqrt(2*D*dt))*np.random.normal(0, 1)+(np.sqrt(dt))*Fi+x_msd[t,n]
					
					if x_real[t+1,n] > L:		#PBC
						x_real[t+1,n] = 0

		for j in range(int(time2/dt)-1):
			for n in range(N):
				MSD[m,j] = MSD[m,j] + ((x_msd[j+1,n]-x_msd[0,n])**2)

	globals()['MSD'+str(k)] = MSD/N
	k=k+1
	print(x_real)


MSD_total0 = numpy.sum(MSD0, axis=0)/M 	#Average over all the configurations
MSD_total1 = numpy.sum(MSD1, axis=0)/M
MSD_total2 = numpy.sum(MSD2, axis=0)/M


time3=np.arange(0,time2,dt)
plt.plot(time3[0:int(time2/dt)-1],MSD0[0,:-1], label = "Γ=0.1, D=0.01")
plt.plot(time3[0:int(time2/dt)-1],MSD1[0,:-1],label = "Γ=1, D=0.1")
plt.plot(time3[0:int(time2/dt)-1],MSD2[0,:-1],label = "Γ=10, D=1")
#plt.plot(time3[0:int(time2/dt)-1],2*time3[0:int(time2/dt)-1]**0.5)
plt.xlabel('t')
plt.ylabel('MSD')
plt.yscale('log')
plt.xscale('log')
plt.legend(loc="upper left")
plt.show()

print(len(x),len(F))
plt.plot(x,F)
plt.xlabel('L')
plt.show()