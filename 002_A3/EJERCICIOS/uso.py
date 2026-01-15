import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Crear una máscara: valores mayores que 25
mask = arr > 25        # [False False  True  True  True]

# Usar la máscara para filtrar
mayores_25 = arr[mask] # [30 40 50]

print(mask)
print(mayores_25)
