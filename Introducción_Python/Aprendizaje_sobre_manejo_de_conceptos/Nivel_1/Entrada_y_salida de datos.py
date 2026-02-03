#// Entrada y salida de datos en Python

# Entrada de datos desde el usuario
nombre = input("Por favor, ingresa tu nombre: ")
edad = input("Por favor, ingresa tu edad: ")
# Salida de datos
print("Hola,", nombre + "!")
print("Tienes", edad, "años.")

# Conversión de tipos de datos
edad_int = int(edad)  # Convertir la edad a entero
print("El próximo año tendrás", edad_int + 1, "años.")


# Entrada de datos numéricos
numero1 = float(input("Ingresa un número decimal: "))
numero2 = float(input("Ingresa otro número decimal: "))
suma = numero1 + numero2
print("La suma de", numero1, "y", numero2, "es:", suma)

# Formateo de cadenas en la salida
print("Gracias por usar el programa, {}. ¡Hasta luego!".format(nombre))

