import numpy as np
import cv2 as cv


def ordenamiento_puntos(puntos):
    #
    n_puntos = np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()

    # coordenadas de espacio de trabajo

    key_y = lambda n_puntos: n_puntos[1]
    y_orden = sorted(n_puntos, key=key_y)

    x1_orden = y_orden[:2]
    key_x1 = lambda x1_orden: x1_orden[0]
    x1_orden = sorted(x1_orden, key=key_x1)

    x2_orden = y_orden[2:4]
    key_x2 = lambda x2_orden: x2_orden[0]
    x2_orden = sorted(x2_orden, key=key_x2)

    return (x1_orden[0], x1_orden[1], x2_orden[0], x2_orden[1])


def alineamiento(imagen, ancho, alto): 
    imagen_alineada = None

    grises = cv.cvtColor(imagen, cv.COLOR_BGR2GRAY)

    
    tipo_de_umbral, umbral = cv.threshold(grises, 150, 255, cv.THRESH_BINARY)
    cv.imshow("umbral", umbral)

    # ✅ ERROR 3 CORREGIDO: sin [0] al final para poder tomar solo contornos
    contorno = cv.findContours(umbral, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

    # ✅ ERROR 4 CORREGIDO: keywords explícitos en sorted()
    contorno = sorted(contorno, key=cv.contourArea, reverse=True)[:1]

    for i in contorno:
        curva = i
        cerrado = True
        epsilon = 0.01 * cv.arcLength(curva, cerrado)
        aproximacion = cv.approxPolyDP(curva, epsilon, cerrado)

        if len(aproximacion) == 4:
            puntos = ordenamiento_puntos(aproximacion)
            punto_s1 = np.float32(puntos)

            # ✅ ERROR 5 CORREGIDO: lista de listas en np.float32
            punto_s2 = np.float32([[0, 0], [ancho, 0], [0, alto], [ancho, alto]])

            M = cv.getPerspectiveTransform(punto_s1, punto_s2)
            imagen_alineada = cv.warpPerspective(imagen, M, (ancho, alto))

    return imagen_alineada


# Función de ayuda para calibrar áreas (actívala al inicio)
def imprimir_areas(contornos):
    for c in contornos:
        area = cv.contourArea(c)
        if area > 300:
            print(f"  Área detectada: {area:.0f} px²")


# ============================================================
# Diámetros reales de monedas colombianas (referencia):
#   $50   → 17.0 mm  (más pequeña)
#   $100  → 20.3 mm
#   $200  → 22.4 mm
#   $500  → 23.7 mm
#   $1000 → 26.7 mm  (más grande)
#
# ⚠ Los rangos de área en píxeles dependen de tu cámara y
#   distancia. Descomenta imprimir_areas() para calibrarlos.
# ============================================================

captura_de_video = cv.VideoCapture(0)

# ✅ ERROR 6 CORREGIDO: while True en lugar de comparar el objeto
while True:
    tipo_camara, camara = captura_de_video.read()
    if tipo_camara == False:
        break

    # ✅ ERROR 7 CORREGIDO: nombre correcto y dimensiones definidas
    cv.imshow("camara", camara)
    
    imagen_A6 = alineamiento(camara, ancho=480, alto=640)
    

    if imagen_A6 is not None:
        imagen_gris = cv.cvtColor(imagen_A6, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(imagen_gris, (5, 5), 1)
        _, umbral_2 = cv.threshold(blur, 0, 255, cv.THRESH_OTSU + cv.THRESH_BINARY_INV)
        cv.imshow('umbral', umbral_2)

        # ✅ ERROR 8 CORREGIDO: findContours() llamado correctamente
        contorno_2 = cv.findContours(umbral_2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
        cv.drawContours(imagen_A6, contorno_2, -1, (225, 0, 0), 2)

        # Descomenta para calibrar rangos según tu cámara:
        # imprimir_areas(contorno_2)

        suma_50   = 0.0
        suma_100  = 0.0
        suma_200  = 0.0
        suma_500  = 0.0
        suma_1000 = 0.0

        # ✅ ERROR 9 CORREGIDO: dos puntos al final del for
        for contorno in contorno_2:
            # ✅ ERROR 10 CORREGIDO: variable llamada "area" de forma consistente
            area = cv.contourArea(contorno)
            momentos = cv.moments(contorno)

            if momentos["m00"] == 0:
                momentos["m00"] = 1.0

            x = int(momentos["m10"] / momentos["m00"])
            y = int(momentos["m01"] / momentos["m00"])

            font = cv.FONT_HERSHEY_SIMPLEX

            # ✅ ERROR 11 CORREGIDO: variables correctas y valores completos
            # ⚠ Ajusta los rangos con imprimir_areas() según tu setup

            if 2500 < area < 4000:        # $50  → la más pequeña
                cv.putText(imagen_A6, "$ 50", (x, y), font, 0.7, (255, 200, 0), 2)
                suma_50 += 50

            elif 4000 < area < 6000:      # $100
                cv.putText(imagen_A6, "$ 100", (x, y), font, 0.7, (0, 255, 0), 2)
                suma_100 += 100

            elif 6000 < area < 7800:      # $200
                cv.putText(imagen_A6, "$ 200", (x, y), font, 0.7, (0, 200, 255), 2)
                suma_200 += 200

            elif 7800 < area < 9300:      # $500
                cv.putText(imagen_A6, "$ 500", (x, y), font, 0.7, (255, 0, 200), 2)
                suma_500 += 500

            elif 9300 < area < 12000:     # $1000 → la más grande
                cv.putText(imagen_A6, "$ 1000", (x, y), font, 0.7, (0, 0, 255), 2)
                suma_1000 += 1000

        total = suma_50 + suma_100 + suma_200 + suma_500 + suma_1000

        # Mostrar total sobre la imagen
        cv.putText(imagen_A6, f"TOTAL: $ {int(total)} COP",
                   (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        print(f"$50: {int(suma_50)} | $100: {int(suma_100)} | $200: {int(suma_200)} "
              f"| $500: {int(suma_500)} | $1000: {int(suma_1000)} "
              f"| TOTAL: ${int(total)} COP")

        cv.imshow("Imagen A6", imagen_A6)

    if cv.waitKey(1) == ord('q'):
        break

# ✅ ERROR 12 CORREGIDO: nombres correctos de variable y módulo
captura_de_video.release()
cv.destroyAllWindows()