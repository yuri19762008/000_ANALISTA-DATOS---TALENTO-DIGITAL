from functools import reduce

# 1. Definir la lista de diccionarios (Productos)
inventario = [
    {"nombre": "laptop", "precio": 800, "stock": 5},
    {"nombre": "mouse", "precio": 25, "stock": 0},
    {"nombre": "teclado", "precio": 45, "stock": 10},
    {"nombre": "monitor", "precio": 150, "stock": 3},
    {"nombre": "cable hdmi", "precio": 10, "stock": 0}
]

def obtener_disponibles(lista):
    """Función que filtra y devuelve los productos que están en stock."""
    return list(filter(lambda producto: producto["stock"] > 0, lista))

def formatear_nombres(lista):
    """Función que formatea los nombres de los productos a mayúsculas."""
    return list(map(lambda producto: producto["nombre"].upper(), lista))

def calcular_valor_total(lista):
    """Función que calcula el valor total del inventario disponible."""
    return reduce(lambda total, producto: total + (producto["precio"] * producto["stock"]), lista, 0)

def ejecutar_inventario():
    """Función principal para ejecutar las operaciones del inventario."""
    disponibles = obtener_disponibles(inventario)
    nombres_formateados = formatear_nombres(disponibles)
    valor_total = calcular_valor_total(disponibles)

    print("Productos disponibles:", disponibles)
    print("Nombres formateados:", nombres_formateados)
    print("Valor total del inventario disponible:", valor_total)

if __name__ == "__main__":
    ejecutar_inventario()







