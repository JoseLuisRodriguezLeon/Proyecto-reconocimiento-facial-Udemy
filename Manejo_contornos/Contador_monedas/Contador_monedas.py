import cv2 as cv2
import os
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio del script actual
ruta_imagen = os.path.join(script_dir, "Data", "monedas_soles.jpg")  # Ruta completa de la imagen


valorGauss = 5   # Tamaño del kernel gaussiano (debe ser impar, si es par se pierde el pixel central de referencia y el filtro no se aplica correctamente)
valorKernel = 7  # Tamaño del kernel morfológico (debe ser impar para mantener simetría)

original = cv2.imread(ruta_imagen)  # Para dibujar resultados finales
imagen = cv2.imread(ruta_imagen)    # Copia sin modificar para comparación

# ============================================================================
# PREPROCESAMIENTO

# Convertir a escala de grises
gris = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

# Aplicar filtro gaussiano para reducir ruido

# cv2.GaussianBlur(src, ksize, sigmaX, sigmaY=0)
#   src: Imagen de entrada
#   ksize: Tamaño del kernel (ancho, alto) - debe ser impar
#   sigmaX: Desviación estándar en X (0 = auto-cálculo)
#   sigmaY: Desviación estándar en Y (0 = usa sigmaX)
#   Retorna: Imagen suavizada
gauss = cv2.GaussianBlur(gris, (valorGauss, valorGauss), 0, 0)

# ============================================================================
# DETECCIÓN DE BORDES

# Detector de bordes Canny

# cv2.Canny(image, threshold1, threshold2, apertureSize=3, L2gradient=False)
#   image: Imagen de entrada en escala de grises
#   threshold1: Umbral inferior para histéresis (60)
#   threshold2: Umbral superior para histéresis (100)
#   apertureSize: Tamaño apertura Sobel (default: 3)
#   L2gradient: Usar norma L2 para gradiente (default: False)
#   Retorna: Imagen binaria con bordes detectados
canny = cv2.Canny(gauss, 60, 100,3)

# ============================================================================
# OPERACIONES MORFOLÓGICAS

# Crear kernel (elemento estructurante)

# np.ones((shape), dtype)
#   shape: Dimensiones de la matriz (filas, columnas)
#   dtype: Tipo de datos (np.uint8 = enteros 0-255)
#   Retorna: Matriz llena de unos
kernel = np.ones((valorKernel, valorKernel), np.uint8)

# Cierre morfológico (dilatación + erosión)

# cv2.morphologyEx(src, op, kernel, iterations=1)
#   src: Imagen de entrada
#   op: Tipo de operación (MORPH_CLOSE = dilatación seguida de erosión)
#   kernel: Elemento estructurante
#   iterations: Número de repeticiones (default: 1)
#   Retorna: Imagen procesada (cierra huecos en contornos)
cierre = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)

# ============================================================================
# DETECCIÓN DE CONTORNOS

#  Encontrar contornos

# cv2.findContours(image, mode, method)
#   image: Imagen binaria de entrada (.copy() para no modificar original)
#   mode: Modo de recuperación (RETR_EXTERNAL = solo contornos externos, retr_internal. osea, retr_list = solo contornos internos todos sin jerarquía)
#   method: Método de aproximación (CHAIN_APPROX_SIMPLE = comprime segmentos)
#   Retorna: (contornos, jerarquía)
#     contornos: Lista de arrays con puntos de cada contorno
#     jerarquía: Relaciones jerárquicas entre contornos
contornos, jerarquía = cv2.findContours(cierre.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print("monedas encontradas: {}".format(len(contornos)))

# ============================================================================
# VISUALIZACIÓN DE RESULTADOS

# Dibujar contornos sobre la imagen original

cv2.drawContours(original, contornos, -1, (0, 0, 255), 3)

# Mostrar imágenes en ventanas
cv2.imshow("Original", imagen)   # Imagen sin procesar
cv2.imshow("Grises", gris)       # Conversión a escala de grises
cv2.imshow("Gauss", gauss)       # Después del filtro gaussiano
cv2.imshow("Canny", canny)       # Detección de bordes
cv2.imshow("Cierre", cierre)     # Operación morfológica de cierre
cv2.imshow("Resultado", original)# Imagen con contornos dibujados


cv2.waitKey(0)
cv2.destroyAllWindows()