#// Ejercicios de práctica Python

#Ejercicio 2

input1= int(input("Ingresa el primer número: "))
input2 = int(input("Ingresa el segundo número: "))
print("Los valores ingresados son:\n", "a =", input1, "y","b =", input2)

#Cambio de valores

print("CAMBIO DE VALORES!\n")
print("...Procesando...\n")
input1, input2 = input2, input1

print("Los valores intercambiados son:\n", "a =", input1, "y","b =", input2)