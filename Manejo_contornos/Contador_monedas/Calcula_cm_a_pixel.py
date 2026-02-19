# calcula tamano de papel cm a pixel

    # A mayor DPI, más píxeles y mayor calidad de imagen:
def cm_a_pixels():
    ancho_cm  = float(input("Ancho (cm): "))
    alto_cm = float(input("Alto (cm): "))
    dpi       = float(input("DPI: "))

    ancho_px  = round(ancho_cm  * dpi / 2.54)
    alto_px = round(alto_cm * dpi / 2.54)

    print("ancho", ancho_px, "alto", alto_px)
    return ancho_px, alto_px

cm_a_pixels()