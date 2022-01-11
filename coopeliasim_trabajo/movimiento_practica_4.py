import sim
import sympy as sp
import csv
import time
import math
import cv2

L0 = 0.2039
L1 = 0.2912
L2 = 0.3236

q = [0,0]

def connect(port):
    sim.simxFinish(-1)
    clientID = sim.simxStart('127.0.0.1',port,True,True,2000,5)
    if clientID == 0: print("cliente conectado a :", port)
    else: print("No se pudo conectar")
    return clientID

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

def mov_efector(cord_x,cord_z):
    h = math.sqrt((cord_z-L0)**2+cord_x**2)
    fi = math.atan((cord_z-L0)/cord_x)
    b = math.acos(((h**2)-(L1**2)-(L2**2))/(-2*L1*L2))
    alfa = math.asin(L2*math.sin(b)/h)

    q[0] = fi+alfa-math.pi/2
    q[1] = b-math.pi/2

    f = open('prueba.csv','a')
    f.write("{},{}\n".format(q[0],q[1]))
    f.close()

    retCode1 = sim.simxSetJointTargetPosition(clientID,joint1,q[0],sim.simx_opmode_oneshot)
    retCode2 = sim.simxSetJointTargetPosition(clientID,joint2,q[1],sim.simx_opmode_oneshot)

def figura(doc,vel):
    f = open(doc,'r')
    mensaje = csv.reader(f)
    for linea in mensaje:
        retCode1 = sim.simxSetJointTargetPosition(clientID,joint1,float(linea[0]),sim.simx_opmode_oneshot)
        retCode2 = sim.simxSetJointTargetPosition(clientID,joint2,float(linea[1]),sim.simx_opmode_oneshot)
        time.sleep(vel)

clientID = connect(19999)
ret,dummy = sim.simxGetObjectHandle(clientID,'redundantRob_tip',sim.simx_opmode_blocking)
ret,joint1 = sim.simxGetObjectHandle(clientID,'redundantRob_joint2',sim.simx_opmode_blocking)
ret,joint2 = sim.simxGetObjectHandle(clientID,'redundantRob_joint4',sim.simx_opmode_blocking)

retCode1 = sim.simxSetJointTargetPosition(clientID,joint1,q[0],sim.simx_opmode_oneshot)
retCode2 = sim.simxSetJointTargetPosition(clientID,joint1,q[1],sim.simx_opmode_oneshot)


cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)#Empezamos a grabar el video donde posteriormente obtenedremos las fotos
llave = 0 #Nos permitira finalizar el programa
while llave == 0:
    ret, frame = cap.read() #se crea variable de pausa y de nombre de la ventana
    gris = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)# Convierte imagenes captadas en binarias
    frame_gris = cv2.Canny(gris,130,150)#-------------------------
    frame_gris = cv2.dilate(frame_gris,None,iterations=1)#       |--> se aplica difuminado y redondeado para mejorar persepción
    frame_gris = cv2.erode(frame_gris,None,iterations=1)#---------
    contornos,hierachy =cv2.findContours(frame_gris,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) # Se recolectan los contornos captados en la imagen
    
    for c in contornos:
        epsilon = 0.02*cv2.arcLength(c,True)#variable relacionada con el perimetro de la imagen o longitud de contorno 
        aproximar = cv2.approxPolyDP(c,epsilon,True)# se aproxima para obtener los vertices de las figuras
        x,y,w,h =cv2.boundingRect(aproximar)#Se obtienen cordenadas y calculo del alto y ancho promedio de la imagen
######################------------------Inicio de condicionales para detección de figuras-------------############################
        if len(aproximar)==3:
            cv2.putText(frame,'Triangulo',(x,y-5),1,1,(0,255,0),1)
            figura('triangulo.csv',0.1)
        if len(aproximar)==4:
            relacion_perimetro = float(w)/h ### esta relación de perimetro para el  es cuadrado = 1 +-20%, y para el rectangulo es 2 o 0.5 
            if relacion_perimetro < 1.2 and relacion_perimetro > 0.8:
                cv2.putText(frame,'Cuadrado',(x,y-5),1,1,(0,255,0),1)
                figura('cuadrado.csv',0.1)
            else:
                cv2.putText(frame,'Rectangulo',(x,y-5),1,1,(0,255,0),1)
                figura('rectangulo.csv',0.1)
        if len(aproximar)==5:
            cv2.putText(frame,'Pentagono',(x,y-5),1,1,(0,255,0),1)
        if len(aproximar)==6:
            cv2.putText(frame,'Hexagono',(x,y-5),1,1,(0,255,0),1)
        if len(aproximar)==10:
            cv2.putText(frame,'Estrella',(x,y-5),1,1,(0,255,0),1)
        if len(aproximar)==8:
            cv2.putText(frame,'Circulo',(x,y-5),1,1,(0,255,0),1)
            figura('circulo.csv',0.01)
        cv2.drawContours(frame,[aproximar],0,(0,255,0),2) #Dibujan los contornos de todas la figuras
        cv2.imshow('frame',frame)
        k = cv2.waitKey(1)
        if k == ord('s'):# condicional para finalizar el programa
            llave = 1
cv2.destroyAllWindows() #Destrucción de la ventana

for a in (30,55):
    mov_efector(a*0.01,0.1)
