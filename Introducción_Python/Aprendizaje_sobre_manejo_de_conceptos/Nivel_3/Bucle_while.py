# // Bucles while en Python
# -> Los bucles while permiten ejecutar un bloque de codigo repetitivamente.
# -> MIENTRAS una condicion sea verdadera.

# Se emplea WHILE cuando el número de iteraciones es desconocido y depende de que una condición se vuelva falsa

#-> ITERACION = Cada vez que se ejecuta el bloque de codigo dentro del bucle

print("Demostracion de funcion de bucle while, contador iniciado en 0 y se detiene al llegar a 3")
numero = 0 
while numero <= 3:  # Condición del bucle, sin el = 3 se detendria en 2
    print("El contador se ha actualizado , esta:", numero)
    numero += 1  # Incrementa el valor de numero en cada iteración
    
    
#EJEMPLO 1 -> Calcular la raiz cuadrada
    
import math
numero_ejemplo = int(input("Escriba un numero: "))

while numero_ejemplo < 0:
    print("Porfavor vuelva a ingresar un número, este debe ser positivo: ")
    numero_ejemplo = int(input("Escriba un numero positivo: "))
print("El resultado de la raiz cuadrada de", numero_ejemplo, "es:", math.sqrt(numero_ejemplo))

