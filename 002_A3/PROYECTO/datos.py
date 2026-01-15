"""
Proyecto Módulo 4 - Preparación de datos con Python
Flujo completo: NumPy + Pandas + obtención, limpieza, wrangling y agrupamiento.
"""

import numpy as np
import pandas as pd

# =========================
# LECCIÓN 1 - NumPy
# =========================

# 1. Generar datos ficticios de clientes y transacciones usando NumPy
np.random.seed(10)

num_clientes = 10

ids = np.arange(1, num_clientes + 1)
edades = np.random.randint(18, 70, size=num_clientes)
ciudades = np.random.choice([
    "Buenos Aires", "Córdoba", "Rosario", "Mendoza", "La Plata",
    "Salta", "Tucumán", "Santa Fe", "Neuquén", "Bahía Blanca"
], size=num_clientes)

# Total compras entre 0 y 20
compras = np.random.randint(0, 21, size=num_clientes)
# Monto promedio de compra entre 100 y 800
monto_promedio = np.random.uniform(100, 800, size=num_clientes)
# Monto total aproximado
monto_total = compras * monto_promedio

# 2. Crear un array base
clientes_numpy = np.column_stack([ids, edades, compras, monto_total])

# 3. Operaciones básicas
cantidad_clientes = clientes_numpy.shape[0]
edad_media = edades.mean()
compras_totales = compras.sum()

# 4. Guardar datos en .npy
np.save("D:/000_ANALISTA DATOS , TALENTO DIGITAL/002_A3/PROYECTO/clientes_numpy.npy", clientes_numpy)

# =========================
# LECCIÓN 2 - Pandas (desde NumPy)
# =========================

# 1. Leer los datos preparados en NumPy y convertirlos en DataFrame
clientes_numpy_cargado = np.load("D:/000_ANALISTA DATOS , TALENTO DIGITAL/002_A3/PROYECTO/clientes_numpy.npy")

df_numpy = pd.DataFrame(
    clientes_numpy_cargado,
    columns=["ID", "Edad", "Total_Compras", "Monto_Total"]
)

# 2. Exploración inicial (puedes imprimir si quieres)
head_df = df_numpy.head()
tail_df = df_numpy.tail()
describe_df = df_numpy.describe()

# Ejemplos de filtros condicionales
mayores_30 = df_numpy[df_numpy["Edad"] > 30]
con_mas_de_5_compras = df_numpy[df_numpy["Total_Compras"] > 5]

# 3. Guardar DataFrame preliminar
df_numpy.to_csv("D:/000_ANALISTA DATOS , TALENTO DIGITAL/002_A3/PROYECTO/clientes_desde_numpy.csv", index=False)

# =========================
# LECCIÓN 3 - Obtención de datos desde archivos
# =========================

# 1. Cargar el CSV generado en la Lección 2
df_base = pd.read_csv("D:/000_ANALISTA DATOS , TALENTO DIGITAL/002_A3/PROYECTO/clientes_desde_numpy.csv")

# 2. Incorporar nuevas fuentes de datos: tus archivos de e-commerce
df_ecom_csv = pd.read_csv("D:/000_ANALISTA DATOS , TALENTO DIGITAL/002_A3/PROYECTO/clientes_ecommerce.csv")
df_ecom_xlsx = pd.read_excel("D:/000_ANALISTA DATOS , TALENTO DIGITAL/002_A3/PROYECTO/clientes_ecommerce.xlsx")

# 3. Opcional: leer una tabla desde la web
try:
    tablas_web = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_cities_in_Argentina_by_population"
    )
    tabla_ciudades = tablas_web[0]
except Exception:
    tabla_ciudades = pd.DataFrame()

# 4. Unificar fuentes de datos
df_ecom_csv["ID"] = df_ecom_csv["ID"].astype(int)
df_base["ID"] = df_base["ID"].astype(int)

df_unificado = pd.merge(
    df_base,
    df_ecom_csv[["ID", "Nombre", "Ciudad"]],
    on="ID",
    how="left"
)

df_unificado.to_csv("D:/000_ANALISTA DATOS , TALENTO DIGITAL/002_A3/PROYECTO/dataset_consolidado.csv", index=False)

# =========================
# LECCIÓN 4 - Valores perdidos y outliers
# =========================

# 1. Identificar valores nulos
nulos_por_columna = df_unificado.isna().sum()

# 2. Imputar Edad faltante con la media
if "Edad" in df_unificado.columns:
    df_unificado["Edad"] = df_unificado["Edad"].fillna(df_unificado["Edad"].mean())

# 3. Detectar outliers en Monto_Total con IQR
q1 = df_unificado["Monto_Total"].quantile(0.25)
q3 = df_unificado["Monto_Total"].quantile(0.75)
iqr = q3 - q1

limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr

outliers = df_unificado[
    (df_unificado["Monto_Total"] < limite_inferior)
    | (df_unificado["Monto_Total"] > limite_superior)
]

# Decisión: recortar valores al rango permitido
df_unificado["Monto_Total"] = df_unificado["Monto_Total"].clip(
    lower=limite_inferior,
    upper=limite_superior
)

df_limpio = df_unificado.copy()
df_limpio.to_csv("D:/000_ANALISTA DATOS , TALENTO DIGITAL/002_A3/PROYECTO/dataset_limpio.csv", index=False)

# =========================
# LECCIÓN 5 - Data Wrangling
# =========================

# 1. Tomar DataFrame limpio
df_wrangle = pd.concat([df_limpio, df_limpio.iloc[:3]], ignore_index=True)

# 2. Eliminar registros duplicados
df_wrangle = df_wrangle.drop_duplicates()

# 3. Transformar tipos de datos
if "Ciudad" in df_wrangle.columns:
    df_wrangle["Ciudad"] = df_wrangle["Ciudad"].astype("category")

# 4. Crear nuevas columnas calculadas
df_wrangle["Ticket_Promedio"] = df_wrangle.apply(
    lambda row: row["Monto_Total"] / row["Total_Compras"] if row["Total_Compras"] > 0 else 0,
    axis=1
)

bins = [0, 1000, 3000, 10000]
labels = ["Bajo", "Medio", "Alto"]
df_wrangle["Segmento_Monto"] = pd.cut(
    df_wrangle["Monto_Total"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

# Normalización simple (min-max) de Monto_Total
min_monto = df_wrangle["Monto_Total"].min()
max_monto = df_wrangle["Monto_Total"].max()

if max_monto > min_monto:
    df_wrangle["Monto_Normalizado"] = (
        df_wrangle["Monto_Total"] - min_monto
    ) / (max_monto - min_monto)
else:
    df_wrangle["Monto_Normalizado"] = 0

df_wrangle.to_csv("D:/000_ANALISTA DATOS , TALENTO DIGITAL/002_A3/PROYECTO/dataset_wrangle.csv", index=False)

# =========================
# LECCIÓN 6 - Agrupamiento y pivoteo
# =========================

# 1. Tomar DataFrame final (df_wrangle)

# 2. Agrupamiento por ciudad
# Observed True o False si quieres mantener 100% el comportamiento actual
if "Ciudad" in df_wrangle.columns:
    agrupado_ciudad = df_wrangle.groupby("Ciudad", observed=True ).agg({
        "Total_Compras": "sum",
        "Monto_Total": ["sum", "mean"],
        "Ticket_Promedio": "mean"
    })
else:
    agrupado_ciudad = pd.DataFrame()

# 3. Pivot por Ciudad y Segmento_Monto
if "Ciudad" in df_wrangle.columns and "Segmento_Monto" in df_wrangle.columns:
    tabla_pivot = df_wrangle.pivot_table(
        index="Ciudad",
        columns="Segmento_Monto",
        values="Monto_Total",
        aggfunc="mean",
        observed=True
    )
else:
    tabla_pivot = pd.DataFrame()

# 4. Melt: volver a formato largo
if not tabla_pivot.empty:
    tabla_melt = tabla_pivot.reset_index().melt(
        id_vars="Ciudad",
        var_name="Segmento_Monto",
        value_name="Monto_Promedio"
    )
else:
    tabla_melt = pd.DataFrame()

# 5. Exportar dataset final
df_wrangle.to_csv("D:/000_ANALISTA DATOS , TALENTO DIGITAL/002_A3/PROYECTO/dataset_final.csv", index=False)
df_wrangle.to_excel("D:/000_ANALISTA DATOS , TALENTO DIGITAL/002_A3/PROYECTO/dataset_final.xlsx", index=False)

if __name__ == "__main__":
    print("\n----Flujo de preparación de datos ejecutado correctamente.----")
