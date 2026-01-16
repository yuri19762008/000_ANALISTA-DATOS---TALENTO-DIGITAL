from functools import reduce
# 1. Definir la lista de diccionarios (Productos)
inventario = [
    {"nombre": "laptop", "precio": 800, "stock": 5},
    {"nombre": "mouse", "precio": 25, "stock": 0},
    {"nombre": "teclado", "precio": 45, "stock": 10},
    {"nombre": "monitor", "precio": 150, "stock": 3},
    {"nombre": "cable hdmi", "precio": 10, "stock": 0}
]

# 2. Filtrar productos con stock mayor a 0
def obtener_disponibles(lista1):
    """Devuelve una lista de productos que tienen stock mayor a 0."""
    return list(filter(lambda p: p["stock"]>0,lista1))

def formatear_nombres(lista2):
    """Devuelve una lista con los nombres de los productos en mayúsculas."""
    return list(map(lambda p: p["nombre"].upper(), lista2))

def calcular_valor_inventario(lista3):
    """Calcula el valor total del inventario (precio * stock) de los productos disponibles."""
    return reduce(lambda acumulador, p: acumulador + (p["precio"] * p["stock"]), lista3, 0)


def calcular_inventario():
    """Función principal para calcular y mostrar información del inventario."""
    disponibles = obtener_disponibles(inventario)
    nombres_mayusculas = formatear_nombres(disponibles)
    valor_total = calcular_valor_inventario(disponibles)

    print("Productos disponibles:", disponibles)
    print("Nombres en mayúsculas:", nombres_mayusculas)
    print("Valor total del inventario disponible:", valor_total)


if __name__ == "__main__":
    calcular_inventario()





