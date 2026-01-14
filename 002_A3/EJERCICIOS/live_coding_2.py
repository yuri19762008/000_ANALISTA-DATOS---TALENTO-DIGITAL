import numpy as np

np.random.seed(42)

# 1) Matriz X (5 ciudades x 7 días) con valores entre 10 y 40
X = np.random.randint(10, 41, size=(5, 7))

# Creamos un "y real" por ciudad (etiqueta)
# Para mantenerlo simple: promedio semanal + un pequeño ruido
y = X.mean(axis=1) + np.random.normal(0, 1, size=5)

print("X (temperaturas):\n", X)
print("\ny (etiquetas reales por ciudad):\n", y)

# 2) Identificar temperaturas mayores a 30
mask_mayor_30 = X > 30
valores_mayor_30 = X[mask_mayor_30]
print("\nValores > 30°C:\n", valores_mayor_30)

# 3) Limpieza: valores menores a 15 se reemplazan por 15
X_clean = X.copy()
X_clean[X_clean < 15] = 15
print("\nX limpio (mínimo 15°C):\n", X_clean)

# 4) Estadísticas útiles
media_por_ciudad = X_clean.mean(axis=1)  # 5 ciudades
media_por_dia = X_clean.mean(axis=0)     # 7 días

print("\nMedia por ciudad:\n", media_por_ciudad)
print("\nMedia por día:\n", media_por_dia)

idx_ciudad_max = np.argmax(media_por_ciudad)
print(f"\nCiudad con mayor promedio: Ciudad {idx_ciudad_max + 1} "
      f"({media_por_ciudad[idx_ciudad_max]:.2f}°C)")

# 5) Predicción simple (y_hat) y error MSE
# y_hat: "predigo que la etiqueta de la ciudad será su promedio semanal"
y_hat = media_por_ciudad

mse = np.mean((y - y_hat) ** 2)
print("\ny_hat (predicción simple):\n", y_hat)
print("\nMSE (error promedio al cuadrado):\n", mse)