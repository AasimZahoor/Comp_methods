#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 20:53:38 2020

@author: aj3008
"""

#%%
#-------------------------------------------libraries--------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import math
import sympy as sp
#-----------------------------------------Extracting data----------------------------------------
data=np.loadtxt("RV_data.txt",usecols=[0,1,2,3,4])
t=[data[i][0]-2454987.097346 for i in range(len(data))]
delT=2455110.814132-2454987.097346
I=data[:,1]
tn=[]
#---------------------------------------------Folding--------------------------------------------
for i in range(len(data)):
    tn.append(t[i]%3.5485)
    
    

#----------------------------------------function to model speed---------------------------------
def sin(tn,q):
    if isinstance(q,list)==True:
        v=q[0]
        phase=q[1]
    else:
        phase=0.17*3.14
        v=q
        
    f=[]
    for i in range(len(tn)):
        omega=2*3.14/3.5485
        a=v*math.cos(omega*tn[i]+phase)
        f.append(a)
    return(f)
#-------------------------------------------finding phase graphically-----------------------------
plt.title("checking the phase")
plt.plot(tn,I,"x")
plt.plot(tn,sin(tn,240),"o")
plt.show()

#-----------------------------------Defining the likelihood function-----------------------------------
def Like(I,s):
    sum=0
    for i in range(len(I)):
#        sum =sum+(1/(np.sqrt(2*3.14)))*np.exp(-0.5*(I[i]-s[i])**2)
        sum=sum+math.log(1/(np.sqrt(2*3.14)))-0.5*(I[i]-s[i])**2
    return(sum)

#-----------------------------------------------MCMC------------------------------------------------------
i=0
xt=200
distd=[]
while i<1000:
    print(i)
    y=np.random.normal(xt)
    while abs(y)>300:              #knowing that velocity isn't higher than that in this case(prior)
        y=np.random.normal(xt)
    num=Like(I,sin(tn,y))
    den=Like(I,sin(tn,xt))
    r=math.exp(num-den)
    if r>=1:
        xt=y
    else:
        u=np.random.uniform(0,1)
        if u<=r:
            xt=y
            
        else:
            xt=xt
    i=i+1
    distd.append(xt)
    
prob=[]
sum=0
for i in range(len(distd)):
    print(i)
    a=sp.exp(Like(I,sin(tn,distd[i])))
    sum=sum+a
    prob.append(a)
prob=[prob[i]/sum for i in range(len(prob))]     #normalising
ind=prob.index(max(prob))
print("the velocity is=",distd[ind],"m/s")


b=distd[ind]
#-------------------------------------marginalised distribution-----------------------------------------
plt.title("marginalised distribution")
plt.plot(distd,prob,"x")
plt.show()
#-----------------------------------------------error-------------------------------
sum=0
for i in range(len(distd)):
    sum=sum+distd[i]
avg=sum/len(distd)
dev=0
for i in range(len(distd)):
    dev=dev+(distd[i]-avg)**2
dev=np.sqrt(dev)/len(distd)

#------------------------------------------------Plotting-----------------------------------------------------
plt.title("comparing data with model")
plt.plot(tn,I,"x")
box=sin(tn,b)
plt.plot(tn,box,"x")

#------------------------------------------------Calculating mass----------------------------------------------

G=6.67408*10**(-11)     #m3 kg-1 s-2
M_sun=2*10**30          #kg
period=3.5485*24*3600   #in seconds
radius=(((G*1.35*M_sun)/(2*3.14)**2)*period**2)**(1/3)    # in meters
velocity=(2*3.14*radius)/period
mass=1.35*b/velocity
print("mass of planet is=",mass,"M_sun")
rad=0.15*7*10**8    #m
volume=(4/3)*3.14*rad**3
density=mass*M_sun/volume
print("density is=",density,"kg/m**3")






