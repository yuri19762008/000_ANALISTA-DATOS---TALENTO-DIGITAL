import pandas as pd
from pathlib import Path

# 1) Importar Pandas y cargar los datos
BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "Titanic-Dataset.csv"

df = pd.read_csv(csv_path)

print("\n✅ Dataset cargado")
print("Shape:", df.shape)

# 2) Explorar con head(), tail(), info()
print("\n--- head() ---")
print(df.head())

print("\n--- tail() ---")
print(df.tail())

print("\n--- info() ---")
df.info()

# 2) Seleccionar un subconjunto de columnas y filas
cols = ["Survived", "Pclass", "Sex", "Age", "Fare", "Embarked"]


# 3) Aplicar filtros condicionales simples y combinados
print("\n--- Filtros ---")

# Filtro simple: mujeres
if "Sex" in df.columns:
    solo_mujeres = df[df["Sex"] == "female"]
    print("\nFiltro simple: Sex == 'female' (5 filas):")
    print(solo_mujeres.head())

# Filtro simple: tarifa alta
df_fare = df[df["Fare"] > 50]
print(df_fare.head())

# 2) Dos condiciones (AND): mujeres y 1ra clase
df_female_1st = df[(df["Sex"] == "female") & (df["Pclass"] == 1)]
print(df_female_1st[["Survived", "Pclass", "Sex", "Age", "Fare"]].head())

# 3) Dos condiciones (OR): 1ra clase o sobrevivieron
df_1st_or_surv = df[(df["Pclass"] == 1) | (df["Survived"] == 1)]
print(df_1st_or_surv[["Survived", "Pclass", "Sex", "Age", "Fare"]].head())

# 4) Con rango: edades entre 18 y 30
df_18_30 = df[(df["Age"] >= 18) & (df["Age"] <= 30)]
print(df_18_30[["Sex", "Age", "Fare"]].head())

# 4) Resumen con describe()
print("\n--- describe() (numéricas) ---")
print(df.describe())

# Conteo por sexo
print(df["Sex"].value_counts())

# Conteo por clase
print(df["Pclass"].value_counts())

# Promedio de edad por sexo
edad_por_sexo = df.groupby("Sex")["Age"].mean()
print(edad_por_sexo)

# Promedio de tarifa por clase
fare_por_clase = df.groupby("Pclass")["Fare"].mean()
print(fare_por_clase)


# 5) Guardar resultados en nuevos CSV
out_dir = BASE_DIR / "outputs"
out_dir.mkdir(exist_ok=True)

# Guardar filtros
if "Sex" in df.columns:
    solo_mujeres.to_csv(out_dir / "titanic_solo_mujeres.csv", index=False)

# Guardar agrupaciones
if {"Pclass", "Fare"}.issubset(df.columns):
    fare_por_clase.to_csv(out_dir / "titanic_fare_promedio_por_clase.csv")

