import cv2 as cv 
import os
import numpy as np
import time

base_dir = os.path.dirname(__file__)
ruta = base_dir + "/data_photos/"  # ruta para fotos

listaData = os.listdir(ruta)
# print("data", lista) -> para ver si se tiene acceso a la carpeta de fotos dentro del script

labels = []

rostros = []

id = 0

tiempo_i = time.time()

for fila in listaData:
    ruta_completa = ruta + "/" + fila #accedemos a cada foto dentro de la carpeta
    for archivo in os.listdir(ruta_completa):
        print("Imagenes en entrenamiento: ", fila + "/" + archivo)
        labels.append(id) #agregamos el id a la lista de labels
       
        imagen = cv.imread(ruta_completa + "/" + archivo, 0) #leemos cada foto
        rostros.append(imagen) #agregamos la imagen a la lista de rostros, cada imagen es un array de pixeles en escala de grises (0-255)
        
        
    id = id + 1 #incrementamos el id para la siguiente persona
    tiempo_f = time.time()
    tiempo_total= tiempo_f - tiempo_i
    print("\nTiempo de lectura: ", tiempo_f - tiempo_i, "segundos")   

entrenamieno_modelo = cv.face.EigenFaceRecognizer_create() #creamos el modelo de reconocimiento facial utilizando el algoritmo EigenFaces

print("Entrenamiento iniciado. . . Por favor espere. . .")
entrenamieno_modelo.train(rostros, np.array(labels)) #entrenamos

tiempo_final = time.time()
print("Tiempo de entrenamiento: ", tiempo_final - tiempo_total, "segundos")

entrenamieno_modelo.write(os.path.join(base_dir, "Entrenamiento EigenFaces.xml")) #guardamos el modelo entrenado en un archivo XML
print("Entrenamiento finalizado. . . ")


    