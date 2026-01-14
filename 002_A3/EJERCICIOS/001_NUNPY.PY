import numpy as np

# 1. Carga y estructuración de datos -------------

# Simulamos precios de 5 acciones (filas) durante 5 días (columnas)
# Puedes ajustar los valores según necesites
precios = np.array([
    [100, 102, 101, 105, 107],  # Acción 1
    [50,  51,  49,  52,  53],   # Acción 2
    [200, 198, 202, 205, 210],  # Acción 3
    [80,  79,  81,  82,  84],   # Acción 4
    [120, 121, 119, 122, 125]   # Acción 5
])

# Verificamos que sea 5x5
print("Matriz de precios (5x5):")
print(precios)
print("Shape:", precios.shape)


# 2. Análisis y transformación de datos --------------------------

# 2.1 Promedio, máximo y mínimo de cada acción (por filas)
promedio_por_accion = precios.mean(axis=1)
max_por_accion = precios.max(axis=1)
min_por_accion = precios.min(axis=1)

print("\nPromedio por acción:", promedio_por_accion)
print("Máximo por acción:", max_por_accion)
print("Mínimo por acción:", min_por_accion)

# 2.2 Variación porcentual diaria de cada acción
# (precio_dia_actual - precio_dia_anterior) / precio_dia_anterior * 100
variacion_pct = (precios[:, 1:] - precios[:, :-1]) / precios[:, :-1] * 100
print("\nVariación porcentual diaria (4 días por acción):")
print(variacion_pct)

# 2.3 Funciones matemáticas: logaritmo, exponencial, normalización

# Logaritmo natural de los precios
log_precios = np.log(precios)
print("\nLogaritmo natural de precios:")
print(log_precios)

# Exponencial (ejemplo artificial, no tiene sentido financiero directo aquí)
exp_precios = np.exp(precios / 100)  # escalado para que no explote
print("\nExponencial de precios (escalados):")
print(exp_precios)

# Normalización min-max por acción: (x - min) / (max - min)
min_por_accion = precios.min(axis=1, keepdims=True)
max_por_accion = precios.max(axis=1, keepdims=True)
precios_norm = (precios - min_por_accion) / (max_por_accion - min_por_accion)
print("\nPrecios normalizados (min-max por acción):")
print(precios_norm)


# 3. Optimización e indexación avanzada --------------------------

# 3.1 Índices: rendimiento de una acción en un día específico
# Ejemplo: Acción 3, Día 4 (recordar que Python indexa desde 0)
accion_idx = 2   # tercera fila
dia_idx = 3      # cuarto día
precio_especifico = precios[accion_idx, dia_idx]
print(f"\nPrecio de la acción 3 en el día 4: {precio_especifico}")

# 3.2 Selección de varias acciones y días con indexación avanzada
# Ejemplo: acciones 1, 3 y 5 en los días 2 y 5
acciones_sel = [0, 2, 4]
dias_sel = [1, 4]
submatriz = precios[np.ix_(acciones_sel, dias_sel)]
print("\nSubmatriz (acciones 1,3,5 y días 2,5):")
print(submatriz)

# 3.3 Broadcasting: restar el promedio de cada acción a sus precios
# (centrado por fila)
promedio_por_accion = precios.mean(axis=1, keepdims=True)
precios_centrados = precios - promedio_por_accion
print("\nPrecios centrados por acción (restando el promedio):")
print(precios_centrados)

# Broadcasting: aumentar todos los precios un 5%
precios_mas_5 = precios * 1.05
print("\nPrecios incrementados en 5%:")
print(precios_mas_5)
