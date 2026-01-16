# 1) Importar la librería Pandas
import pandas as pd

# 2) Crear Series desde listas y diccionarios
serie_lista = pd.Series([10, 20, 30, 40, 50])
print("\n- Serie desde lista:")
print(serie_lista)

serie_dic = pd.Series({"Ana": 90, "Juan": 75, "María": 88})
print("\n- Serie desde diccionario:")
print(serie_dic)


# 3) Personalizar índices y acceder a elementos
serie_idx = pd.Series([10, 20, 30, 40, 50], index=["a", "b", "c", "d", "e"])
print("\n- Serie con índice personalizado:")
print(serie_idx)

print("\n- Acceso por etiqueta (índice): serie_idx['c'] ->", serie_idx["c"])
print("- Acceso por posición (.iloc): serie_idx.iloc[2] ->", serie_idx.iloc[2])

print("\n- Selección múltiple por etiquetas:")
print(serie_idx[["a", "e"]])

print("\n- Slicing por posición (.iloc[1:4]):")
print(serie_idx.iloc[1:4])

print("\n- Filtrado condicional (valores > 25):")
print(serie_idx[serie_idx > 25])


# 4) Crear DataFrames desde diccionarios y listas de listas
df_dic = pd.DataFrame({
    "nombre": ["Ana", "Juan", "María", "Pedro"],
    "edad": [23, 30, 27, 22],
    "ciudad": ["Santiago", "Valparaíso", "Concepción", "La Serena"]
})
print("\n- DataFrame desde diccionario:")
print(df_dic)

df_lista = pd.DataFrame(
    [
        ["Ana", 90],
        ["Juan", 75],
        ["María", 88]
    ],
    columns=["nombre", "nota"]
)
print("\n- DataFrame desde lista de listas:")
print(df_lista)


# 5) Cargar un CSV y mostrar las primeras filas con head()
from pathlib import Path
import pandas as pd

base_dir = Path(__file__).resolve().parent. #esta línea deja en base_dir el directorio donde vive el archivo Python que se está ejecutando, no importa desde dónde lo llames.
csv_path = base_dir / "Titanic-Dataset.csv"

df_csv = pd.read_csv(csv_path)
print(df_csv.head())


# 6) Seleccionar columnas y filas con .loc[] y .iloc[] (usando Titanic)
print(df_csv.head())

# .iloc -> por posición (número de fila/columna)
# Filas 0,1,2 y columnas 0,1,2,3
print(df_csv.iloc[0:3, 0:4])

# .loc -> por etiquetas (índice y nombres de columnas)
# Filas 0 a 2 y columnas específicas
print(df_csv.loc[0:2, ["Survived", "Sex", "Age"]])

# .loc -> condición + columnas (muy típico)
# Pasajeros con Fare > 50
print(df_csv.loc[df_csv["Fare"] > 50, ["Pclass", "Sex", "Age", "Fare"]].head())






