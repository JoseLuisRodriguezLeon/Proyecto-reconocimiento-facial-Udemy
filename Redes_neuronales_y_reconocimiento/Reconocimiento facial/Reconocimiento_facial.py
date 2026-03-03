#nombre del archivo xml del clasificador

# haarcascade_eye.xml - Detecta ojos abiertos en rostros frontales
# haarcascade_eye_tree_eyeglasses.xml - Detecta ojos incluso con gafas
# haarcascade_lefteye_2splits.xml - Detecta ojo izquierdo específicamente
# haarcascade_righteye_2splits.xml - Detecta ojo derecho específicamente
# haarcascade_frontalface_default.xml - Detecta rostros frontales, uso recomendado
# haarcascade_frontalface_alt.xml - Variante alternativa para rostro frontal
# haarcascade_frontalface_alt2.xml - Otra variante rostro frontal
# haarcascade_frontalface_alt_tree.xml - Variante árbol, más pesada
# haarcascade_frontalface_extended.xml - Rostro frontal con mayor cobertura
# haarcascade_profileface.xml - Detecta rostros de perfil
# haarcascade_smile.xml - Detecta sonrisas, requiere rostro previo
# haarcascade_fullbody.xml - Detecta cuerpo completo de persona
# haarcascade_upperbody.xml - Detecta parte superior del cuerpo
# haarcascade_lowerbody.xml - Detecta parte inferior del cuerpo
# haarcascade_russian_plate_number.xml - Detecta placas rusas principalmente
# haarcascade_license_plate_rus_16stages.xml - Placas rusas, cascada 16 etapas

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