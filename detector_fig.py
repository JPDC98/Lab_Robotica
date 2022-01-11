import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)#Empezamos a grabar el video donde posteriormente obtenedremos las fotos
llave = 0 #Nos permitira finalizar el programa
while llave == 0:
    ret, frame = cap.read() #se crea variable de pausa y de nombre de la ventana
    gris = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)# Convierte imagenes captadas en binarias
    fgaussiano = cv2.GaussianBlur(gris,(5,5),0)
    frame_gris = cv2.Canny(fgaussiano,130,150)#-------------------------
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
        if len(aproximar)==4:
            relacion_perimetro = float(w)/h ### esta relación de perimetro para el  es cuadrado = 1 +-20%, y para el rectangulo es 2 o 0.5 
            if relacion_perimetro < 1.2 and relacion_perimetro > 0.8:
                cv2.putText(frame,'Cuadrado',(x,y-5),1,1,(0,255,0),1)
            else:
                cv2.putText(frame,'Rectangulo',(x,y-5),1,1,(0,255,0),1)
        if len(aproximar)==5:
            cv2.putText(frame,'Pentagono',(x,y-5),1,1,(0,255,0),1)
        if len(aproximar)==6:
            cv2.putText(frame,'Hexagono',(x,y-5),1,1,(0,255,0),1)
        if len(aproximar)==10:
            cv2.putText(frame,'Estrella',(x,y-5),1,1,(0,255,0),1)
        if len(aproximar)==8:
            cv2.putText(frame,'Circulo',(x,y-5),1,1,(0,255,0),1)
        cv2.drawContours(frame,[aproximar],0,(0,255,0),2) #Dibujan los contornos de todas la figuras
        cv2.imshow('frame',frame)
        k = cv2.waitKey(0)
        if k == ord('s'):# condicional para finalizar el programa
            llave = 1
cap.release()
cv2.destroyAllWindows() #Destrucción de la ventana