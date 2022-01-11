import numpy as np



L0 = 0.2039
L1 = 0.2912
L2 = 0.3236


q1 = -45
q2 = 0
q3 = 20

Entidad = np.array([[1,0,0,0],
           [0,1,0,0],
           [0,0,1,0],
           [0,0,0,1]],float)

def matriz_tranformada_DH(theta,d,a,alfa):
       R_z = np.array([[np.cos(np.radians(theta)),-1*np.sin(np.radians(theta)),0,0],
                   [np.sin(np.radians(theta)),   np.cos(np.radians(theta)),0,0],
                   [0,0,1,0],
                   [0,0,0,1]],float)

       R_x = np.array([[1,0,0,0],
                   [0,np.cos(np.radians(alfa)),-1*np.sin(np.radians(alfa)),0],
                   [0,np.sin(np.radians(alfa)),   np.cos(np.radians(alfa)),0],
                   [0,0,0,1]],float)

       T_x = np.array([[1,0,0,a],
           [0,1,0,0],
           [0,0,1,0],
           [0,0,0,1]],float)

       T_z = np.array([[1,0,0,0],
           [0,1,0,0],
           [0,0,1,d],
           [0,0,0,1]],float)
       
       T = Multi_mat(R_z,T_z,T_x,R_x,Entidad,Entidad,Entidad,Entidad,Entidad)

       return  T

def Multi_mat(a,b,c,d,e,f,g,h,i):
       re_1 = np.dot(a,b)
       re_2 = np.dot(re_1,c)
       re_3 = np.dot(re_2,d)
       re_4 = np.dot(re_3,e)
       re_5 = np.dot(re_4,f)
       re_6 = np.dot(re_5,g)
       re_7 = np.dot(re_6,h)
       re_8 = np.dot(re_7,i)
       return re_8

T1 = matriz_tranformada_DH(0,L0,0,0)
T2 = matriz_tranformada_DH(0,0,0,90)
T3 = matriz_tranformada_DH(90,0,0,0)
T4 = matriz_tranformada_DH(q1,0,0,0)
T5 = matriz_tranformada_DH(0,0,L1,0)
T6 = matriz_tranformada_DH(-90,0,0,0)
T7 = matriz_tranformada_DH(q3,0,0,0)
T8 = matriz_tranformada_DH(0,0,L2,0)
T9 = matriz_tranformada_DH(0,0,0,-90)
T_total = Multi_mat(T1,T2,T3,T4,T5,T6,T7,T8,T9)      

print(T_total)