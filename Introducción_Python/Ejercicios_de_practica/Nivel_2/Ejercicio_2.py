#// Ejercicios de práctica Python

#Ejercicio 2

print("Programa que pide tres números enteros y determina cual es el mayor de los tres\n")

#Entrada de datos
a= int(input("Ingresa el primer número entero: "))
b = int(input("Ingresa el segundo número entero: "))
c= int(input("Ingresa el tercer número entero: "))

#Proceso y salida de datos
if a >=b and a >= c:
    print("El número mayor es:\n", a)
elif b >= a and b >= c:
    print("El número mayor es:\n", b) 
else:
    print("El número mayor es:\n", c)
    
print("\nFin del programa.")