#// Ejercicios de práctica Python

#Ejercicio 1

print("Programa que pide dos números enteros y detecta cual de ellos es par\n")

#Entrada de datos
num1= int(input("Ingresa el primer número entero: "))
num2 = int(input("Ingresa el segundo número entero: \n"))

#Proceso y salida de datos
if num1 % 2 == 0:
    print("El número", num1, "es par.")
else:
    print(f"El número {num1} es impar.")

if num2 % 2 == 0:
    print(f"El número {num2} es par.")
else:
    print(f"El número {num2} es impar.\n")
    
print("Fin del programa.")