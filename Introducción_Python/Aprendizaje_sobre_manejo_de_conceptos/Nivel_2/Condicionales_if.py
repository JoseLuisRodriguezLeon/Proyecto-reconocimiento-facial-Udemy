#// Condicionales if en Python

#if condición:

#else:
#    bloque de código si la condición es falsa

#Ejemplo 1: Verificar si un número es positivo o negativo

print("Estructura básica de un condicional if en Python:\n")
print("if condición:")
dato = float(input("Ingresa un número: "))

if dato > 0:
    print("El número es positivo.")
elif dato == 0:
    print("El número es cero.")
else:
    print("El número es negativo.")
    

print("\nPuedes agregar tantas condiciones 'elif' como necesites para evaluar múltiples casos.")
print("Recuerda que la indentación es crucial en Python para definir bloques de código.")
