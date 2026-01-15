import numpy as np

# (Opcional) Para que te salga siempre lo mismo mientras practicas
np.random.seed(42)

# 1) Simular matriz 5x7 con temperaturas enteras entre 10°C y 40°C
#    Ojo: np.random.randint(low, high) incluye low pero EXCLUYE high
temps = np.random.randint(10, 41, size=(5, 7))
print("Temperaturas (5 ciudades x 7 días):\n", temps)

# 2) Identificar temperaturas que superan los 30°C
mask_mayor_30 = temps > 30
temps_mayor_30 = temps[mask_mayor_30]
print("\nTemperaturas > 30°C:\n", temps_mayor_30)

# 3) Reemplazar valores inferiores a 15°C por el valor 15
#    (esto "limpia" los datos, poniendo un mínimo)
temps_limpias = temps.copy()
temps_limpias[temps_limpias < 15] = 15
print("\nTemperaturas limpias (mínimo 15°C):\n", temps_limpias)

# 4) Medias por ciudad (fila) y por día (columna)
media_por_ciudad = temps_limpias.mean(axis=1)  # 5 valores
media_por_dia = temps_limpias.mean(axis=0)     # 7 valores
print("\nMedia por ciudad (fila):\n", media_por_ciudad)
print("\nMedia por día (columna):\n", media_por_dia)

# 5) Ciudad con mayor temperatura promedio
idx_ciudad_max = np.argmax(media_por_ciudad)  # índice 0..4
print("\nCiudad con mayor promedio:",
      idx_ciudad_max,
      "con promedio:",
      media_por_ciudad[idx_ciudad_max])