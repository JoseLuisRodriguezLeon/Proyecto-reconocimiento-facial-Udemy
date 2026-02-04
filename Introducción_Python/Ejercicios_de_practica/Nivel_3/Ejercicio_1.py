#// Ejercicios de práctica Python

#Ejercicio 1

print("USANDO EL BUCLE FOR\n")
print("Crear un programa que muestre la sumatoria de todos los números enteros entre 0 y 100\n")

print("Version 1, solo se muestra el resultado final (sumando desde el 0)\n")
#Proceso y salida de datos
suma = 0                                # Variable para almacenar la suma de los números
for i in range(101):                    # Itera desde 0 hasta 100 (101 no incluido)
    suma += i                           # Suma el valor de i a la variable suma
    print("La sumatoria de los números enteros entre 0 y 100 va en:", suma)
print("Fin del programa.")


print("Version 1, solo se muestra el resultado final\n")
#Proceso y salida de datos
suma = 1                                # Variable para almacenar la suma de los números
for i in range(2,101):                    # Itera desde 1 hasta 100 (101 no incluido)
    suma += i                           # Suma el valor de i a la variable suma
#Tambien es valido escribir: suma = suma + i
print("La sumatoria de TODOS los números enteros entre 0 y 100 es:", suma)
print("Fin del programa.")

