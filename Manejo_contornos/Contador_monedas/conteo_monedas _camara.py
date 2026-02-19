import numpy as np
import cv2 as cv


# define la forma d elos circulos de las monedas


def ordenamiento_puntos(puntos):
    #unir matrices(matriz-> coleccion columnas y filas)
    n_puntos = np.concatenate(puntos[0], puntos[1], puntos [2], puntos [3]).tolist()
    
    key_y= lambda n_puntos:n_puntos[1] # ordena los puntos hasta la cordenada [ ]
    
    y_orden = sorted(n_puntos, key_y ) # ordenamiento nativo .sort de python
    
    x1_orden = y_orden[:2]
    key_x1= lambda x1_orden:x1_orden[0]
    x1_orden = sorted(x1_orden,key_x1)
    
    x2_orden = y_orden[2:4]
    key_x2= lambda x2_orden:x2_orden[0]
    x2_orden= sorted(x2_orden, key_x2) 
    
    
    return (x1_orden[0],x1_orden[1],x2_orden[0],x2_orden[1])


# funcion para la d efinir la horientacion de la camara
def alineamineto(imagen, ancho, alto):
    imagen_alineada = None
    
    grises = cv.cvtColor(imagen, cv.COLOR_BGR2GRAY)
    
    max_valor= 150,255
    tipo_de_umbral,umbral =cv.threshold(grises, max_valor,type)
    
    cv.imshow("umbral",umbral)
    
    mode= cv.RETR_EXTERNAL           #external para recibir las imagenes de la camara de forma externa
    method = cv.CHAIN_APPROX_SIMPLE  #modelado, metodo de aproximacion de contornos (aprox simple)
    contorno,jerarquia= cv.findContours(umbral,mode, method)[0]
    
    key= cv.contourArea
    reverse= True 
    contorno= sorted(contorno,key,reverse) [:1]
    
    for i in contorno:
        curva = i
        cerrado = True #cerrado de contorno
        epsilon = 0.01*cv.arcLength(curva ,cerrado) #reduccion de ruido en detenccion de contorno de curvas
        
        aproximacion = cv.approxPolyDP(curva, epsilon, cerrado)
        
        if len(aproximacion) == 4:
            puntos = ordenamiento_puntos(aproximacion)  
            
            punto_s1 = np.float32(puntos)
            
            #coordenadas
            punto_s2 = np.float32([0,0],[ancho,0], [0,alto],[ancho,alto]) #espacio de trabajo
            
            #metodo de perspectiva -> cuando la camara se mueva
            
            M = cv.getPerspectiveTransform(punto_s1,punto_s2) 
            imagen_alineada = cv.warpPerspective(imagen,M,(ancho,alto))
    
    return imagen_alineada


#=========================================================================================

captura_de_video = cv.VideoCapture(0)

while captura_de_video == True:
    tipo_camara,camara = captura_de_video.read()
    if tipo_camara == False:
        break
    imagen_A6 = alineamiento(camara,ancho_px,alto_px)    # Elige el formato de la imagen de trabajo (revisar tamano de formatos de papel y pasar a pixeles)
    if imagen_A6 is not None:
        puntos = []
        imagen_gris =cv.cvtColor(imagen_A6,cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(imagen_gris, (5,5),1)
        _  ,umbral_2= cv.threshold(blur, 0, 255, cv.THRESH_OTSU + cv.THRESH_BINARY_INV) #binarizacion inversa
        cv.imshow('umbral', umbral_2)
        
        contorno_2, jerarquia_2 = (umbral_2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        cv.drawContours(imagen_A6, contorno_2, -1, (225,0,0),2)
        
        # escalas monedas colombianas, 1 suma por cada tipo de moneda
        
        suma_50= 0.0
        suma_100= 0.0
        suma_200= 0.0
        suma_500= 0.0
        suma_1000 = 0.0
        
        for contorno in contorno_2 # contorno -> array
            areas = cv.contourArea(contorno)
            momentos = cv.moments(contorno) 
            if(momentos["m00"]== 0): # Hallar centroide segun la intensidad de pixeles
                momentos ["m00"]= 1.0 #valor necesario para momento estatico
            x= int(momentos["m10"]/momentos['m00']) #momento de desplazamiento
            y= int(momentos["m01"]/momentos['m00']) 
            #dar dato de area  por rando paea cada moneda
            
            if area<9300 and area>8000:
                font=cv.FONT_HERSHEY_SIMPLEX
                cv.putText(imagen_A6, "20 SOLES",(x,y) , font, 0.75, (0,255,0),2)
                suma1=suma1+0.
            
            if area<7800 and area>6500:
                font=cv.FONT_HERSHEY_SIMPLEX
                cv.putText(imagen_A6, "S/. 0.10",(x,y) , font, 0.75, (0,255,0),2)
                suma2=suma2+0.1
        total=suma1+suma2
        print("Sumatoria total en Centimos:",round(total,2))
        cv.imshow("Imagen A6", imagen_A6)
        cv.imshow("camara", camara)
    if cv.waitKey(1) == ord('s'):
        break
capturavideo.release()
cv2.destroyAllWindows()
                
    

#=======================================================================================