import numpy as np
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
def project_line(I0, Q0, I1, Q1, t_I_Q, N):
    pro = []
    a = np.array([I1-I0,Q1-Q0])
    for i in range(N):
        b = np.array([[float(t_I_Q[i,0])-I0],[float(t_I_Q[i,1])-Q0]])
        c = np.dot(a,b)/((I1-I0)**2+(Q1-Q0)**2)**0.5
        pro.append(c[0])
    pro = np.array(pro)
    return pro
def T1_fitting(xdata, ydata):
    popt, pcov = sco.curve_fit(expdecay, xdata, ydata)
    return popt