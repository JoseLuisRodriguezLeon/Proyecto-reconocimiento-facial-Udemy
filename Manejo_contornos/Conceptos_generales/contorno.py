import cv2 as cv
import os

# ==================== CARGAR IMAGEN ====================
# Obtener el directorio donde está el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# dirname(): Obtiene el directorio de una ruta dada
# abspath(): Convierte rutas relativas en absolutas

# Crear la ruta completa a la imagen
ruta_imagen = os.path.join(script_dir, "Data", "contorno.jpg")

# join(): Combina partes de rutas de forma segura (maneja separadores)

# Cargar la imagen
imagen = cv.imread(ruta_imagen)

# Verificar si se cargó correctamente
if imagen is None:
    print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")
    exit()



else:

    # ==================== PROCESAMIENTO ====================
    
    # Convertir a escala de grises
    
    # cvtColor convierte colores. BGR2GRAY elimina el color dejando solo intensidades
    escala_grises = cv.cvtColor(imagen, cv.COLOR_BGR2GRAY)
    
    # Umbralización (binarización)
    
    # threshold separa la imagen en blanco y negro según un valor límite
    
    # Parámetros:
    #   - escala_grises: imagen de entrada
    #   - 100: valor umbral (si pixel > 100 → blanco, si pixel ≤ 100 → negro)
    #   - 255: valor máximo (blanco puro)
    #   - THRESH_BINARY: tipo de umbral (binario simple)
    # Cambiar 100 por valores mayores deja menos blanco, valores menores más blanco
    contorno1, umbral = cv.threshold(escala_grises, 100, 255, cv.THRESH_BINARY)
    
    # Encontrar contornos
    
    # findContours detecta bordes de objetos blancos sobre fondo negro
    
    # Parámetros:
    #   - umbral: imagen binarizada
    #   - RETR_LIST: modo de recuperación (lista simple de todos los contornos)
    #   - CHAIN_APPROX_SIMPLE: comprime contornos (guarda solo puntos esenciales)
    # Retorna lista de contornos y su jerarquía
    contornos, jerarquia = cv.findContours(umbral, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    
    # Dibujar contornos en la imagen original
    
    # drawContours traza los contornos encontrados
    
    # Parámetros:
    #   - imagen: donde dibujar
    #   - contornos: lista de contornos a dibujar
    #   - -1: índice de contorno (-1 = todos, 0 = primero, 1 = segundo, etc.)
    #   - (128, 0, 255): color en formato BGR (magenta)
    #   - 3: grosor en píxeles (1-10 recomendado, -1 rellena)
    cv.drawContours(imagen, contornos, -1, (128, 0, 255), 3)
    
    # ==================== MOSTRAR RESULTADOS ====================
    cv.imshow('Imagen con contornos', imagen)
    cv.imshow('Escala de grises', escala_grises)
    cv.imshow('Imagen binaria', umbral)
    
    # Esperar a que se presione una tecla para cerrar las ventanas
    cv.waitKey(0)
    cv.destroyAllWindows()