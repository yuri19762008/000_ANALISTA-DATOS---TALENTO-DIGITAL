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

# 6. Filtrar filas donde la primera característica (columna 0) sea mayor al promedio
# Usamos el promedio de la primera columna calculado en el paso 3
promedio_primera_col = mean_col[0]
filtered_data = data[data[:, 0] > promedio_primera_col]
print(f"\nFilas con primera col > {promedio_primera_col:.4f}:\n", filtered_data)

# 7. Agregar una columna con el promedio por fila
# axis=1 calcula el promedio horizontalmente
mean_row = np.mean(data, axis=1).reshape(-1, 1) # reshape para que sea una columna (10, 1)
data_with_mean = np.hstack((data, mean_row)) # hstack pega las columnas (concatenas con data)
print("\nMatriz con nueva columna de promedios (última col):\n", data_with_mean[:3])

# 8. Obtener la matriz de correlación entre columnas
# rowvar=False indica que las columnas son las variables
correlation_matrix = np.corrcoef(data, rowvar=False)
print("\nMatriz de correlación:\n", correlation_matrix)