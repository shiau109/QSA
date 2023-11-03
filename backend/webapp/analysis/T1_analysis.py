import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sco

def expdecay(x,a, b,c):
    #p: amp, tau, offset
    return a*np.exp(-x/b)+c

def readfile(s):
    #T1, I, Q
    t_I_Q = []
    f = open(s,"r")
    for line in f.readlines():
        line = line.strip()
        line = line.split(",")
        t_I_Q.append([line[0],line[1],line[2]])
    t_I_Q.remove(['<b>T1</b>', 'I', 'Q'])
    t_I_Q = np.array(t_I_Q)
    return t_I_Q
def project_line(I0, Q0, I1, Q1):
    t_I_Q = readfile("1DSingle_Qubit.csv")
    pro = []
    a = np.array([I1-I0,Q1-Q0])
    for i in range(101):
        b = np.array([[float(t_I_Q[i,1])-I0],[float(t_I_Q[i,2])-Q0]])
        c = np.dot(a,b)/((I1-I0)**2+(Q1-Q0)**2)**0.5
        pro.append([float(t_I_Q[i,0]),c[0]])
    pro = np.array(pro)
    return pro
def data_project():
    return
a = readfile("1DSingle_Qubit.csv")
I1 = float(a[0,1])
Q1 = float(a[0,2])
I0 = float(a[100,1])
Q0 = float(a[100,2])
xdata = project_line(I0, Q0, I1, Q1)[:,0]/10**6
ydata = project_line(I0, Q0, I1, Q1)[:,1]
print(xdata)
plt.plot(xdata,ydata)


popt, pcov = sco.curve_fit(expdecay, xdata, ydata)
print(popt)
plt.plot(xdata,expdecay(xdata,*popt))
plt.show()
