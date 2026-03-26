# Script: dataset_ventas_parquet_csv_advanced.py
# Objetivo:
# 1. Cargar un dataset de ventas.
# 2. Guardarlo en Parquet y CSV.
# 3. Ejecutar tres consultas avanzadas con explain().
# 4. Mostrar brevemente cómo Catalyst optimiza los planes.

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, expr

# -------------------------------------------------------------------
# Paso 1: crear sesión Spark
# -------------------------------------------------------------------
spark = (
    SparkSession.builder
    .appName("DatasetVentasEjemploAvanzado")
    .getOrCreate()
)

# -------------------------------------------------------------------
# Paso 2: cargar dataset (puede ser tu CSV grande)
# -------------------------------------------------------------------
# Si ya tienes un CSV grande, cambia la ruta aquí:
input_csv_path = "data/ventas_big.csv"

ventas_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(input_csv_path)
)

print("Esquema original del dataset:")
ventas_df.printSchema()

# -------------------------------------------------------------------
# Paso 3: guardar en Parquet y CSV (misma lógica que antes)
# -------------------------------------------------------------------
base_path = "data/ventas_spark_advanced"

ventas_df.write.mode("overwrite").parquet(base_path + "/parquet")

ventas_df.write \
    .mode("overwrite") \
    .option("header", True) \
    .option("sep", ",") \
    .csv(base_path + "/csv")

# Leer de nuevo ambos formatos para trabajar con ellos
parquet_df = spark.read.parquet(base_path + "/parquet")

csv_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(base_path + "/csv")
)

print("Filas en Parquet:", parquet_df.count())
print("Filas en CSV:", csv_df.count())

parquet_df.createOrReplaceTempView("ventas_parquet")
csv_df.createOrReplaceTempView("ventas_csv")

# -------------------------------------------------------------------
# CONSULTA 1:
# Filtros y ordenamientos encadenados + explain()
# -------------------------------------------------------------------
print("\n=== CONSULTA 1: filtros + orden ===")

consulta1_df = (
    parquet_df
    .filter(col("categoria") == "Electronica")
    .filter(col("monto") > 500)
    .orderBy(col("fecha").asc(), col("monto").desc())
)

print("\nPlan de ejecución (CONSULTA 1):")
consulta1_df.explain(mode="extended")  # lógico + físico [web:61][web:62]

print("\nResultado de CONSULTA 1:")
consulta1_df.show(10)

# -------------------------------------------------------------------
# CONSULTA 2:
# Agregaciones con funciones estadísticas + explain()
# -------------------------------------------------------------------
print("\n=== CONSULTA 2: agregaciones ===")

consulta2_df = (
    parquet_df
    .groupBy("categoria")
    .agg(
        sum("monto").alias("total_monto"),
        avg("monto").alias("monto_promedio"),
        count("*").alias("num_ventas")
    )
    .orderBy(col("total_monto").desc())
)

print("\nPlan de ejecución (CONSULTA 2):")
consulta2_df.explain(mode="extended")  # [web:45][web:61]

print("\nResultado de CONSULTA 2:")
consulta2_df.show()

# -------------------------------------------------------------------
# CONSULTA 3:
# Join entre DataFrames + selectExpr + explain()
# -------------------------------------------------------------------
print("\n=== CONSULTA 3: join + selectExpr ===")

# Supongamos una segunda tabla de categorías (puedes ajustarla a tu caso)
data_categorias = [
    ("Electronica", "Alta"),
    ("Hogar", "Media"),
    ("Deportes", "Media"),
    ("Juguetes", "Baja"),
]
cols_categorias = ["categoria", "prioridad"]

categorias_df = spark.createDataFrame(data_categorias, cols_categorias)

categorias_df.createOrReplaceTempView("dim_categoria")

consulta3_df = (
    parquet_df.alias("v")
    .join(categorias_df.alias("c"), col("v.categoria") == col("c.categoria"), "left")
    .selectExpr(
        "v.id_venta",
        "v.fecha",
        "v.categoria",
        "c.prioridad as prioridad_categoria",
        "v.cantidad",
        "v.monto",
        "monto * cantidad as ingreso_total"
    )
)

print("\nPlan de ejecución (CONSULTA 3):")
consulta3_df.explain(mode="extended")  # [web:56][web:61]

print("\nResultado de CONSULTA 3:")
consulta3_df.show(10)

# -------------------------------------------------------------------
# Comentario corto sobre Catalyst y Tungsten (texto en logs)
# -------------------------------------------------------------------
print("""
=== Comentario sobre Catalyst y Tungsten ===
- Catalyst toma las operaciones lógicas (filter, groupBy, join, selectExpr)
  y genera un plan lógico optimizado: reordena filtros (predicate pushdown),
  elimina columnas no usadas y elige estrategias de join/agregación eficientes. [web:61][web:69]
- Tungsten ejecuta el plan físico optimizado usando representación binaria en memoria,
  administración eficiente de memoria y generación de código (whole-stage codegen)
  para aprovechar mejor CPU y cachés. [web:64][web:66]
""")
