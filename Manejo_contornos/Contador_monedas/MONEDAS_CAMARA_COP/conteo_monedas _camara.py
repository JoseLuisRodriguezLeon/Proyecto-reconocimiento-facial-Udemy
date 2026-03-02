# =============================================================================
# DETECTOR DE MONEDAS COLOMBIANAS CON OPENCV
# =============================================================================
# Este programa usa la cámara web para detectar monedas colombianas en tiempo
# real, clasificarlas por su valor y sumar el total visible en pantalla. 
# Adaptacion del codigo hecha por Jose L. dentro del curso de OpenCV en Python de Udemy.
# Adaptado a monedas colombianas por Jose L. (basado en dimensiones de monedas peruanas)
#
# SE NECESITA MONEDAS LIMPIAS Y UNA EXELENTE ILUMINACION PARA QUE FUNCIONE BIEN
#
# Librerías necesarias:
#   - numpy  → manejo de matrices y operaciones matemáticas
#   - cv2    → OpenCV, librería principal de visión por computadora
# =============================================================================

import numpy as np   # numpy es la base matemática de OpenCV; maneja imágenes como matrices de números
import cv2 as cv     # OpenCV: permite capturar video, procesar imágenes y detectar formas


# =============================================================================
# SECCIÓN 1 — MODO DE OPERACIÓN
# =============================================================================
# El programa tiene dos modos que se controlan con esta variable:
#
#   CALIBRAR = True  → Modo calibración:
#                      Muestra encima de cada moneda detectada sus valores reales
#                      de radio (r), ratio (rt), Hue (H), Saturación (S) y Value (V).
#                      Úsalo para conocer los valores reales de TUS monedas con
#                      TU cámara y TU iluminación, ya que estos varían.
#
#   CALIBRAR = False → Modo detección normal:
#                      Clasifica cada moneda y muestra su valor en pesos.
#                      Usa este modo una vez hayas calibrado los rangos.

CALIBRAR = False


# =============================================================================
# SECCIÓN 2 — TABLA DE MONEDAS (RANGOS DE CLASIFICACIÓN)
# =============================================================================
# Cada moneda se define con los siguientes parámetros:
#
#   "nombre"    → texto que aparece en pantalla sobre la moneda
#   "valor"     → valor numérico en pesos para sumar al total
#   "color"     → color del círculo dibujado sobre la moneda en formato BGR
#                 (BGR = Azul, Verde, Rojo — OpenCV usa este orden, no RGB)
#
#   "radio_min" → radio mínimo aceptado en píxeles
#   "radio_max" → radio máximo aceptado en píxeles
#                 Estos valores dependen de la distancia de tu cámara.
#                 Si te acercas, el radio sube. Si te alejas, baja.
#                 (Calibrar tamaño de monedas con una de dimensiones distinguibles)
#
#   "rt_min"    → ratio mínimo (radio de esta moneda / radio de la más pequeña visible)
#   "rt_max"    → ratio máximo
#                 El ratio es relativo, por eso es más estable que el radio absoluto.
#                 Ejemplo: si la moneda más pequeña tiene radio 52px y esta tiene 61px,
#                 su ratio es 61/52 = 1.17, independientemente de qué tan lejos esté la cámara.
#
#   "hue_min"   → tono de color mínimo en el espacio HSV (rango 0-179 en OpenCV)
#   "hue_max"   → tono de color máximo
#                 El Hue representa el color puro: 0=rojo, 30=amarillo/dorado, 60=verde, etc.
#
#   "sat_min"   → saturación mínima (qué tan "intenso" o "puro" es el color)
#   "sat_max"   → saturación máxima (rango 0-255, donde 0=gris y 255=color puro)
#                   LA SATURACIÓN ES EL DIFERENCIADOR MÁS IMPORTANTE entre $200 y $500:
#                    $200 → moneda gris/oscura → S baja (~20-60)
#                    $500 → moneda dorada brillante → S alta (~95-160)
# =============================================================================
RATIOS_MONEDAS = [
    {
        "nombre"   : "$ 100",
        "valor"    : 100,
        "color"    : (0, 255, 0),      # verde en BGR
        "radio_min": 45, "radio_max": 58,
        "rt_min"   : 0.90, "rt_max": 1.15,
        "hue_min"  : 18, "hue_max": 32,
        "sat_min"  : 70, "sat_max": 115,
    },
    {
        "nombre"   : "$ 200",
        "valor"    : 200,
        "color"    : (0, 200, 255),    # amarillo en BGR
        "radio_min": 55, "radio_max": 68,
        "rt_min"   : 1.10, "rt_max": 1.25,
        "hue_min"  : 18, "hue_max": 35,
        "sat_min"  : 20, "sat_max": 60,    # ← S baja: moneda gris oscura
    },
    {
        "nombre"   : "$ 500",
        "valor"    : 500,
        "color"    : (255, 0, 200),    # magenta en BGR
        "radio_min": 48, "radio_max": 65,
        "rt_min"   : 1.00, "rt_max": 1.28,
        "hue_min"  : 18, "hue_max": 32,
        "sat_min"  : 95, "sat_max": 160,   # ← S alta: moneda dorada brillante
    },
    {
        "nombre"   : "$ 1000",
        "valor"    : 1000,
        "color"    : (0, 0, 255),      # rojo en BGR
        "radio_min": 62, "radio_max": 80,
        "rt_min"   : 1.25, "rt_max": 1.50,
        "hue_min"  : 18, "hue_max": 32,
        "sat_min"  : 45, "sat_max": 80,
    },
]


# =============================================================================
# SECCIÓN 3 — PARÁMETROS DE DETECCIÓN (HoughCircles)
# =============================================================================
# HoughCircles es el algoritmo principal de detección. Busca círculos en la
# imagen usando la Transformada de Hough, que acumula "votos" para cada posible
# centro y radio de círculo.
#
#   RADIO_MIN / RADIO_MAX   → limita la búsqueda a monedas de tamaño razonable.
#                             Si buscas en todo el rango, detectará ruido.
#
#   DISTANCIA_MIN           → distancia mínima entre los centros de dos monedas
#                             detectadas. Evita que detecte la misma moneda dos veces.
#
#   PARAM1                  → umbral superior del detector de bordes Canny interno.
#                             Valores altos = solo bordes muy marcados.
#                             Si no detecta monedas → bajarlo.
#
#   PARAM2                  → umbral del acumulador de Hough.
#                             Más bajo = detecta más círculos (incluyendo falsos).
#                             Más alto = solo círculos muy bien definidos.
#                             Si detecta círculos donde no hay monedas → subirlo.
#                             Si no detecta monedas reales → bajarlo.
#
#   SAT_MINIMA / VAL_MINIMA → filtros adicionales para descartar detecciones
#                             sobre papel blanco (S0) o zonas muy oscuras (V0).

RADIO_MIN     = 40    # radio mínimo de moneda a buscar (px)
RADIO_MAX     = 85    # radio máximo de moneda a buscar (px)
DISTANCIA_MIN = 50    # distancia mínima entre centros de dos círculos (px)
PARAM1        = 50    # sensibilidad al borde interno de Hough
PARAM2        = 45    # sensibilidad del acumulador (sube si hay falsas detecciones)
SAT_MINIMA    = 20    # saturación mínima para considerar que hay una moneda real
VAL_MINIMA    = 40    # brillo mínimo para descartar zonas completamente oscuras


# =============================================================================
# SECCIÓN 4 — FUNCIONES AUXILIARES
# =============================================================================

def extraer_color_hsv(frame_hsv, cx, cy, radio):
    """
    Extrae el color promedio del INTERIOR de una moneda detectada.

    Por qué se usa el 70% interior:
        El borde de todas las monedas tiende a ser similar (metal brillante).
        El interior es donde está el color característico de cada denominación.
        Excluir el borde reduce el ruido en la clasificación por color.

    Proceso:
        1. Calcula el radio interior como el 70% del radio total.
        2. Crea una imagen negra del mismo tamaño que el frame (máscara).
        3. Dibuja un círculo BLANCO relleno en la posición de la moneda.
        4. Extrae solo los píxeles que están dentro del círculo blanco.
        5. Calcula el promedio de H, S y V de esos píxeles.

    Parámetros:
        frame_hsv → imagen completa convertida al espacio de color HSV
        cx, cy    → coordenadas del centro de la moneda en píxeles
        radio     → radio de la moneda en píxeles

    Retorna:
        hue_promedio → tono de color promedio (0-179)
        sat_promedio → saturación promedio (0-255)
        val_promedio → brillo promedio (0-255)
    """
    radio_interior = int(radio * 0.7)  # solo el 70% central

    # Crear una imagen completamente negra del mismo tamaño que el frame
    # dtype=np.uint8 → valores entre 0 y 255, igual que una imagen normal
    mascara = np.zeros(frame_hsv.shape[:2], dtype=np.uint8)

    # Dibujar círculo blanco (255) relleno (-1 = relleno completo) en la máscara
    # Solo los píxeles dentro del círculo quedan en blanco
    cv.circle(mascara, (cx, cy), radio_interior, 255, -1)

    # Extraer solo los píxeles de frame_hsv donde la máscara es blanca (255)
    # Resultado: array de píxeles [H, S, V] del interior de la moneda
    pixeles = frame_hsv[mascara == 255]

    # Si por algún error no hay píxeles, retornar ceros
    if len(pixeles) == 0:
        return 0, 0, 0

    # Calcular el promedio de cada canal por separado
    # pixeles[:, 0] → columna 0 = todos los valores H
    # pixeles[:, 1] → columna 1 = todos los valores S
    # pixeles[:, 2] → columna 2 = todos los valores V
    return (np.mean(pixeles[:, 0]),   # Hue promedio
            np.mean(pixeles[:, 1]),   # Saturation promedio
            np.mean(pixeles[:, 2]))   # Value promedio


def es_moneda_real(frame_hsv, cx, cy, radio):
    """
    Filtra detecciones falsas causadas por el papel o sombras.

    Problema que resuelve:
        HoughCircles a veces detecta círculos en el papel blanco (texto circular,
        manchas, bordes del papel). Estas zonas tienen Saturación muy baja (~0-15)
        porque el papel blanco no tiene color, solo brillo.
        Las monedas siempre tienen algo de color (S > 20).

    Filtros aplicados:
        SAT_MINIMA → descarta zonas sin color (papel blanco, fondo claro)
        VAL_MINIMA → descarta zonas muy oscuras (sombras profundas)

    Retorna:
        True  + valores HSV → es una moneda real, continuar procesando
        False + valores HSV → es una falsa detección, descartar
    """
    hue, sat, val = extraer_color_hsv(frame_hsv, cx, cy, radio)

    if sat < SAT_MINIMA:   # demasiado poco color → probablemente papel
        return False, hue, sat, val

    if val < VAL_MINIMA:   # demasiado oscuro → probablemente sombra
        return False, hue, sat, val

    return True, hue, sat, val


def clasificar(radio, ratio, hue, sat, val):
    """
    Determina qué moneda es la detectada usando tres criterios en orden de prioridad:

    CRITERIO 1 — Radio absoluto (radio_min / radio_max):
        Descarta monedas que físicamente no pueden ser de esa denominación.
        Si el radio en píxeles es 30, no puede ser una moneda de $1000.

    CRITERIO 2 — Ratio relativo (rt_min / rt_max):
        Compara el tamaño de esta moneda con la moneda más pequeña visible.
        Es más estable que el radio absoluto porque no cambia con la distancia.
        Ejemplo: la $1000 siempre mide ~1.3x más que la $100, sin importar
        qué tan lejos esté la cámara.

    CRITERIO 3 — Color HSV (hue + saturación):
        Desempata cuando dos monedas pasan los filtros de radio y ratio.
        El caso más importante: $200 (gris, S baja) vs $500 (dorada, S alta).

    Proceso:
        1. Busca todos los candidatos que pasen radio Y ratio.
        2. Si solo hay uno → retornarlo directamente.
        3. Si hay varios → elegir el que también coincide en color.
        4. Si ninguno coincide en color → retornar el primer candidato por ratio.

    Retorna:
        diccionario de la moneda encontrada, o None si no clasificó
    """
    candidatos = []

    for moneda in RATIOS_MONEDAS:
        # Verificar si el radio absoluto está dentro del rango esperado
        radio_ok = moneda["radio_min"] < radio < moneda["radio_max"]

        # Verificar si el ratio relativo está dentro del rango esperado
        ratio_ok = moneda["rt_min"] < ratio < moneda["rt_max"]

        # Verificar si el color HSV coincide con el de la moneda
        color_ok = (moneda["hue_min"] <= hue <= moneda["hue_max"] and
                    moneda["sat_min"] <= sat <= moneda["sat_max"])

        # Solo agregar como candidato si pasa radio Y ratio
        # El color se usa para desempatar, no para eliminar
        if radio_ok and ratio_ok:
            candidatos.append((moneda, color_ok))

    # Sin candidatos → no se pudo clasificar
    if not candidatos:
        return None

    # Un solo candidato → retornarlo sin necesitar el color
    if len(candidatos) == 1:
        return candidatos[0][0]

    # Varios candidatos → elegir el que también coincide en color
    con_color = [c for c in candidatos if c[1]]
    if con_color:
        return con_color[0][0]

    # Ninguno coincide en color → retornar el primero por radio/ratio
    return candidatos[0][0]


# =============================================================================
# SECCIÓN 5 — INICIALIZACIÓN DE LA CÁMARA
# =============================================================================
# VideoCapture(0) → cámara integrada del computador
# VideoCapture(1) → primera cámara externa conectada por USB
# Si la cámara no abre, cambiar el número (0, 1, 2...)

captura_de_video = cv.VideoCapture(1)


# =============================================================================
# SECCIÓN 6 — BUCLE PRINCIPAL DE DETECCIÓN
# =============================================================================
# El programa corre en un bucle infinito:
#   1. Captura un frame de la cámara
#   2. Lo preprocesa para facilitar la detección
#   3. Busca círculos con HoughCircles
#   4. Filtra y clasifica los círculos encontrados
#   5. Dibuja los resultados sobre la imagen
#   6. Muestra las ventanas actualizadas
#   7. Repite desde 1

while True:

    # ── Captura de frame ──────────────────────────────────────────────────────
    # .read() retorna dos valores:
    #   tipo_camara → True si el frame se capturó correctamente, False si falló
    #   camara      → el frame capturado como matriz de píxeles BGR (Alto x Ancho x 3)
    tipo_camara, camara = captura_de_video.read()

    # Si la cámara falla o se desconecta, salir del bucle
    if not tipo_camara:
        break


    # ── Preprocesamiento ──────────────────────────────────────────────────────

    # Convertir a espacio de color HSV para extraer el color de cada moneda.
    # HSV separa el color (Hue) del brillo (Value), lo que hace la clasificación
    # por color más robusta ante cambios de iluminación que BGR.
    frame_hsv = cv.cvtColor(camara, cv.COLOR_BGR2HSV)

    # Convertir a escala de grises para la detección de círculos.
    # HoughCircles solo trabaja con imágenes de un canal (escala de grises).
    gris = cv.cvtColor(camara, cv.COLOR_BGR2GRAY)

    # Ecualización del histograma: redistribuye los niveles de brillo para
    # aumentar el contraste. Útil cuando la iluminación es irregular o débil.
    # Ejemplo: una moneda oscura bajo luz tenue ganará contraste en sus bordes.
    ecualizada = cv.equalizeHist(gris)

    # Filtro Gaussiano: suaviza la imagen para reducir el ruido.
    # Sin este paso, HoughCircles detectaría demasiados bordes falsos causados
    # por la textura de las monedas y variaciones de brillo pixel a pixel.
    # (9, 9) → kernel 9x9 píxeles (más grande = más suavizado)
    # 2      → desviación estándar (controla cuánto se difumina)
    gauss = cv.GaussianBlur(ecualizada, (9, 9), 2)


    # ── Detección de círculos con HoughCircles ────────────────────────────────
    # HoughCircles busca círculos usando la Transformada de Hough Circular:
    #   Para cada píxel de borde posible, vota por todos los centros posibles
    #   a distancias entre RADIO_MIN y RADIO_MAX. Los centros con más votos
    #   son los círculos detectados.
    #
    # Retorna un array 3D de forma (1, N, 3) donde cada círculo es [cx, cy, radio]
    # Retorna None si no encuentra ningún círculo.
    circulos = cv.HoughCircles(
        gauss,                   # imagen preprocesada en escala de grises
        cv.HOUGH_GRADIENT,       # único método disponible en OpenCV
        dp=1,                    # resolución del acumulador = misma que la imagen
        minDist=DISTANCIA_MIN,   # distancia mínima entre centros detectados
        param1=PARAM1,           # umbral Canny interno de Hough
        param2=PARAM2,           # umbral acumulador (más alto = más estricto)
        minRadius=RADIO_MIN,     # radio mínimo a buscar en píxeles
        maxRadius=RADIO_MAX      # radio máximo a buscar en píxeles
    )


    # ── Preparación del frame de resultado ───────────────────────────────────
    # .copy() crea una copia independiente del frame original.
    # Los dibujos se hacen sobre esta copia, no sobre el frame original.
    resultado = camara.copy()

    # Inicializar acumuladores de suma para cada denominación
    suma_100 = suma_200 = suma_500 = suma_1000 = 0.0


    # ── Procesamiento de círculos detectados ──────────────────────────────────
    if circulos is not None:

        # np.around → redondea los valores flotantes al entero más cercano
        # np.uint16 → convierte a enteros sin signo de 16 bits (0 a 65535)
        # Necesario porque los píxeles y radios deben ser enteros para dibujar
        circulos_int = np.uint16(np.around(circulos))

        # ── Paso 1: Filtrar monedas reales ────────────────────────────────────
        # Antes de calcular ratios, descartar círculos que no son monedas
        # (papel blanco, sombras, ruido). Esto evita que un falso positivo
        # sea tomado como "la moneda más pequeña" y distorsione todos los ratios.
        monedas_validas = []

        for c in circulos_int[0]:   # circulos_int[0] → lista de [cx, cy, radio]
            cx    = int(c[0])       # coordenada X del centro
            cy    = int(c[1])       # coordenada Y del centro
            radio = int(c[2])       # radio en píxeles

            # Verificar si hay suficiente color y brillo en esta zona
            es_real, hue, sat, val = es_moneda_real(frame_hsv, cx, cy, radio)

            if es_real:
                monedas_validas.append((cx, cy, radio, hue, sat, val))


        # ── Paso 2: Calcular radio mínimo de referencia ───────────────────────
        if monedas_validas:
            # El radio mínimo entre todas las monedas reales detectadas
            # se usa como referencia para calcular los ratios relativos.
            # IMPORTANTE: si hubiera falsos positivos aquí, distorsionarían
            # todos los ratios (por eso filtramos primero en el Paso 1).
            radio_minimo = min(r for _, _, r, _, _, _ in monedas_validas)


            # ── Paso 3: Clasificar y dibujar cada moneda ──────────────────────
            for (cx, cy, radio, hue, sat, val) in monedas_validas:

                # ratio = qué tan grande es esta moneda respecto a la más pequeña
                # Si radio_minimo=52 y este radio=61 → ratio = 61/52 = 1.17
                ratio = radio / radio_minimo

                # ── Modo calibración ──────────────────────────────────────────
                if CALIBRAR:
                    # Dibujar círculo blanco (sin clasificar) sobre la moneda
                    cv.circle(resultado, (cx, cy), radio, (255, 255, 255), 2)

                    # Mostrar radio absoluto y ratio encima de la moneda
                    cv.putText(resultado,
                               f"r:{radio} rt:{ratio:.2f}",
                               (cx - 45, cy - 20),
                               cv.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

                    # Mostrar Hue y Saturación (valores clave para calibrar color)
                    cv.putText(resultado,
                               f"H:{hue:.0f} S:{sat:.0f}",
                               (cx - 45, cy + 2),
                               cv.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

                    # Mostrar Value (brillo)
                    cv.putText(resultado,
                               f"V:{val:.0f}",
                               (cx - 45, cy + 24),
                               cv.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

                # ── Modo detección normal ─────────────────────────────────────
                else:
                    # Intentar clasificar la moneda con los tres criterios
                    moneda = clasificar(radio, ratio, hue, sat, val)

                    if moneda:
                        # Moneda clasificada correctamente
                        # Dibujar círculo con el color de la denominación
                        cv.circle(resultado, (cx, cy), radio, moneda["color"], 2)
                        # Dibujar punto en el centro
                        cv.circle(resultado, (cx, cy), 3, moneda["color"], -1)
                        # Escribir el nombre de la moneda en el centro
                        cv.putText(resultado, moneda["nombre"],
                                   (cx - 35, cy + 5),
                                   cv.FONT_HERSHEY_SIMPLEX, 0.7, moneda["color"], 2)

                        # Acumular el valor en el total correspondiente
                        if moneda["valor"] == 100:    suma_100  += 100
                        elif moneda["valor"] == 200:  suma_200  += 200
                        elif moneda["valor"] == 500:  suma_500  += 500
                        elif moneda["valor"] == 1000: suma_1000 += 1000

                    else:
                        # Moneda real pero no clasificada → mostrar datos para calibrar
                        # El círculo gris indica "es real pero no sé cuál es"
                        cv.circle(resultado, (cx, cy), radio, (100, 100, 100), 1)
                        cv.putText(resultado,
                                   f"r:{radio} rt:{ratio:.2f} S:{sat:.0f}",
                                   (cx - 40, cy),
                                   cv.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)


    # ── Mostrar total o mensaje de modo ──────────────────────────────────────
    if not CALIBRAR:
        # Calcular y mostrar el total acumulado en la esquina superior izquierda
        total = suma_100 + suma_200 + suma_500 + suma_1000
        cv.putText(resultado,
                   f"TOTAL: $ {int(total)} COP",
                   (10, 35),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    else:
        # Recordar al usuario que está en modo calibración
        cv.putText(resultado,
                   "MODO CALIBRACION — anota r, rt, H, S de cada moneda",
                   (10, 30),
                   cv.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)


    # ── Mostrar ventanas ──────────────────────────────────────────────────────
    # Ventana con el frame crudo de la cámara (sin procesamiento)
    cv.imshow("camara", camara)

    # Ventana con los resultados: círculos, etiquetas y total
    cv.imshow("Resultado", resultado)


    # ── Control de teclado ────────────────────────────────────────────────────
    # cv.waitKey(1) → espera 1 milisegundo por una tecla
    # & 0xFF         → máscara para compatibilidad en sistemas de 64 bits
    # ord('q')       → código ASCII de la letra 'q'
    # Si el usuario presiona 'q', salir del bucle
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


# =============================================================================
# SECCIÓN 7 — LIMPIEZA Y CIERRE
# =============================================================================
# Liberar la cámara para que otros programas puedan usarla
captura_de_video.release()

# Cerrar todas las ventanas de OpenCV abiertas
cv.destroyAllWindows()