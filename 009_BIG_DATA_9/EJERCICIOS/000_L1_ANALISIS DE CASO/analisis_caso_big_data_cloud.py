# Análisis de Caso – Big Data (MarketTrend S.A.)
# Arquitectura Big Data en la nube (data lake en S3)


# 1. Análisis de la situación y las 5V del Big Data
#   - Volumen: gran cantidad de datos desde múltiples fuentes.
#   - Velocidad: datos generados de forma continua y necesidad de casi tiempo real.
#   - Variedad: datos estructurados, semiestructurados y no estructurados.
#   - Veracidad: calidad y confiabilidad de datos (ruido, errores, bots).
#   - Valor: uso de datos para decisiones estratégicas y recomendaciones.


# 2. Arquitectura Big Data en la nube por capas:
#   1) Ingesta (streaming y batch) con Kafka y procesos ETL.
#   2) Data lake en S3 organizado en zonas raw, clean y curated.
#   3) Procesamiento batch y streaming con Apache Spark.
#   4) Capa de analítica y consumo (BI y ML).


# Definición ilustrativa de fuentes de datos (diccionarios Python)
fuentes_streaming = {
    'redes_sociales': {
        'tipo': 'streaming',
        'tecnologia_ingesta': 'Kafka',
        'topico_kafka': 'eventos_redes_sociales'
    },
    'app_movil': {
        'tipo': 'streaming',
        'tecnologia_ingesta': 'Kafka',
        'topico_kafka': 'eventos_app_movil'
    }
}


fuentes_batch = {
    'registros_compras': {
        'tipo': 'batch',
        'formato_archivo': 'parquet',
        'frecuencia': 'diaria'
    },
    'encuestas_online': {
        'tipo': 'batch',
        'formato_archivo': 'csv',
        'frecuencia': 'semanal'
    }
}


print('Fuentes en streaming:', fuentes_streaming)
print('Fuentes batch:', fuentes_batch)


# Estructura ilustrativa de un data lake en S3
data_lake_s3 = {
    'raw': {
        'redes_sociales': 's3://markettrend-datalake/raw/redes_sociales/',
        'app_movil': 's3://markettrend-datalake/raw/app_movil/',
        'registros_compras': 's3://markettrend-datalake/raw/registros_compras/',
        'encuestas': 's3://markettrend-datalake/raw/encuestas/'
    },
    'clean': {
        'interacciones': 's3://markettrend-datalake/clean/interacciones/',
        'compras': 's3://markettrend-datalake/clean/compras/',
        'clientes': 's3://markettrend-datalake/clean/clientes/'
    },
    'curated': {
        'segmentos_clientes': 's3://markettrend-datalake/curated/segmentos_clientes/',
        'features_ml': 's3://markettrend-datalake/curated/features_ml/'
    }
}


for zona, rutas in data_lake_s3.items():
    print(f'Zona {zona}:')
    for nombre, ruta in rutas.items():
        print(f'  - {nombre}: {ruta}')


# A continuación se incluyen cadenas con pseudocódigo PySpark para batch y streaming.
# Estos fragmentos sirven como referencia conceptual; no se ejecutan directamente en este script.


spark_code_batch = '''
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName('MarketTrendBatch').getOrCreate()

# Leer datos de compras (zona clean)
df_compras = spark.read.parquet('s3://markettrend-datalake/clean/compras/')

# Calcular métricas por cliente
df_metricas = df_compras.groupBy('id_cliente').agg(
    F.count('*').alias('frecuencia_compras'),
    F.max('fecha_compra').alias('ultima_compra'),
    F.avg('monto').alias('ticket_promedio')
)

# Guardar en zona curated
df_metricas.write.mode('overwrite').parquet('s3://markettrend-datalake/curated/metricas_clientes/')

spark.stop()
'''



spark_code_streaming = '''
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

spark = SparkSession.builder.appName('MarketTrendStreaming').getOrCreate()

# Leer eventos desde Kafka
df_raw = spark.readStream.format('kafka')\
    .option('kafka.bootstrap.servers', 'kafka:9092')\
    .option('subscribe', 'eventos_app_movil')\
    .load()

# Esquema del mensaje
schema = StructType([
    StructField('id_cliente', StringType()),
    StructField('producto', StringType()),
    StructField('timestamp', TimestampType())
])

# Parsear mensajes
df_parsed = df_raw.select(
    from_json(col('value').cast('string'), schema).alias('data')
).select('data.*')

# Productos más vistos en ventanas de 5 minutos
df_agg = df_parsed.groupBy(
    window(col('timestamp'), '5 minutes'),
    col('producto')
).count().orderBy(col('count').desc())

# Escribir resultados en consola (o en otro sink)
query = df_agg.writeStream.outputMode('complete')\
    .format('console')\
    .start()

query.awaitTermination()
'''
