from functools import reduce # Importación específica según requerimiento 7

# 1. Definir la lista de diccionarios (Productos)
inventario = [
    {"nombre": "laptop", "precio": 800, "stock": 5},
    {"nombre": "mouse", "precio": 25, "stock": 0},
    {"nombre": "teclado", "precio": 45, "stock": 10},
    {"nombre": "monitor", "precio": 150, "stock": 3},
    {"nombre": "cable hdmi", "precio": 10, "stock": 0}
]

# 6. Funciones personalizadas para modularizar

def obtener_disponibles(lista):
    """Filtra productos que tengan stock mayor a 0 usando filter y lambda."""
    # Requerimiento 2: Aplicar filter() con lambda
    return list(filter(lambda p: p["stock"] > 0, lista))

def formatear_nombres(lista):
    """Transforma los nombres a mayúsculas usando map y lambda."""
    # Requerimiento 3: Usar map() para transformar nombres
    return list(map(lambda p: {**p, "nombre": p["nombre"].upper()}, lista))

def calcular_valor_total(lista):
    """Calcula el valor total del inventario (precio * stock) usando reduce."""
    # Requerimiento 4: Aplicar reduce() para el valor total
    return reduce(lambda acumulador, p: acumulador + (p["precio"] * p["stock"]), lista, 0)

# --- Lógica Principal ---
def ejecutar_inventario():
    print("--- Gestión de Inventario ---")
    
    # Filtrado
    disponibles = obtener_disponibles(inventario)
    
    # Transformación
    inventario_formateado = formatear_nombres(disponibles)
    
    # Cálculo total
    total_dinero = calcular_valor_total(disponibles)
    
    # 5. Mostrar resultados usando print()
    print("Productos disponibles (Nombres en mayúsculas):")
    for prod in inventario_formateado:
        print(f"- {prod['nombre']}: ${prod['precio']} (Stock: {prod['stock']})")
        
    print(f"\nValor total del inventario disponible: ${total_dinero}")

if __name__ == "__main__":
    ejecutar_inventario()