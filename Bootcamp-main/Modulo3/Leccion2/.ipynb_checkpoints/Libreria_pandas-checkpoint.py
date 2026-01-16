##### Creación de una serie
# 1) Desde una lista (lo más típico)
import pandas as pd

s = pd.Series([10, 20, 30, 40, 50])
print(s)

# 2) Desde una lista, pero con índice personalizado
import pandas as pd

s = pd.Series([10, 20, 30], index=["Enero", "Febrero", "Marzo"])
print(s)

# 3) Desde un diccionario (las llaves pasan a ser el índice)
import pandas as pd

s = pd.Series({"Ana": 90, "Juan": 75, "María": 88})
print(s)

#4) Desde un array de NumPy
import pandas as pd
import numpy as np

arr = np.array([1.5, 2.5, 3.5])
s = pd.Series(arr)
print(s)

# 5) Forzar tipo de dato (dtype): Útil si quieres asegurarte de que sea entero, por ejemplo:


s = pd.Series([10, 20, 30], dtype="int64")
print(s)
print(s.dtype)


#### Creación de series con Índices Personalizados
serie_indexada = pd.Series([100,200,300], index=['a','b','c'])
print(serie_indexada)

# Obtención de datos de una serie
serie_indexada = pd.Series([10,20,30,40], index=['a','b','c','d'])
print(serie_indexada['b'])

##### Métodos de acceso a datos en Series
# Serie de ejemplo (con índice "con nombre")
s = pd.Series([10, 20, 30, 40, 50], index=["a", "b", "c", "d", "e"])
print(s)
# 1) Selección por índice (por etiqueta)
print(s["c"])            # 30 (una etiqueta)

print(s[["a", "e"]])     # varias etiquetas
# Si tu índice son palabras (meses, nombres, etc.), esta forma es la más natural.

#2) Método .iloc[] (por posición numérica) Nota: posición (0,1,2,3…), no etiqueta.
print(s.iloc[0])         # primer elemento -> 10
print(s.iloc[3])         # cuarto elemento -> 40
print(s.iloc[[1, 4]])    # posiciones 1 y 4 -> 20 y 50

# 3) Slicing (rangos) 
# Con .iloc (por posición: el final NO se incluye)
print(s.iloc[1:4])       # toma posiciones 1,2,3 -> b,c,d

# Con etiquetas (el final SÍ se incluye)
print(s["b":"d"])        # b, c y d (incluye "d") # Este detalle confunde al principio, pero una vez lo ves, queda.

# 4) Filtrado condicional: Te quedas con valores que cumplen una condición.
print(s[s > 25])         # valores mayores a 25
print(s[(s >= 20) & (s <= 40)])  # entre 20 y 40

##### Operaciones aritméticas con escalares
serie = pd.Series([10,20,30,40], index=['a','b','c','d'])
# Multiplicar todos los elementos por 2
serie_doble = serie * 2

# Sumar 5 a todos los elementos
serie_mas_5 = serie + 5

# Elevar al cuadrado todos los elementos
serie_cuadrado = serie ** 2

####Operaciones entre Series
serie  = pd.Series([10,20,30,40], index=['a','b','c','d'])
serie2 = pd.Series([5,10,15,20], index=['a','b','c','d'])
print(serie + serie2)

### Aplicación de funciones matemáticas
import numpy as np
serie  = pd.Series([10,20,30,40], index=['a','b','c','d'])
# Calcular el logaritmo natural
log_serie = np.log(serie)
# Calcular el valor absoluto
abs_serie = serie.abs()
# Calcular la raíz cuadrada
sqrt_serie = np.sqrt(serie)

# Funciones Personalizadas en Series
serie  = pd.Series([10,20,30,40], index=['a','b','c','d'])
# Definir una función personalizada
def cuadrado_mas_uno(x):
    return x**2 + 1

# Aplicar la función a cada elemento de la Serie
resultado = serie.apply(cuadrado_mas_uno)


### Creación de un DATAFRAME
import pandas as pd
# Crear un DataFrame a partir de un diccionario
data = {
    'Nombre': ['Ana', 'Juan', 'María', 'Carlos'],
    'Edad': [25, 30, 22, 28],
    'Ciudad': ['Madrid', 'Barcelona', 'Sevilla', 'Valencia']
}
df = pd.DataFrame(data)

#Creación de DataFrames desde Archivos
df_csv = pd.read_csv('archivo.csv')
print(df_csv.head())


##### PARTE 2
## Selección de filas o columnas en un DATAFRAME
#Ejemplos con un DataFrame simple (Nombre / Edad)
import pandas as pd

df = pd.DataFrame({
    "Nombre": ["Ana", "Juan", "María", "Pedro", "Luis"],
    "Edad": [23, 30, 27, 22, 35],
    "Ciudad": ["Santiago", "Valpo", "Concepción", "La Serena", "Antofagasta"]
})

#1) Seleccionar una columna
nombres = df["Nombre"]
print(nombres)

#2) Seleccionar varias columnas
datos_personales = df[["Nombre", "Edad"]]
print(datos_personales)

#3) Tip útil: seleccionar columnas y ver las primeras filas
print(df[["Nombre", "Ciudad"]].head(3))

#Selección de Filas en un DataFrame
import pandas as pd

df = pd.DataFrame({
    "Nombre": ["Ana", "Juan", "María", "Pedro", "Luis"],
    "Edad": [23, 30, 27, 22, 35],
    "Ciudad": ["Santiago", "Valparaíso", "Santiago", "La Serena", "Valparaíso"],
    "Activo": [True, False, True, True, False]
})

print(df)
#Selección de elementos en un DataFrame
#Con .loc (por etiqueta)
# Edad de María (fila 2, columna Edad)
edad_maria = df.loc[2, "Edad"]
print(edad_maria)

#Con .iloc (por posición)
# Valor en la fila 2 y columna 1 (Edad)
valor = df.iloc[2, 1]
print(valor)

"""
.loc → nombres / etiquetas
.iloc → posiciones numéricas
"""

##Selección de subconjuntos de datos => Filas + columnas
# Con .loc
# Filas 1 a 3, columnas Nombre y Ciudad
sub_df = df.loc[1:3, ["Nombre", "Ciudad"]]
print(sub_df)

# Con .iloc
# Filas 0 a 2, columnas 0 a 1
sub_df_iloc = df.iloc[0:3, 0:2]
print(sub_df_iloc)

# Selección condicional en un DataFrame
# Filtrar filas según una condición
# Personas mayores de 25 años
mayores_25 = df[df["Edad"] > 25]
print(mayores_25)

# Personas activas
activos = df[df["Activo"] == True]
print(activos)

## Combinación de condiciones => Filtros más complejos

#AND: personas activas y mayores de 25
filtro_and = df[
    (df["Edad"] > 25) & (df["Activo"] == True)
]

print(filtro_and)

# OR: personas de Santiago o Valparaíso
filtro_or = df[
    (df["Ciudad"] == "Santiago") | (df["Ciudad"] == "Valparaíso")
]

print(filtro_or)


### Métodos básicos de exploración 
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "Titanic-Dataset.csv"

df = pd.read_csv(csv_path)

# head() – primeras filas del DataFrame
# Sirve para tener una primera mirada rápida: columnas, tipos de datos “a ojo”, valores faltantes evidentes.
df.head()
df.head(3)

# tail() – últimas filas del DataFrame
# Útil para revisar el final del dataset (a veces hay datos raros al final, o simplemente para confirmar el tamaño).
df.tail()
df.tail(3)

# info() – estructura del DataFrame
# Este es clave pedagógicamente. Aquí se responde:
# ¿Cuántas filas y columnas hay?
# ¿Qué tipo de dato tiene cada columna?
# ¿Hay valores nulos?
df.info()

# describe() – estadísticas descriptivas
# Entrega un resumen estadístico solo de columnas numéricas:
df.describe()
df["Age"].describe()
df[["Age", "Fare"]].describe()

###### Métodos básicos de sumarización 
import pandas as pd

from pathlib import Path

# --- Cargar CSV (misma carpeta que este .py) ---
BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "Titanic-Dataset.csv"

df = pd.read_csv(csv_path)

# MIN y MAX (ej: Age y Fare)
edad_min = df["Age"].min()
edad_max = df["Age"].max()
fare_min = df["Fare"].min()
fare_max = df["Fare"].max()

print("Edad mínima:", edad_min)
print("Edad máxima:", edad_max)
print("Fare mínimo:", fare_min)
print("Fare máximo:", fare_max)

# COUNT (cuenta valores NO nulos por columna)
print("\nCount por columna (no nulos):")
print(df.count())

# MEAN y MEDIAN (promedio y mediana)
edad_mean = df["Age"].mean()
edad_median = df["Age"].median()
fare_mean = df["Fare"].mean()
fare_median = df["Fare"].median()

print("\nEdad promedio:", edad_mean)
print("Edad mediana:", edad_median)
print("Fare promedio:", fare_mean)
print("Fare mediana:", fare_median)

# SUM (suma de una columna numérica)
total_fare = df["Fare"].sum()
print("\nSuma total de Fare:", total_fare)

### Métodos unique, nunique, value_counts
import pandas as pd

from pathlib import Path

# --- Cargar CSV (misma carpeta que este .py) ---
BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "Titanic-Dataset.csv"

df = pd.read_csv(csv_path)

# unique(): valores únicos (ej: Sex y Embarked)
print("Valores únicos en 'Sex':")
print(df["Sex"].unique())

print("\nValores únicos en 'Embarked':")
print(df["Embarked"].unique())

# nunique(): cantidad de valores únicos (ej: Pclass y Embarked)
print("\nCantidad de valores únicos en 'Pclass':", df["Pclass"].nunique())
print("Cantidad de valores únicos en 'Embarked':", df["Embarked"].nunique())

# value_counts(): frecuencia de cada valor (ej: Sex, Pclass, Embarked)
print("\nFrecuencia por 'Sex':")
print(df["Sex"].value_counts())

print("\nFrecuencia por 'Pclass':")
print(df["Pclass"].value_counts())

print("\nFrecuencia por 'Embarked' (incluye NaN):")
print(df["Embarked"].value_counts(dropna=False))

# (Opcional) value_counts en porcentaje
print("\nPorcentaje por 'Sex':")
print(df["Sex"].value_counts(normalize=True) * 100)

### Ejemplo de Análisis con value_counts()
import pandas as pd

df = pd.read_csv("Titanic-Dataset.csv")

# Contar la frecuencia de cada puerto de embarque (Embarked)
embarque = df["Embarked"].value_counts()
print("Frecuencia por Embarked:")
print(embarque)

# Normalizar para obtener porcentajes
porcentajes = df["Embarked"].value_counts(normalize=True) * 100
print("\nPorcentajes por Embarked:")
print(porcentajes)

# Ordenar por frecuencia descendente (value_counts ya viene ordenado, pero lo mostramos igual)
ordenado = df["Embarked"].value_counts().sort_values(ascending=False)
print("\nOrdenado por frecuencia (desc):")
print(ordenado)

### Métodos Adicionales para Exploración de Datos
import pandas as pd

df = pd.read_csv("Titanic-Dataset.csv")

# dtypes: tipos de dato por columna
print("Tipos de dato (dtypes):")
print(df.dtypes)

# shape: dimensiones (filas, columnas)
print("\nDimensión (shape):")
print(df.shape)

# columns: nombres de columnas
print("\nColumnas (columns):")
print(df.columns)

# isnull().sum(): cantidad de nulos por columna
print("\nNulos por columna (isnull().sum()):")
print(df.isnull().sum())


### Métodos de Agrupación
import pandas as pd

df = pd.read_csv("Titanic-Dataset.csv")

# 1) Agrupar por una columna y calcular una media (ej: edad promedio por clase)
edad_prom_por_clase = df.groupby("Pclass")["Age"].mean()
print("Edad promedio por clase (Pclass):")
print(edad_prom_por_clase)

# 2) Agrupar y contar registros (tamaño del grupo)
pasajeros_por_clase = df.groupby("Pclass").size()
print("\nCantidad de pasajeros por clase (Pclass):")
print(pasajeros_por_clase)

# 3) Agrupar y obtener múltiples estadísticas (min, max, mean) de Age por clase
stats_edad_por_clase = df.groupby("Pclass").agg({"Age": ["min", "max", "mean"]})
print("\nEstadísticas de Age por clase (min, max, mean):")
print(stats_edad_por_clase)

# (Opcional) Agrupar por dos columnas: supervivencia por sexo (conteo)
sobrevivencia_por_sexo = df.groupby(["Sex", "Survived"]).size()
print("\nConteo por Sex y Survived:")
print(sobrevivencia_por_sexo)

# (Opcional) Tasa de supervivencia promedio por clase (mean de Survived: 0/1)
tasa_sobrev_por_clase = df.groupby("Pclass")["Survived"].mean()
print("\nTasa de supervivencia por clase (promedio de Survived):")
print(tasa_sobrev_por_clase)


# Operaciones de Unión y Combinación
import pandas as pd

# ----------------------------
# DataFrames de ejemplo
# ----------------------------
df_personas = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "Nombre": ["Ana", "Juan", "María", "Pedro"]
})

df_edades = pd.DataFrame({
    "id": [1, 2, 4, 5],
    "Edad": [23, 30, 27, 40]
})

# ----------------------------
# 1) merge()  -> une por una columna en común (tipo JOIN)
# ----------------------------
merge_inner = pd.merge(df_personas, df_edades, on="id", how="inner")
print("merge INNER (solo ids que están en ambos):")
print(merge_inner)

merge_left = pd.merge(df_personas, df_edades, on="id", how="left")
print("\nmerge LEFT (todos los de df_personas):")
print(merge_left)

# ----------------------------
# 2) concat() -> pega DataFrames por filas (axis=0) o por columnas (axis=1)
# ----------------------------
df_a = pd.DataFrame({"id": [1, 2], "Nombre": ["Ana", "Juan"]})
df_b = pd.DataFrame({"id": [3, 4], "Nombre": ["María", "Pedro"]})

concat_filas = pd.concat([df_a, df_b], axis=0, ignore_index=True)
print("\nconcat por filas (axis=0):")
print(concat_filas)

df_c = pd.DataFrame({"Edad": [23, 30]})
df_d = pd.DataFrame({"Ciudad": ["Santiago", "Valparaíso"]})

concat_columnas = pd.concat([df_a, df_c, df_d], axis=1)
print("\nconcat por columnas (axis=1):")
print(concat_columnas)

# ----------------------------
# 3) join() -> une usando el índice
# ----------------------------
df_personas_idx = df_personas.set_index("id")
df_edades_idx = df_edades.set_index("id")

join_inner = df_personas_idx.join(df_edades_idx, how="inner")
print("\njoin INNER (por índice):")
print(join_inner)

join_left = df_personas_idx.join(df_edades_idx, how="left")
print("\njoin LEFT (por índice):")
print(join_left)


## Manejo de datos faltantes
import pandas as pd

df = pd.read_csv("Titanic-Dataset.csv")

# 1) Detectar valores nulos (True/False por celda)
print(df.isnull().head())

# 2) Contar nulos por columna
print(df.isnull().sum())

# 3) Eliminar filas con al menos un nulo
df_limpio = df.dropna()
print("Filas antes:", df.shape[0], "| Filas después:", df_limpio.shape[0])

# 4) Rellenar TODOS los nulos con un valor específico (ej: 0)
df_relleno_0 = df.fillna(0)

# 5) Rellenar nulos en una columna numérica con la media (ej: Age)
df_age_media = df.copy()
df_age_media["Age"] = df_age_media["Age"].fillna(df_age_media["Age"].mean())

# (Opcional) Rellenar nulos en Embarked con el valor más frecuente (moda)
df_embarked_moda = df.copy()
moda_embarked = df_embarked_moda["Embarked"].mode()[0]
df_embarked_moda["Embarked"] = df_embarked_moda["Embarked"].fillna(moda_embarked)


#### Transformación de Datos
import pandas as pd

df = pd.read_csv("Titanic-Dataset.csv")

# ----------------------------
# 1) apply() -> aplicar una función a una columna
# ----------------------------
df["Age_x2"] = df["Age"].apply(lambda x: x * 2 if pd.notnull(x) else x)

# (opcional) apply() por fila: crear una etiqueta simple según Age
df["Grupo_Edad"] = df["Age"].apply(
    lambda x: "Niño" if pd.notnull(x) and x < 18 else ("Adulto" if pd.notnull(x) else "Desconocido")
)

# ----------------------------
# 2) map() -> mapear valores de una Serie según diccionario
# ----------------------------
df["Sexo_txt"] = df["Sex"].map({"male": "Masculino", "female": "Femenino"})

# ----------------------------
# 3) replace() -> reemplazar valores específicos
# ----------------------------
# Cambiar etiquetas de Embarked (C, Q, S) a nombres más claros
df["Embarked_txt"] = df["Embarked"].replace({"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"})

# ----------------------------
# 4) astype() -> convertir tipo de dato
# ----------------------------
# Pclass como string/categoría para análisis (1,2,3 -> "1","2","3")
df["Pclass_str"] = df["Pclass"].astype(str)

# Ejemplo: Survived a booleano (0/1 -> False/True)
df["Survived_bool"] = df["Survived"].astype(bool)

print(df[["Age", "Age_x2", "Grupo_Edad", "Sex", "Sexo_txt", "Embarked", "Embarked_txt", "Pclass", "Pclass_str", "Survived", "Survived_bool"]].head())


### Ordenación de datos
import pandas as pd

df = pd.read_csv("Titanic-Dataset.csv")

# 1) Ordenar por una columna (Age) ascendente
df_ordenado_edad = df.sort_values("Age", ascending=True)
print(df_ordenado_edad[["Name", "Age", "Sex", "Pclass"]].head(10))

# 2) Ordenar por una columna (Fare) descendente
df_ordenado_fare = df.sort_values("Fare", ascending=False)
print(df_ordenado_fare[["Name", "Fare", "Pclass", "Sex"]].head(10))

# 3) Ordenar por múltiples columnas:
#    Primero por Pclass (asc), luego por Fare (desc)
df_ordenado_multi = df.sort_values(["Pclass", "Fare"], ascending=[True, False])
print(df_ordenado_multi[["Pclass", "Fare", "Name"]].head(10))

# 4) Ordenar por índice
df_ordenado_indice = df.sort_index()
print(df_ordenado_indice.head(5))


### Visualización de Datos con Pandas
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Titanic-Dataset.csv")

# 1) Histograma de edades
df["Age"].plot.hist(bins=20)
plt.title("Distribución de edades")
plt.xlabel("Edad")
plt.ylabel("Frecuencia")
plt.show()

# 2) Gráfico de barras: cantidad de pasajeros por sexo
df["Sex"].value_counts().plot.bar()
plt.title("Cantidad de pasajeros por sexo")
plt.xlabel("Sexo")
plt.ylabel("Cantidad")
plt.show()

# 3) Gráfico de barras: cantidad de pasajeros por clase
df["Pclass"].value_counts().sort_index().plot.bar()
plt.title("Cantidad de pasajeros por clase")
plt.xlabel("Clase")
plt.ylabel("Cantidad")
plt.show()

# 4) Diagrama de dispersión: Edad vs Tarifa
df.plot.scatter(x="Age", y="Fare")
plt.title("Relación entre Edad y Tarifa")
plt.xlabel("Edad")
plt.ylabel("Tarifa")
plt.show()

# 5) Gráfico de líneas: promedio de tarifa por clase
fare_promedio = df.groupby("Pclass")["Fare"].mean()
fare_promedio.plot.line(marker="o")
plt.title("Tarifa promedio por clase")
plt.xlabel("Clase")
plt.ylabel("Tarifa promedio")
plt.show()

## Manejo de Series Temporales
# Crear un rango de fechas
fechas = pd.date_range(start='2023-01-01', periods=10, freq='D')

# Convertir columna a tipo datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Extraer componentes de fecha
df['Año'] = df['Fecha'].dt.year
df['Mes'] = df['Fecha'].dt.month

# Remuestreo de datos temporales
df_mensual = df.resample('M', on='Fecha').mean()











