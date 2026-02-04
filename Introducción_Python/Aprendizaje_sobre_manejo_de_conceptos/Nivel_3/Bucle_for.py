# // Bucles For en Python
# -> Los bucles while permiten ejecutar un bloque de codigo repetitivamente.

# El bucle FOR se utiliza cuando se conoce de antemano el número exacto de iteraciones (bucle definido)
# Ideal para recorrer listas o rangos con un numero fijo de elementos

# i -> centinela para control de bucle (variable de iteracion)
print("Demostracion de funcion de bucle for, iterando desde 0 hasta 4")
for i in range(5):  # Itera desde 0 hasta 4 (5 no incluido). es la forma en la que Python maneja los rangos
    print("Iteración número:", i)
    
    
print("\nDemostracion de funcion de bucle for, iterando desde 0 hasta 5")
#Si se quiere que el bucle llegue hasta el número N, se debe escribir range(inicio, N + 1)    

for i in range(0,6):  # Itera desde 0 hasta 5 (6 no incluido)
    print("Iteración número:", i)
    
# EJEMPLO DE USO DE BUCLE FOR PARA RECORRER UNA LISTA
array_ejemplo = ["Manzana", 2, "Cereza",6.5, True, [1,2,3], "Final"]

print("\nDemostracion de funcion de bucle for, recorriendo una lista")

#Recorre la lista hasta el final (no hallar mas elementos), elemento por elemento
for elemento in array_ejemplo:
    print("Elemento actual de la lista:", elemento)