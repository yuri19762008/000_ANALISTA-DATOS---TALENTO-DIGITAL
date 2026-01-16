import pandas as pd
from pathlib import Path

# --- Cargar CSV (misma carpeta que este .py) ---
BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "Titanic-Dataset.csv"

df = pd.read_csv(csv_path)

print("\n✅ Dataset cargado")
print("Shape:", df.shape)

# ------------------------------------------
# 1) Seleccionar columnas y filas con .loc[] y .iloc[]
# ------------------------------------------
print("\n--- 1) Selección con .loc y .iloc ---")

# 1) .iloc -> por posición (números)
# Filas 0 a 2 (3 filas) y columnas 0 a 3 (4 columnas)
print(df.iloc[0:3, 0:4])

# 2) .loc -> por nombre (etiquetas)
# Filas 0 a 2 y columnas específicas por nombre
print(df.loc[0:2, ["Survived", "Sex", "Age"]])

# 3) .loc -> filtrando filas con condición + columnas
# Pasajeros mujeres y mostrar solo Sex, Age y Fare
print(df.loc[df["Sex"] == "female", ["Sex", "Age", "Fare"]].head())


# ------------------------------------------
# 2) Filtrar datos usando & y |
# ------------------------------------------
print("\n--- 2) Filtros con & y | ---")

# AND: mujeres Y 1ra clase
filtro_and = (df["Sex"] == "female") & (df["Pclass"] == 1)
print(df.loc[filtro_and, ["Survived", "Pclass", "Sex", "Age", "Fare"]].head())

# OR: 1ra clase O sobrevivieron
filtro_or = (df["Pclass"] == 1) | (df["Survived"] == 1)
print(df.loc[filtro_or, ["Survived", "Pclass", "Sex", "Age", "Fare"]].head())

# AND con rango: edad entre 18 y 30 (incluye extremos)
filtro_edad = (df["Age"] >= 18) & (df["Age"] <= 30)
print(df.loc[filtro_edad, ["Sex", "Age", "Fare"]].head())


# ------------------------------------------
# 3) Métodos básicos de exploración
# ------------------------------------------
print("\n--- 3) Exploración rápida ---")
print("\nPrimeras 5 filas (head):")
print(df.head())

print("\nÚltimas 5 filas (tail):")
print(df.tail())

print("\nInfo del DataFrame (info):")
df.info()

print("\nEstadísticas descriptivas (describe):")
print(df.describe())

# ------------------------------------------
# 4) Estadísticas básicas: mean(), median(), sum()
# ------------------------------------------
print("\n--- 4) Estadísticas básicas ---")

if "Age" in df.columns:
    print("\nEdad:")
    print("mean  :", df["Age"].mean())
    print("median:", df["Age"].median())

if "Fare" in df.columns:
    print("\nTarifa (Fare):")
    print("mean  :", df["Fare"].mean())
    print("median:", df["Fare"].median())
    print("sum   :", df["Fare"].sum())

# Ejemplo adicional: total de sobrevivientes (si Survived es 0/1)
if "Survived" in df.columns:
    print("\nSobrevivientes (suma de Survived):", df["Survived"].sum())

# ------------------------------------------
# 5) Analizar valores únicos con value_counts()
# ------------------------------------------
print("\n--- 5) value_counts() ---")

if "Sex" in df.columns:
    print("\nFrecuencia por sexo:")
    print(df["Sex"].value_counts())

if "Pclass" in df.columns:
    print("\nFrecuencia por clase (Pclass):")
    print(df["Pclass"].value_counts().sort_index())

# Ejemplo con normalize=True (porcentajes)
if "Embarked" in df.columns:
    print("\nFrecuencia por puerto de embarque (Embarked) - porcentajes:")
    print(df["Embarked"].value_counts(normalize=True, dropna=False))
