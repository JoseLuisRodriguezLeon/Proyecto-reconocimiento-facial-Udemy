#// Ejercicios de práctica Python

#Ejercicio 2

print("Compara dos nombres y verifica si hay coincidencias o no, si terminan en la misma letra o en la ultima\n")

#Entrada de datos
nombre1= (input("Ingresa el primer nombre: ")).lower()
nombre2 = (input("Ingresa el segundo nombre: ")).lower()

#Proceso y salida de datos
if nombre1 == nombre2:
    print("Los nombres son iguales.\n")
else:
    print("Los nombres son diferentes.\n")
    
if nombre1[-1] == nombre2[-1]:
    print("Los nombres terminan con la misma letra.\n")
else:
    print("Los nombres no terminan con la misma letra.\n")

if nombre1[0] == nombre2[0]:
    print("Los nombres comienzan con la misma letra.\n")
else:
    print("Los nombres no comienzan con la misma letra.\n")
    
print("Fin del programa.")

