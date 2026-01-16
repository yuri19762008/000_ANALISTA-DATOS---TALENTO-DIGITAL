import pandas as pd
from pathlib import Path

# -----------------------------
# 0) Cargar Titanic (base para toda la consigna)
# -----------------------------
base_dir = Path(__file__).resolve().parent
csv_path = base_dir / "Titanic-Dataset.csv"

df = pd.read_csv(csv_path)
print("✅ Titanic cargado. Filas/Columnas:", df.shape)
print(df.head())

# -----------------------------
# 1) Crear una Serie (mín. 5 elementos) con índice personalizado
# -----------------------------
# Ejemplo: tarifas de 5 pasajeros (Fare) con índice como PassengerId
# Si tu CSV no tiene PassengerId, puedes usar el índice normal df.index
serie_fare = pd.Series(
    df.loc[0:4, "Fare"].values,
    index=df.loc[0:4, "PassengerId"].values
)

print("\n1) Serie creada (Fare de 5 pasajeros, índice = PassengerId):")
print(serie_fare)

# -----------------------------
# 2) Operación aritmética + filtro
# -----------------------------
# Ejemplo: aplicar “+10” a la tarifa (operación simple)
serie_fare_mas10 = serie_fare + 10
print("\n2.1) Operación aritmética (Fare + 10):")
print(serie_fare_mas10)

# Filtro: tarifas mayores a 20
print("\n2.2) Filtro (Fare > 20):")
print(serie_fare[serie_fare > 20])

# -----------------------------
# 3) Crear un DataFrame desde un diccionario (mín. 3 columnas y 5 filas)
# -----------------------------
# Ejemplo: armar un “mini Titanic” con 5 filas
df_mini = pd.DataFrame({
    "Nombre": df.loc[0:4, "Name"].values,
    "Sexo": df.loc[0:4, "Sex"].values,
    "Edad": df.loc[0:4, "Age"].values
})

print("\n3) DataFrame desde diccionario (5 filas, 3 columnas):")
print(df_mini)

# -----------------------------
# 4) Seleccionar una columna, una fila y un subconjunto de datos
# -----------------------------
print("\n4.1) Seleccionar una columna (Age):")
print(df["Age"].head())

print("\n4.2) Seleccionar una fila (fila 0) con .iloc:")
print(df.iloc[0])

print("\n4.3) Subconjunto: filas 0 a 4 y columnas Name, Sex, Age:")
print(df.loc[0:4, ["Name", "Sex", "Age"]])

# (Extra útil) Subconjunto con filtro real de Titanic:
print("\n4.4) Subconjunto filtrado: sobrevivieron (Survived == 1), columnas Name, Sex, Age:")
print(df.loc[df["Survived"] == 1, ["Name", "Sex", "Age"]].head())

# -----------------------------
# 5) Cargar un CSV y mostrar primeras y últimas 5 filas
# -----------------------------
print("\n5) Primeras 5 filas (head):")
print(df.head())

print("\n5) Últimas 5 filas (tail):")
print(df.tail())
