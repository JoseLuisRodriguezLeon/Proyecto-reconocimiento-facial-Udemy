import cv2 as cv
import os

base_dir = os.path.dirname(__file__)
cascade_path = os.path.join(base_dir, "data", "haarcascades", "haarcascade_frontalface_default.xml") # Cambiar solo el ultimo parametro para cambiar de clasificador

ruidos = cv.CascadeClassifier(cascade_path)

camara = cv.VideoCapture(0)

while True:
    _,captura = camara.read()
    grises = cv.cvtColor(captura, cv.COLOR_BGR2GRAY)
    cara= ruidos.detectMultiScale(grises, 1.4,5) # 1.4 es el factor de escala, mover tolerancia para mejorar deteccion, 5 es el numero de vecinos, entre mas alto mas seguro pero menos detecciones
    for(x,y,z1,z2) in cara:
        # x, y -> esquina superior izquierda
        # w -> ancho del rectángulo
        # h -> alto del rectángulo
        cv.rectangle(captura, (x,y),(x+z1, y+z2),(255,0,0),4)
        
        # Punto 1 -> (x, y) esquina superior izquierda
        # Punto 2 -> (x+z1, y+z2) esquina inferior derecha 
        # (sumando el ancho y alto)
    
    cv.imshow("Reconocimiento facial", captura)
    if cv.waitKey(1) == ord("q"):
        break
camara.release()
cv.destroyAllWindows()