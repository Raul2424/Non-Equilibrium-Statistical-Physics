import random
import numpy as np
import matplotlib.pyplot as plt
import math
from collections import Counter




def show_particles(M):
	fig, ax = plt.subplots()
	for i in range(0,len(M)):
		if M[i][2] == 1:
			circle1 = plt.Circle(M[i], 0.3, color='r')
		if M[i][2] == -1:
			circle1 = plt.Circle(M[i], 0.3, color='b')
		ax.add_patch(circle1)


	plt.xticks([-1,25,50,75])
	plt.yticks([-1,25,50])
	ax.set_aspect( 1 )
	plt.show()

def magnetization(M):
	magg=0

	for i in range(len(M)):
		magg = magg + M[i][2]
	return magg

def bc(randd,L,M):
	if 1 <= randd <= L-2:						#Spines de abajo menos extremos
		a1 = randd+1
		b=L*(L-1)+2
		c=L*(L-1)+1
		d=randd-1
		e=randd+L-1
		f=randd+L

	elif L*(L-1)+1 <= randd <= len(M)-2:			#Spines de arriba menos extremos
		a1 = randd+1
		b=randd-L+1
		c=randd-L
		d=randd-1
		e=len(M)-randd-3
		f=len(M)-randd-2

	elif randd in [L,2*L]:						#Spines de la izquierda menos extremos
		a1 = randd+1
		b=randd-L+1
		c=randd-L
		d=randd+L-1
		e=randd+2*L-1
		f=randd+L

	elif randd in [2*L-1,3*L-1]:					#Spines de la derecha menos extremos
		a1 = randd-L+1
		b=randd-2*L+1
		c=randd-L
		d=randd-1
		e=randd+L-1
		f=randd+L

	elif randd == 0:								#Spin de abajo a la izquierda
		a1 = 1
		b=L*(L-1)+1
		c=L*(L-1)
		d=L-1
		e=2*L-1
		f=L

	elif randd == L-1:							#Spin de abajo a la derecha
		a1 = 0
		b= len(M)-L
		c=L*L-1
		d=L-2
		e=2*L-2
		f=2*L-1

	elif randd == len(M)-L:						#Spin de arriba a la izquierda
		a1 = len(M)-L
		b= len(M)-2*L+1
		c=L*(L-2)
		d=len(M)-1
		e=L-1
		f=0

	elif randd == len(M)-1:						#Spin de arriba a la derecha
		a1 = len(M)-L
		b= L*(L-2)
		c=L*L-L-1
		d=len(M)-2
		e=L-2
		f=0

	else:
		a1 = randd+1
		b= randd-L+1
		c=randd-L
		d=randd-1
		e=randd+L-1
		f=randd+L

	return [a1,b,c,d,e,f]

def energy(randd,lista1,M):
	energia = -J*M[randd][2]*(M[lista1[0]][2]+M[lista1[1]][2]+M[lista1[2]][2]+M[lista1[3]][2]+M[lista1[4]][2]+M[lista1[5]][2])
	return energia


a=1
L=50	#Number of spins per edge. The sistem has L*L spins then.
steps=20000
Magg = np.zeros(steps)
J=1
num=math.sqrt(3)/2   #Parameter of the triangular lattice: gives the height of the next file respect the present one.
M=[()]
M_prov=[()]
i,k,k2,k4,column,total=0,0,0,0,0,0    #Parameters needed to build the rhombus figure made of a triangular lattice
k3=1
while total<L:
	if i%2==0:
		while column<(int(L/a)):
			M.append((a*column+k2*a,num*a*i,[-1,1][random.randrange(2)]))
			column = column+1
		column = 0
		k2=k2+1
		i=i+1
		k=k+2
		total=total+1

	if i%2!=0:
		while column<int(L/a):
			M.append((k4*a+(2*column+1)/2,num*a*i,[-1,1][random.randrange(2)]))
			column = column+1
		column=0
		k3=k3+2
		i=i+1
		k4=k4+1
		total=total+1 						#The system is initiated.
M.remove(M[0])
counter=0


Pl=[1,1,1,1,0,0,0]											#Probability of change according to the rules: decrease in energy or 0, accepted. increase in energy rejected.
#Pl corresponds to energy changes of [-12,-8-4,0,4,8,12]	#Temperature has no role in probabilities because T=0.
t=0 														#Start time.
time = np.zeros(steps)
l=[0,1,2,3,4,5,6]											#Array that accounts for the class of eache E change. Order: [-12,-8-4,0,4,8,12]

show_particles(M)
for i in range(steps):
	#print(i)
	gll=[[],[],[],[],[],[],[]]								#Array of arrays. Each inner array corresponds to an energy change. [-12,-8,-4,0,8,12]
	for rand in range(len(M)):							#Loop that goes over all the spins
		lista = bc(rand,L,M)
		energy_rand = -2*energy(rand,lista,M)				#The energy of a virtual change of each spin is computed.

		if energy_rand == -12:								#According to the energy change, the spin is appended in an specific array of gll
			gll[0].append(rand)
		if energy_rand == -8:
			gll[1].append(rand)
		if energy_rand == -4:
			gll[2].append(rand)
		if energy_rand == 0:
			gll[3].append(rand)
		if energy_rand == 4:
			gll[4].append(rand)
		if energy_rand == 8:
			gll[5].append(rand)
		if energy_rand == 12:
			gll[6].append(rand)

	#gl_new accounts for the number spins in each specidic energy change. Hence, the sum of all the components of gll_new, must be L*L.
	gl_new = [len(gll[0]),len(gll[1]),len(gll[2]),len(gll[3]),len(gll[4]),len(gll[5]),len(gll[6])]
	#print(gll)
	#print(gl_new)
	
	weights=np.multiply(gl_new,Pl)					#Multiplication of the probabilities, with the number of spins of each E change.
	#print(weights)
	Q =1-sum(np.multiply(gl_new,Pl))/(L*L)			#Compute of Q where the sum is normalized.
	if Q == 1:
		break
	weights2=weights/sum(weights)					#Weights normalized by the sum of all
	li = random.choices(l, weights=weights, cum_weights=None, k=1)		#Selects a class from l, according to the weights.
	li=li[0]										#Conversion to a number
	r=random.randint(0, len(gll[li])-1)				#random number generated between 0 and the number of spins of the class selected

	M[gll[li][r]] = list(M[gll[li][r]])				#Change made in the particular spin selected
	M[gll[li][r]][2] = M[gll[li][r]][2]*(-1)
	M[gll[li][r]] = tuple(M[gll[li][r]])

	delta_t = 1+int(math.log(np.random.uniform(0,1))/math.log(Q))		#Calculation of delta_t, theoretical time that we have to wait for that particular change to happen.
	t = t + delta_t									#Calculation of the "true time"

	time[i] = t
	Magg[i] = math.sqrt((magnetization(M)**2))/(L*L)
	print(Magg[i])
	counter=counter+1

Magg=Magg[Magg != 0]
#Plots
print(t)
print(np.max(np.nonzero(Magg)))
show_particles(M)
plt.plot(time[:len(Magg)],Magg)
plt.xlabel('t')
plt.ylabel('MSD')
plt.show()
