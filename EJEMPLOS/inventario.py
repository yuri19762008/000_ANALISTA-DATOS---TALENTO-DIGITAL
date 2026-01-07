from functools import reduce

# 1. Lista de diccionarios (productos)
inventario = [
    {"nombre": "manzana", "precio": 500, "stock": 10},
    {"nombre": "banana",  "precio": 300, "stock": 0},
    {"nombre": "naranja", "precio": 400, "stock": 5},
    {"nombre": "pera",    "precio": 450, "stock": 3},
]

# 2. filter() + lambda: productos disponibles (stock > 0)
productos_disponibles = list(filter(lambda p: p["stock"] > 0, inventario))

# 3. map(): transformar nombres a mayúsculas
productos_mayus = list(
    map(lambda p: {**p, "nombre": p["nombre"].upper()}, productos_disponibles)
)

# 4. reduce(): calcular valor total del inventario (precio * stock)
valor_total = reduce(
    lambda acc, p: acc + p["precio"] * p["stock"],
    productos_mayus,
    0
)

# 5. Mostrar resultados
print("Productos disponibles:")
for p in productos_mayus:
    print(f"- {p['nombre']}: ${p['precio']} (stock: {p['stock']})")

print(f"\nValor total del inventario: ${valor_total}")

# 6. Funciones personalizadas para modularizar

def filtrar_disponibles(productos):
    return list(filter(lambda p: p["stock"] > 0, productos))

def transformar_nombres_mayus(productos):
    return list(map(lambda p: {**p, "nombre": p["nombre"].upper()}, productos))

def calcular_valor_total(productos):
    return reduce(lambda acc, p: acc + p["precio"] * p["stock"], productos, 0)

# 7. Reutilizar funciones en otros contextos
if __name__ == "__main__":
    disponibles = filtrar_disponibles(inventario)
    mayus = transformar_nombres_mayus(disponibles)
    total = calcular_valor_total(mayus)

    print("\n--- Usando funciones reutilizables ---")
    for p in mayus:
        print(f"- {p['nombre']}: ${p['precio']} (stock: {p['stock']})")
    print(f"\nValor total (reutilizando funciones): ${total}")
