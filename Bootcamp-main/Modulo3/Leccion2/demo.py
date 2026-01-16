import pandas as pd

df = pd.DataFrame({
    "Nombre": ["Ana", "Juan", "María", "Pedro", "Luis"],
    "Edad": [23, 30, 27, 22, 35],
    "Ciudad": ["Santiago", "Valpo", "Concepción", "La Serena", "Antofagasta"]
})

#1) Seleccionar una columna
nombres = df["Nombre"]
print(nombres)