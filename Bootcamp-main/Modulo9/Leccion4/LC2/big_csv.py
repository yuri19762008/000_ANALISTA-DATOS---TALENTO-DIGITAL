import pandas as pd
import numpy as np
import os

# Parámetros del dataset
N = 500000  # número de filas, ajústalo según necesites

np.random.seed(42)  # para reproducibilidad

# Listas de valores posibles
regiones = ["Norte", "Centro", "Sur"]
categorias = ["Electronica", "Hogar", "Deportes", "Juguetes", "Moda"]
metodos_pago = ["Tarjeta", "Efectivo", "Online"]

# Aseguramos que exista la carpeta data/
os.makedirs("data", exist_ok=True)

# 1) id_venta secuencial
id_venta = np.arange(1, N + 1)

# 2) fechas aleatorias entre 2024-01-01 y 2026-12-31
fechas_inicio = pd.to_datetime("2024-01-01")
offsets = np.random.randint(0, 3 * 365, size=N)
fechas = fechas_inicio + pd.to_timedelta(offsets, unit="D")

# Versión sencilla: formatear directamente el DatetimeIndex a string
fechas_str = fechas.strftime("%Y-%m-%d")

# 3) otras columnas aleatorias
tienda_id = np.random.randint(1, 51, size=N)          # 1 a 50
region = np.random.choice(regiones, size=N)
categoria = np.random.choice(categorias, size=N)
producto_id = np.random.randint(1, 5001, size=N)      # 1 a 5000
cantidad = np.random.randint(1, 11, size=N)           # 1 a 10
precio_unitario = np.round(np.random.uniform(5, 2000, size=N), 2)
descuento_pct = np.random.choice([0, 5, 10, 15], size=N)
metodo_pago = np.random.choice(metodos_pago, size=N)
cliente_id = np.random.randint(1, 100001, size=N)     # 1 a 100000

# 4) monto con descuento
monto = np.round(precio_unitario * cantidad * (1 - descuento_pct / 100), 2)

# 5) construir el DataFrame
df = pd.DataFrame({
    "id_venta": id_venta,
    "fecha": fechas_str,              # ya viene formateado YYYY-MM-DD
    "tienda_id": tienda_id,
    "region": region,
    "categoria": categoria,
    "producto_id": producto_id,
    "cantidad": cantidad,
    "precio_unitario": precio_unitario,
    "descuento_pct": descuento_pct,
    "monto": monto,
    "metodo_pago": metodo_pago,
    "cliente_id": cliente_id,
})

# 6) guardar a CSV
output_path = r"D:\000_ANALISTA_DATOS\Bootcamp-main\Modulo9\Leccion4\LC2\data/ventas_big.csv"
df.to_csv(output_path, index=False, encoding="utf-8")
print("CSV generado en:", output_path, "con filas:", len(df))
