# Script: dataset_ventas_parquet_csv.py
# Objetivo:
# 1. Crear un DataFrame de ventas de ejemplo en PySpark.
# 2. Guardarlo en formato Parquet y CSV.
# 3. Leer ambos formatos para verificar.
# 4. Crear vistas temporales para usar en Spark SQL.

# Paso 1: importar librerías principales
from pyspark.sql import SparkSession

# Creamos la sesión de Spark (puedes ajustar el master según tu entorno)
spark = (
    SparkSession.builder
    .appName("DatasetVentasEjemplo")
    .getOrCreate()
)

# Paso 2: definir los datos de ejemplo en una lista de tuplas
ventas_data = [
    (1, "2026-01-01", "Electronica", 3, 1200.0),
    (2, "2026-01-02", "Hogar", 1, 300.0),
    (3, "2026-01-03", "Electronica", 2, 800.0),
    (4, "2026-01-04", "Deportes", 5, 500.0),
    (5, "2026-01-05", "Hogar", 4, 900.0),
]

# Definimos los nombres de las columnas
cols = ["id_venta", "fecha", "categoria", "cantidad", "monto"]

# Paso 3: crear el DataFrame a partir de la lista de tuplas
ventas_df = spark.createDataFrame(ventas_data, cols)

# Inspeccionamos los datos y el esquema para validar el DataFrame
ventas_df.show()
ventas_df.printSchema()

# Paso 4: definir la ruta base donde guardaremos los archivos
base_path = "data/ventas_spark"

# Paso 5: guardar el DataFrame en formato Parquet
# mode("overwrite") permite sobrescribir si la carpeta ya existe
ventas_df.write.mode("overwrite").parquet(base_path + "/parquet")

# Paso 6: guardar el DataFrame en formato CSV con cabecera
ventas_df.write \
    .mode("overwrite") \
    .option("header", True) \
    .option("sep", ",") \
    .csv(base_path + "/csv")

# Paso 7: leer nuevamente el Parquet para verificar
parquet_df = spark.read.parquet(base_path + "/parquet")
parquet_df.show()
parquet_df.printSchema()

# Paso 8: leer nuevamente el CSV para verificar
csv_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(base_path + "/csv")
)

csv_df.show()
csv_df.printSchema()

# Paso 9: comparar rápidamente el número de filas
print("Filas en Parquet:", parquet_df.count())
print("Filas en CSV:", csv_df.count())

# Paso 10: crear vistas temporales para usar en Spark SQL
parquet_df.createOrReplaceTempView("ventas_parquet")
csv_df.createOrReplaceTempView("ventas_csv")

# Ejemplo de consulta SQL 1: agregación por categoría
consulta1 = spark.sql("""
    SELECT categoria, SUM(monto) AS total_monto
    FROM ventas_parquet
    GROUP BY categoria
""")
consulta1.show()

# Ejemplo de consulta SQL 2: filtro por categoría y orden por fecha
consulta2 = spark.sql("""
    SELECT *
    FROM ventas_csv
    WHERE categoria = 'Electronica'
    ORDER BY fecha
""")
consulta2.show()
