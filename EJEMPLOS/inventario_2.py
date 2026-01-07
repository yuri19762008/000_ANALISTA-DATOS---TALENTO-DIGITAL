# archivo: inventario.py
from functools import reduce

# -----------------------------
# Datos de ejemplo
# -----------------------------
productos = [
    {"nombre": "Teclado",   "precio": 15_000, "stock": 10},
    {"nombre": "Mouse",     "precio":  8_000, "stock": 0},
    {"nombre": "Monitor",   "precio":120_000, "stock": 5},
    {"nombre": "Notebook",  "precio":550_000, "stock": 2},
    {"nombre": "Cable HDMI","precio": 5_000,  "stock": 0},
]

# -----------------------------
# Funciones del módulo
# -----------------------------
def filtrar_con_stock(lista_productos):
    """Devuelve solo los productos con stock > 0."""
    return list(filter(lambda p: p["stock"] > 0, lista_productos))

def calcular_valor_producto(producto):
    """Valor total de un producto (precio * cantidad)."""
    return producto["precio"] * producto["stock"]

def calcular_valor_total_stock(lista_productos):
    """Usa reduce para sumar el valor total del stock disponible."""
    return reduce(
        lambda acumulado, prod: acumulado + calcular_valor_producto(prod),
        lista_productos,
        0
    )

def mostrar_productos(lista_productos):
    """Imprime los productos de forma ordenada."""
    print("Productos con stock disponible:\n")
    for p in lista_productos:
        valor = calcular_valor_producto(p)
        print(f"- {p['nombre']}: precio ${p['precio']}, "
              f"stock {p['stock']}, valor total ${valor}")
    print()  # línea en blanco


# -----------------------------
# Punto de entrada (main)
# -----------------------------
def main():
    # 1. Filtrar productos con stock
    productos_con_stock = filtrar_con_stock(productos)

    # 2. Mostrar productos
    mostrar_productos(productos_con_stock)

    # 3. Calcular valor total del stock disponible
    total = calcular_valor_total_stock(productos_con_stock)
    print(f"Valor total del stock disponible: ${total}")


if __name__ == "__main__":
    main()
