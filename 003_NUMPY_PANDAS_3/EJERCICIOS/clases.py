# Operaciones con vectores
import numpy as np
vector = np.array([1,2,3,4,5])
print(vector)
print(vector*2)

# Operaciones entre Vectores
vector1 = np.array([1,2,3])
vector2 = np.array([4,5,6])
suma = vector1 + vector2
print(suma)

# Creación de Matrices
# Crear una matriz 3x3
matrix = np.array([
 [1, 2, 3],
 [4, 5, 6],
 [7, 8, 9]
])

# Acceso a Elementos de una Matriz
valor = matrix[1,2]
print(valor)

# Operaciones con Matrices
matriz_cuadrada = matrix ** 2
print(matriz_cuadrada)

# Multiplicación de matrices
# Creamos dos matrices
A = np.array([[1, 2], 
              [3, 4]])

B = np.array([[5, 6], 
              [7, 8]])

# Multiplicación de matrices
resultado = A @ B

print(resultado)

resultado = np.dot(A, B)


# Arreglo con valores (arange)
secuencia = np.arange(0, 10, 2)  # Values de 0 a 10
print(secuencia)

# Matrices de ceros y unos
# Matriz de ceros 3x3
zeros_matrix = np.zeros((3, 3))

# Matriz de unos 2x4
ones_matrix = np.ones((2, 4))

print(zeros_matrix)
print(ones_matrix)

# Vector con distribución de puntos
# 5 puntos equidistantes entre 0 y 1
points = np.linspace(0, 1, 5)
print(points)

# Matriz Identidad
# Matriz identidad 3x3
identity = np.eye(3)
print(identity)

# Matriz Aleatoria
matriz_aleatoria = np.random.rand(3,3)
print(matriz_aleatoria)

# Redimensionado de un arreglo
# Vector de 12 elementos
arr = np.arange(12)
# Redimensionar a matriz 3x4
reshaped = arr.reshape(3, 4)

print(arr)
print(reshaped)

#### PARTE 2 ####
# Selección de elementos de un arreglo
vector = np.array([10,20,30,40,50])
print(vector[2])
print(vector[0:2])

# Indexación en matrices
# Acceder al elemento en la fila 1, columna 2
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
element = matrix[1, 2]  # Valor: 6
print(element)

# Ejemplos de Slicing
# Vector
arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
slice1 = arr[2:7]  # [2, 3, 4, 5, 6]
slice2 = arr[::2]  # [0, 2, 4, 6, 8]

print(slice1)
print(slice2)

# Matriz
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
rows_1_2 = matrix[1:3]  # Filas 1 y 2
cols_0_1 = matrix[:, 0:2]  # Columnas 0 y 1
print(rows_1_2)
print(cols_0_1)

# Selección condicional de elementos
numeros = np.array([3,7,2,8,5])
mayores_a_5 = numeros[numeros > 5]
print(mayores_a_5)

# Combinación de condiciones
arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

# Elementos mayores que 2 Y menores que 7
condition = (arr > 2) & (arr < 7)
result = arr[condition]  # [3, 4, 5, 6]

print(result)

# Referencia y copia de arreglos
original = np.array([1,2,3,4])
copia_ref = original
copia_ref[0] = 99
print(original)

# Creación de copias
original = np.array([1,2,3,4])
copia_ref = original.copy()
copia_ref[0] = 99
print(original)
print(copia_ref)

# Referencia (no copia)
arr = np.array([1, 2, 3, 4])
ref = arr  # Referencia al mismo arreglo

# Copia real
copy_arr = arr.copy()  # Nueva copia independiente

# Operaciones entre arreglos
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Operaciones elemento a elemento
suma = a + b  # [5, 7, 9]
resta = a - b  # [-3, -3, -3]
producto = a * b  # [4, 10, 18]
division = a / b  # [0.25, 0.4, 0.5]

print(suma)
print(resta)
print(producto)
print(division)

# Ejemplo de Broadcasting
# Vector y escalar
arr = np.array([1, 2, 3, 4])
result = arr + 10  # [11, 12, 13, 14]
print(result)

# Matriz y vector
matrix = np.array([[1, 2, 3], [4, 5, 6]])
vector = np.array([10, 20, 30])
result = matrix + vector
print(result)

# Operaciones con Escalares
arr = np.array([1, 2, 3, 4])

# Operaciones con escalares
suma = arr + 5  # [6, 7, 8, 9]
producto = arr * 2  # [2, 4, 6, 8]
potencia = arr ** 2  # [1, 4, 9, 16]
division = arr / 2  # [0.5, 1, 1.5, 2]

print(suma)
print(producto)
print(potencia)
print(division)

# Aplicando funciones a un arreglo
array = np.array([1, 4, 9, 16])

raiz_cuadrada = np.sqrt(array)
logaritmo = np.log(array)
seno = np.sin(array)

print(raiz_cuadrada)   
print(logaritmo)      
print(seno)     

# Ejemplos de funciones matemáticas
arr = np.array([0, np.pi/4, np.pi/2, np.pi])

# Aplicar funciones
senos = np.sin(arr)  # [0, 0.7071, 1, 0]
logaritmos = np.log(np.array([1, 2, 3, 4]))
raices = np.sqrt(np.array([1, 4, 9, 16]))  # [1, 2, 3, 4]
print(senos)
print(logaritmos)
print(raices)

# Ejemplos de Funciones Estadísticas
arr = np.array([1, 2, 3, 4, 5])

# Funciones estadísticas
media = np.mean(arr)  # 3.0
mediana = np.median(arr)  # 3.0
desviacion = np.std(arr)  # ~1.41
minimo = np.min(arr)  # 1
maximo = np.max(arr)  # 5
suma = np.sum(arr)  # 15

print(media)
print(mediana)
print(desviacion)
print(minimo)
print(maximo)
print(suma)

# Ejemplos de Agregación
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Suma por filas (axis=1)
row_sums = np.sum(matrix, axis=1)  # [6, 15, 24]

# Suma por columnas (axis=0)
col_sums = np.sum(matrix, axis=0)  # [12, 15, 18]

# Media por filas
row_means = np.mean(matrix, axis=1)  # [2, 5, 8]

print(row_sums)
print(col_sums)
print(row_means)

# Ejemplos de funciones universales
# Unarias: Trabajan con un solo array y devuelven otro del mismo tamaño.
arr = np.array([-1, 0, 1, 2])
abs_values = np.abs(arr)  # [1, 0, 1, 2]
squared = np.square(arr)  # [1, 0, 1, 4]
print(abs_values)
print(squared)

# Binarias: Trabajan con dos arrays (o array + escalar) y operan par a par.
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
maximum = np.maximum(a, b)  # [4, 5, 6]
power = np.power(a, b)  # [1, 32, 729]
print(maximum)
print(power)

# Ejemplos de Álgebra Lineal
from numpy import linalg as LA

A = np.array([[1, 2], [3, 4]])

# Determinante
det_A = LA.det(A)  # -2.0

# Inversa
inv_A = LA.inv(A)

# Autovalores
eigenvalues = LA.eigvals(A)

# Norma
norm = LA.norm(A)