#nombre del archivo xml del clasificador, alojados en la carpeta data/haarcascades

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
import imutils
modelo = "fotos-entrenamiento" # nombre del modelo, carpeta donde se guardaran las fotos de entrenamiento


base_dir = os.path.dirname(__file__)
ruta = base_dir + "/data_photos/" + modelo # ruta para fotos

if not os.path.exists(ruta):
    os.makedirs(ruta)

cascade_path = os.path.join(base_dir, "data", "haarcascades", "haarcascade_frontalface_default.xml") # Cambiar solo el ultimo parametro para cambiar de clasificador

ruidos = cv.CascadeClassifier(cascade_path)

camara = cv.VideoCapture(0) # caracter numerico para camara, STR -> ruta de video

id = 0  

while True:
    respuesta,captura = camara.read()
    if respuesta == False:
        break
    captura = imutils.resize(captura, width=640) # Redimensionamos la imagen de la camara (bajando resolucion) para mejorar el rendimiento
    
    grises = cv.cvtColor(captura, cv.COLOR_BGR2GRAY)
    
    id_captura = captura.copy()
    
    cara= ruidos.detectMultiScale(grises, 1.4,5) # 1.4 es el factor de escala, mover tolerancia para mejorar deteccion, 5 es el numero de vecinos, entre mas alto mas seguro pero menos detecciones
    
     
    
    for(x,y,z1,z2) in cara:
        # x, y -> esquina superior izquierda
        # w -> ancho del rectángulo
        # h -> alto del rectángulo
        cv.rectangle(captura, (x,y),(x+z1, y+z2),(255,0,0),4)
        
        rostro_capturado = id_captura[y:y+z2, x:x+z1] # Recortamos la cara detectada
        
        rostro_capturado= cv.resize(rostro_capturado, (160,160), interpolation=cv.INTER_CUBIC) # Redimensionamos la imagen a un tamaño fijo
        
        cv.imwrite(ruta+ "/imagen_{}.jpg".format(id), rostro_capturado) # Guardamos la imagen recortada en la carpeta)
        id= id+1
        # Punto 1 -> (x, y) esquina superior izquierda
        # Punto 2 -> (x+z1, y+z2) esquina inferior derecha 
        # (sumando el ancho y alto)
    
    cv.imshow("Reconocimiento facial", captura)

    if id == 351:
        break
camara.release()
cv.destroyAllWindows()