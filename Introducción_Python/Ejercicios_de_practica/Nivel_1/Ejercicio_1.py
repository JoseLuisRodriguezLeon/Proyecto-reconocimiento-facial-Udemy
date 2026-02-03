#// Ejercicios de práctica Python ()

#Ejercicio 1

a= int(input("Ingresa el primer número entero: "))
b = int(input("Ingresa el segundo número entero: "))
c= int(input("Ingresa el tercer número entero: "))

if a == 0:
    print("Error: No se puede dividir por cero. Por favor ingresa números enteros distintos de cero.")
    exit()
    
r = ((c+5)*((b)**2-(3*a*c)))/(4*a)

print("El resultado de la operación propuesta la formula en el ejercicio 1 (archivo .jpg adjunto) es:", r)