# // Operadores lógicos en Python

a = True
b = False

print("Valores iniciales: a =", a, ", b =", b)

# Operador AND 
print("--------------")
and_result = a and b
print("Operador AND (a and b):", and_result)

# Operador OR
print("--------------")
or_result = a or b
print("Operador OR (a or b):", or_result)

# Operador NOT
print("--------------")
not_a = not a
not_b = not b
print("Operador NOT (not a):", not_a)
print("Operador NOT (not b):", not_b)

# EJEMPLO DE USO DE OPERADORES LÓGICOS
print("--------------")
x = 10
y = 5
z = 15
print("Valores iniciales: x =", x, ", y =", y, ", z =", z)
print("--------------")
print("Evaluar si (x > y) AND (z > x):")
result = (x > y) and (z > x)
print("Resultado:", result)
print("--------------")
print("Evaluar si (x < y) OR (z > y):")
result = (x < y) or (z > y)
print("Resultado:", result)
print("--------------")
print("Evaluar NOT (x == y):")
result = not (x == y)
print("Resultado:", result)
