#// Ejercicios de práctica Python

#Ejercicio 4

print("Obtener precio final que se obtiene al pagar un producto con descuento de 36%\n")

#Entrada de datos
precio_producto = float(input("Ingresa el precio del producto: "))
print("calculando el precio final con el descuento aplicado......\n")

descuento = precio_producto*(36/100)

precio_final = precio_producto - descuento

print(f"El precio final del producto con el descuento aplicado es de: {precio_final:.2f}")