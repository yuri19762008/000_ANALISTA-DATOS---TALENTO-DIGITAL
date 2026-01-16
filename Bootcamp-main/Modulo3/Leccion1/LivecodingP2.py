import numpy as np

np.random.seed(42)

X = np.random.randint(10, 40, size=(5, 7))

print(X)

mask_mayor_30 = X > 30
valores_mayor_30 = X[mask_mayor_30]
print("\nValores > 30°C:\n", valores_mayor_30)


X_clean = X.copy()
X_clean[X_clean < 15] = 15
print(X_clean)

# Estadisticas utiles
media_por_ciudad = X_clean.mean(axis=1) #1 fila
media_por_dia = X_clean.mean(axis=0) # 0 columna

print(media_por_ciudad)
print(media_por_dia)

#argmax te dice dónde está el valor más grande dentro de un arreglo.
#No devuelve el valor, devuelve la posición (índice).

idx_ciudad_max = np.argmax(media_por_ciudad)
print(f"\nCiudad con mayor promedio: Ciudad {idx_ciudad_max + 1} "
      f"({media_por_ciudad[idx_ciudad_max]:.2f}°C)")


idx_dia_max = np.argmax(media_por_dia)
print(f"\nDia con mayor promedio: Dia {idx_dia_max + 1} "
      f"({media_por_dia[idx_dia_max]:.2f}°C)")
