import numpy as np

# 1) Vector 0..99
v = np.arange(100)

# 2) Matriz 10x10 a partir del vector
A = v.reshape(10, 10)

# 3) Transpuesta
A_T = A.T

# 4) Multiplicar cada valor por 2 (vectorizado)
A_x2 = A * 2

# 5) Diagonal principal
diag_A = np.diag(A)

# 6) Matriz identidad del mismo tamaño
I = np.eye(10)

# 7) Multiplicación matricial con @ entre la original y la identidad
A_I = A @ I

# ---- Mostrar resultados (opcional) ----
print("Vector v (0..99):\n", v)
print("\nMatriz A (10x10):\n", A)
print("\nTranspuesta A_T:\n", A_T)
print("\nA * 2 (A_x2):\n", A_x2)
print("\nDiagonal principal (diag_A):\n", diag_A)
print("\nIdentidad I:\n", I)
print("\nA @ I (A_I):\n", A_I)

# (Opcional) Validación rápida:
print("\n¿A @ I es igual a A?:", np.allclose(A_I, A))