# 1. Importar NumPy
import numpy as np 

# 2. Crear un conjunto de datos aleatorios (ej: 10 filas, 3 columnas)
# np.random.rand genera valores entre 0 y 1
data = np.random.rand(10, 3)
print("Datos Originales:\n", data)

# 3. Calcular la media por columna (axis=0 representa las columnas)
mean_col = np.mean(data, axis=0)
print("\nMedia por columna:", mean_col)

# 4. Calcular la desviación estándar por columna
std_col = np.std(data, axis=0)
print("Desviación estándar por columna:", std_col)

# 5. Estandarizar los datos (Z-score normalization)
# Fórmula: (dato - media) / desviación estándar
data_scaled = (data - mean_col) / std_col
print("\nDatos estandarizados (primeras 3 filas):\n", data_scaled[:3])