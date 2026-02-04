# // funciones de listas en Python
# Contenido trabajado y adaptado por: JOSE LUIS RODRIGUEZ LEON
# Organizacion del codigo propuesta por Chat Gpt-4

# Inicialización de la lista
array = [0, "Juan", 4, True, "Maria", (1, 2, 3), 5.6]

print("=" * 50)
print("LISTA INICIAL")
print("=" * 50)
print(f"Contenido: {array}")
print(f"Longitud: {len(array)}\n") #LEN para longitud de la lista (numerico de elementos)

# ============================================
# AGREGAR ELEMENTOS
# ============================================
print("=" * 50)
print("AGREGAR ELEMENTOS")
print("=" * 50)

# append() - Agrega un elemento SOLO al final
array.append("Nuevo Elemento")
print(f"Después de append('Nuevo Elemento'):\n{array}\n")

array.append("Maria")
print(f"Después de append('Maria'):\n{array}\n")

# ============================================
# ELIMINAR ELEMENTOS
# ============================================
print("=" * 50)
print("ELIMINAR ELEMENTOS")
print("=" * 50)

# pop() - Elimina y puede devolver el último elemento, si no se guarda en variable, se pierde
elemento_eliminado = array.pop()
print(f"Elemento eliminado con pop(): {elemento_eliminado}")
print(f"Lista actualizada:\n{array}\n")

# pop(índice) - Elimina elemento en posición específica
elemento_eliminado = array.pop(2)
print(f"Elemento eliminado en índice 2: {elemento_eliminado}")
print(f"Lista actualizada:\n{array}\n")

# remove() - Elimina la primera aparición de un valor
array.remove("Juan")
print(f"Después de remove('Juan'):\n{array}\n")

# ============================================
# INSERTAR ELEMENTOS
# ============================================
print("=" * 50)
print("INSERTAR ELEMENTOS")
print("=" * 50)

# insert() - Inserta elemento en posición específica
array.insert(1, "Elemento Insertado")
print(f"Después de insert(1, 'Elemento Insertado'):\n{array}\n")

# ============================================
# BÚSQUEDA Y CONTEO
# ============================================
print("=" * 50)
print("BÚSQUEDA Y CONTEO")
print("=" * 50)

# count() - Cuenta apariciones de un elemento
count_maria = array.count("Maria")
print(f"Número de veces que 'Maria' aparece: {count_maria}")

# index() - Encuentra el índice de un elemento
if "Juan" in array:
    indice_juan = array.index("Juan")
    print(f"Índice de 'Juan': {indice_juan}")
if "Juan" not in array:
    print("'Juan' no está en la lista")

# in - Verifica si un elemento está en la lista
esta_maria = "Maria" in array
print(f"¿'Maria' está en la lista?: {esta_maria}\n")

# ============================================
# MODIFICAR ORDEN
# ============================================
print("=" * 50)
print("MODIFICAR ORDEN")
print("=" * 50)

# reverse() - Invierte el orden de los elementos
array.reverse()
print(f"Después de reverse():\n{array}\n")

# ============================================
# COPIAR Y LIMPIAR
# ============================================
print("=" * 50)
print("COPIAR Y LIMPIAR")
print("=" * 50)

# copy() - Crea una copia de la lista
print("Array original antes de clear():", array)
new_array = array.copy()
print(f"Copia del array: {new_array}\n")

# clear() - Elimina todos los elementos
array.clear()
print(f"Después de clear():\n{array}")
print(f"Backup del array:\n{new_array}\n")

# ============================================
# EXTENDER Y ORDENAR
# ============================================
print("=" * 50)
print("EXTENDER Y ORDENAR")
print("=" * 50)

# extend() - Agrega múltiples elementos
array.extend(["C", "B", "A"])
print(f"Después de extend(['C', 'B', 'A']):\n{array}\n")

# sort() - Ordena la lista, Para caracteres A-Z, a-z, 0-9. Se usa el mismo orden que su valor ASCII para ordenar
array.sort(key=str)
print(f"Después de sort(key=str):\n{array}\n")

print("=" * 50)
print("FIN DEL PROGRAMA")
print("=" * 50)


