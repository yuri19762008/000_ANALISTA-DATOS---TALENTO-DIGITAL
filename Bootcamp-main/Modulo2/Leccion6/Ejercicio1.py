# 1. Crear una lista de diccionarios (nombre, stock y precio)
inventario = [
    {"nombre": "Arroz", "stock": 10, "price": 1.50},
    {"nombre": "Leche", "stock": 3, "price": 0.99},
    {"nombre": "Pan", "stock": 15, "price": 0.50},
    {"nombre": "Huevos", "stock": 2, "price": 2.10},
    {"nombre": "Aceite", "stock": 4, "price": 3.80}
]

# 2. Usar un for para recorrer los productos
print("--- Alertas de Stock Bajo (Menor a 5) ---")
total_valor_bajo_stock = 0
cantidad_bajo_stock = 0

for producto in inventario:
    # 2a. Imprimir solo los productos cuyo stock sea menor a 5
    if producto["stock"] < 5:
        print(f"ALERTA: El producto '{producto['nombre']}' tiene solo {producto['stock']} unidades.")
        # Acumulamos datos para el punto 4
        cantidad_bajo_stock += 1
        total_valor_bajo_stock += (producto["stock"] * producto["price"])

print("-" * 40)

# 3. Usar list comprehension para crear la lista 'reposicion' con los nombres
reposicion = [p["nombre"] for p in inventario if p["stock"] < 5]
print(f"Productos a reponer: {reposicion}")

# 4. Imprimir el total de productos en bajo stock y su valor total
print(f"Cantidad de productos en bajo stock: {cantidad_bajo_stock}")
print(f"Valor total de la mercadería en bajo stock: ${total_valor_bajo_stock:.2f}")

print("-" * 40)

# 5. Usar un while que simule el ingreso de productos hasta escribir "salir"
print("Registro de nuevos productos (Escriba 'salir' para terminar)")
while True:
    nuevo_nombre = input("Nombre del producto: ")
    if nuevo_nombre.lower() == "salir":
        break
    
    # Pedimos los otros datos
    nuevo_stock = int(input(f"Cantidad de stock para {nuevo_nombre}: "))
    nuevo_precio = float(input(f"Precio para {nuevo_nombre}: "))
    
    # Agregamos el nuevo diccionario a nuestra lista
    inventario.append({"nombre": nuevo_nombre, "stock": nuevo_stock, "price": nuevo_precio})
    print(f"¡{nuevo_nombre} agregado con éxito!")

print("\nInventario actualizado finalizado.")