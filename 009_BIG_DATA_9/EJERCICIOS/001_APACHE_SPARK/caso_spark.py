# Caso de uso Apache Spark Streaming – Detección de fraude en banco digital
#
# Este script está pensado como PLANTILLA TEÓRICA para que la copies
# y pegues en un notebook Jupyter o la adaptes a tu contexto.
# Incluye secciones que puedes convertir en celdas markdown y código.

"""
## 1. Contexto y problema

1. Un banco digital procesa miles de transacciones por minuto (pagos, transferencias, retiros).
2. Con análisis batch tradicional, muchas operaciones fraudulentas se detectan tarde.
3. Objetivo: usar Apache Spark Streaming para detectar patrones sospechosos casi en tiempo real.

Idea clave: procesar el flujo de transacciones en movimiento, aplicando reglas simples y/o modelos de ML.
"""

# 2. Ejemplo de estructura de una transacción (solo ilustrativo)
ejemplo_transaccion = {
    "id_transaccion": "T12345",
    "id_cliente": "C001",
    "tarjeta": "4111-****-****-1234",
    "monto": 250000.0,
    "pais": "CL",
    "timestamp": "2026-03-12T18:00:00Z"
}

for k, v in ejemplo_transaccion.items():
    print(f"{k}: {v}")

"""
## 3. Arquitectura lógica (para celda markdown)

Capas principales de la solución:

- Ingesta: Kafka recibe transacciones del backend de pagos.
- Procesamiento en tiempo real: Spark Streaming consume desde Kafka y aplica lógica de detección.
- Salida: las transacciones sospechosas se envían a otro tópico Kafka, una base de datos o sistema de monitoreo.

Flujo general:
1) Backend -> Kafka (tópico `transacciones`).
2) Spark Streaming -> lee micro-lotes desde `transacciones`.
3) Aplica reglas / modelo ML.
4) Publica resultados en `alertas_fraude` o los guarda en una BD.
"""

"""
## 4. Pseudocódigo PySpark de detección simple basada en reglas

A continuación se muestra un pseudocódigo (no ejecutarlo tal cual sin adaptar):

- Lee desde Kafka.
- Parsea JSON.
- Marca como sospechosas las transacciones con monto muy alto.
- Envía las sospechosas a otro sink (consola, Kafka, BD).
"""

# IMPORTANTE: este fragmento es pseudocódigo, ajústalo a tu entorno real
spark_code_streaming_fraude = '''
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# 1. Crear la sesión de Spark
spark = SparkSession.builder.appName("FraudeStreamingBanco").getOrCreate()

# 2. Definir el esquema de las transacciones
schema = StructType([
    StructField("id_transaccion", StringType()),
    StructField("id_cliente", StringType()),
    StructField("tarjeta", StringType()),
    StructField("monto", DoubleType()),
    StructField("pais", StringType()),
    StructField("timestamp", TimestampType())
])

# 3. Leer el stream desde Kafka
df_raw = spark.readStream.format("kafka")\\
    .option("kafka.bootstrap.servers", "kafka:9092")\\
    .option("subscribe", "transacciones")\\
    .load()

# 4. Parsear el JSON del campo 'value'
df_transacciones = df_raw.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# 5. Regla simple: marcar transacciones con monto > 1.000.000 como sospechosas
df_flag = df_transacciones.withColumn(
    "es_sospechosa",
    when(col("monto") > 1000000, True).otherwise(False)
)

# 6. Filtrar solo sospechosas
df_alertas = df_flag.filter(col("es_sospechosa") == True)

# 7. Para simplificar, mostramos las alertas por consola
query = df_alertas.writeStream\\
    .outputMode("append")\\
    .format("console")\\
    .start()

query.awaitTermination()
'''

print(spark_code_streaming_fraude)

"""
## 5. Extensión a Machine Learning (para markdown)

1. Entrenar un modelo de clasificación (fraude / no fraude) con Spark MLlib en modo batch.
2. Guardar el modelo entrenado en disco o en HDFS/S3.
3. Cargar el modelo dentro del job de streaming y aplicarlo sobre cada transacción o sobre features agregadas.

Este .py te sirve como guion: cada bloque comentado puede ser una celda markdown en un notebook, y las partes de código puedes ejecutarlas (adaptando rutas, tópicos Kafka, etc.).
"""
