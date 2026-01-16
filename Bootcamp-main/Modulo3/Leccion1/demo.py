# Operaciones con vectores
import numpy as np

np.random.seed(42)

X = np.random.randint(8, 40, size=(5,7))
print(X)

mask_mayor_30 = X > 30
valores_mayor_30 = X[mask_mayor_30]
#print(valores_mayor_30)

X_clean = X.copy()
#print(X_clean)

X_clean[X_clean<15] = 15
#print(X_clean)

media_por_ciudad = X.mean(axis=1)
media_por_dia = X.mean(axis=0)
print(media_por_ciudad)
print(media_por_dia)

idx_ciudad_max = np.argmax(media_por_ciudad)
print(f"\nCiudad con mayor promedio: Ciudad {idx_ciudad_max} "
      f"({media_por_ciudad[idx_ciudad_max]:.2f}°C)")