#// Ejercicios de práctica Python

#Ejercicio 3
import math

print("Calculo del radio y longitud de un circulo\n")

#Entrada de datos
r= float(input("Ingresa el valor del radio del circulo: "))

area = math.pi * r**2
longitud = 2 * math.pi * r

#Salida de datos a solo 2 decimales
print("El valor de la longitud del circulo es:", round(longitud, 2))
print("El valor del área del circulo es:", round(area, 2))