#// Ejercicios de práctica Python

#Ejercicio 2 CONJUNTOS
# SOLO SE TRABAJARA CON CONJUNTOS {}
# Revisar enunciado del ejercicio en el archivo JPG adjunto

A = {1, 2, 3, 4}
B = {2, 3, 5, 6}
C = {3, 4, 6, 7}

print("Conjuntos iniciales:")
print("A =", A)
print("B =", B)
print("C =", C) 

# a) Unión de A y B
union_AB = A | B #No se toma en cuenta datos repetidos
print("a) Unión de A y B:", union_AB)

# b) Intersección de B y C
interseccion_BC = (B&C)
print("b) Intersección de B y C:", interseccion_BC)

# c) Diferencia de A y C (elementos en A que no están en C)
diferencia_AC = A - C   
print("c) Diferencia de A y C:", diferencia_AC) #todos los elementos de A que no estan en C

# d) Diferencia simétrica entre B y C (elementos en B o C pero no en ambos)
diferencia_simetrica_BC = (B-C) | (C-B) # tambien se puede usar el operador " ^ " -> B ^ C
print("d) Diferencia simétrica entre B y C:", diferencia_simetrica_BC)

# e) Comprobar si A es subconjunto de B
print("e) ¿A es subconjunto de B?: ", A==B)