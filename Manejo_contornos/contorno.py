import cv2 as c
import os

# Obtener el directorio donde está el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Crear la ruta completa a la imagen
ruta_imagen = os.path.join(script_dir, 'contorno.jpg')

# Cargar la imagen
imagen = c.imread(ruta_imagen)

# Verificar si se cargó correctamente
if imagen is None:
    print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")
    print(f"Archivos en el directorio: {os.listdir(script_dir)}")
else:
    #escala de grises
    escala_grises= c.cvtColor(imagen, c.COLOR_BGR2GRAY)
    # umbralizacion
    # 100 y 255 afecta valor de umbral, el tipo de umbral afecta el resultado, en este caso se usa umbral binario hasta 255
    # Si el valor del pixel es mayor a 100 se vuelve blanco (255)
    Contorno1,umbral= c.threshold(escala_grises,100,255,c.THRESH_BINARY)
    
    Contorno2, jerarquia = c.findContours(umbral, c.RETR_LIST, c.CHAIN_APPROX_SIMPLE)
    
    c.drawContours(imagen, Contorno2, 1, (251,60,50), 3) # dibujar contornos en la imagen original, -1 para dibujar todos los contornos, color verde y grosor de 3
    
    # Mostrar la imagen
    c.imshow('IMAGEN ORIGINAL, aqui edito el nombre de la ventana', imagen)
    c.imshow('escala_grises', escala_grises)
    c.imshow('binaria', umbral)
    
    
    
    # waitKey y destroyAllWindows -> para cerrar las ventanas al presionar una tecla
    c.waitKey(0)
    c.destroyAllWindows()