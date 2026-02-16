import cv2 as cv

# ============================================================================
# CAPTURA DE VIDEO DESDE CÁMARA

# cv.VideoCapture(index)

#   index: 0 = cámara por defecto, 1,2,3... = otras cámaras
#   Retorna: objeto VideoCapture

#si la camara esta en uso por otro programa produce un error ([ WARN:0@8.946] global cap_msmf.cpp:477 `anonymous-namespace'::SourceReaderCB::OnReadSample videoio(MSMF): OnReadSample() is called with error status: -1072875772)
video = cv.VideoCapture(0)

# Verificar si la cámara se abrió correctamente
if not video.isOpened():
    print("Error: No se pudo abrir la cámara")
    exit()
    
# ==================================================================================================

while True:
    # video.read() retorna (ret, frame)
    
    #   ret: booleano - True si se leyó correctamente, False si falló
    #   frame: numpy.ndarray - imagen capturada
    condicion, captura = video.read()

    grises = cv.cvtColor(captura, cv.COLOR_BGR2GRAY)
    
    
    gauss = cv.GaussianBlur(grises, (5, 5), 0, 0)
    
    canny = cv.Canny(gauss, 60, 100,3)  
    
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
    
    cierre = cv.morphologyEx(canny, cv.MORPH_CLOSE, kernel)  
    
    contornos, jerarquía = cv.findContours(cierre.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    resultado = cv.drawContours(captura.copy(), contornos, -1, (0, 255, 0), 2)

    # Verificar si el frame se capturó correctamente
    if not condicion:
        print("Error: No se pudo leer el frame de la cámara")
        break
    
    
# ========================================================================
    # cv.imshow(winname, mat)
    
    #   winname: nombre de la ventana
    #   mat: imagen a mostrar
    cv.imshow('Camara', captura)
    
    # cv.imshow('Grises', grises)
    
    # cv.imshow('Gauss', gauss)
    
    # cv.imshow('Canny', canny) # Detección de bordes
    
    # cv.imshow('Cierre', cierre) # Operación morfológica de cierre
    
    # cv.imshow('Contornos', resultado) # Imagen con contornos dibujados
    
    
# ========================================================================
    # cv.waitKey(delay)
    
    #   delay: tiempo de espera en ms (1 ms para video fluido)
    #   Retorna: código de la tecla presionada (-1 si no se presionó nada)
    # ord('q'): convierte el carácter 'q' a su código ASCII
    if cv.waitKey(1) == ord('q'):
        print("Saliendo...")
        break

# Liberar recursos
video.release()           # Libera la cámara
cv.destroyAllWindows()    # Cierra todas las ventanas

