import sympy as sp

L0 = 0.2039
L1 = 0.2912
L2 = 0.3236

x = 0.5189
y = 0
z = 0.3260

def matriz_tranformada_DH(theta,d,a,alfa):
    R_z = sp.Matrix([[sp.cos(theta),-sp.sin(theta),0,0],
                   [sp.sin(theta),   sp.cos(theta),0,0],
                   [0,0,1,0],
                   [0,0,0,1]])

    R_x = sp.Matrix([[1,0,0,0],
                   [0,sp.cos(alfa),-sp.sin(alfa),0],
                   [0,sp.sin(alfa), sp.cos(alfa),0],
                   [0,0,0,1]])

    T_x = sp.Matrix([[1,0,0,a],
           [0,1,0,0],
           [0,0,1,0],
           [0,0,0,1]])

    T_z = sp.Matrix([[1,0,0,0],
           [0,1,0,0],
           [0,0,1,d],
           [0,0,0,1]])

    T = R_z*T_z*T_x*R_x

    return T 

q1 = sp.symbols('q1')
q3 = sp.symbols('q3')
T1 = matriz_tranformada_DH(0,L0,0,0)
T2 = matriz_tranformada_DH(0,0,0,90)
T3 = matriz_tranformada_DH(90,0,0,0)
T4 = matriz_tranformada_DH(q1,0,0,0)
T5 = matriz_tranformada_DH(0,0,L1,0)
T6 = matriz_tranformada_DH(-90,0,0,0)
T7 = matriz_tranformada_DH(q3,0,0,0)
T8 = matriz_tranformada_DH(0,0,L2,0)

T_total = T1*T2*T3*T4*T5*T6*T7*T8
T_eq = sp.simplify(T_total)

eq1 = T_eq[0,3]-x 
eq3 = T_eq[2,3]-z

solucion = sp.nsolve((eq1,eq3),(q1,q3),(1,1))

print(solucion)





