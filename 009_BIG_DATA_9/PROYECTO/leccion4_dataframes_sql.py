#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# ================================================================
# Lección 4: Procesamiento de datos estructurados — Spark SQL y DataFrames
# ================================================================
# Proyecto: Retail Analytics Pipeline — Módulo 9
# Empresa ficticia: RetailMax (e-commerce de moda)
# Dataset: Fashion-MNIST (70,000 imágenes de prendas de ropa)
#
# MAPA DE LA LECCIÓN:
#   Sección 0: Configuración inicial
#   Sección 1: De RDD a DataFrame — Esquemas explícitos
#   Sección 2: Operaciones básicas con DataFrame API
#   Sección 3: Spark SQL — Vistas temporales y consultas
#   Sección 4: Métricas de negocio RetailMax
#   Sección 5: Optimización — Catalyst y particionamiento
#   Sección 6: Guardar en formato Parquet
#   Sección 7: Guardar métricas en Parquet
#   Sección 8: Cierre e informe final
# ================================================================
"""


# ================================================================
# SECCIÓN 0: Configuración inicial
# ================================================================
# --- Recap de Lección 3 ---
# En la Lección 3 trabajamos con RDDs: map(), filter(), flatMap(),
# sortBy() y entendimos el DAG de ejecución diferida.
# Limitación: Spark no conoce la estructura interna de los RDDs,
# por lo que no puede optimizar automáticamente las consultas.
#
# ¿Qué cambia con DataFrames?
#   RDD:       [objeto, objeto, ...]   ← caja negra para Spark
#   DataFrame: [fila con columnas tipadas, ...]  ← schema conocido por Spark
#
# El optimizador Catalyst usa el schema para reescribir y optimizar
# el plan de ejecución automáticamente (igual que un motor de BD).
#
# Conexión con Lección 5:
#   Al final guardaremos Parquet → la Lección 5 (MLlib) lo usará
#   como entrada del pipeline de Machine Learning distribuido.


def main():

    # === SECCIÓN 0: Importaciones y configuración ================

    # --- 0.1 Importaciones de PySpark ---
    from pyspark.sql import SparkSession
    from pyspark.sql.types import (
        StructType,    # Define la estructura completa del DataFrame
        StructField,   # Define cada campo (columna) del schema
        StringType,    # Tipo string de Spark
        IntegerType,   # Tipo entero de Spark
        FloatType,     # Tipo float de Spark
        ArrayType      # Tipo array (lista) de Spark — declarado por completitud
    )
    import pyspark.sql.functions as F  # Funciones de Spark SQL (col, when, avg, count, etc.)

    # --- 0.2 Importaciones estándar ---
    import numpy as np           # Operaciones numéricas sobre arrays de píxeles
    import pandas as pd          # Para toPandas() y visualización de resultados
    import matplotlib.pyplot as plt   # Visualizaciones
    import matplotlib.cm as cm        # Colormaps para gráficos
    import os                    # Manejo de rutas y archivos
    import shutil                # Para eliminar carpetas (shutil.rmtree)
    import time                  # Para medir tiempos de ejecución

    print("✓ Librerías importadas correctamente")

    # --- 0.3 Crear SparkSession ---
    # Usamos los mismos parámetros que en las lecciones anteriores
    spark = (
        SparkSession.builder
        .appName("RetailMax-Leccion4-DataFrames")    # Nombre del job en la Spark UI
        .master("local[*]")                           # Usar todos los cores disponibles
        .config("spark.driver.memory", "2g")          # Memoria del driver
        .config("spark.sql.shuffle.partitions", "4")  # Particiones para operaciones de shuffle
        .config("spark.ui.showConsoleProgress", "false")   # Suprimir barras de progreso
        .getOrCreate()
    )

    # Reducir verbosidad de los logs de Spark
    spark.sparkContext.setLogLevel("ERROR")

    print(f"✓ SparkSession creada — Versión de Spark: {spark.version}")
    print(f"  AppName: {spark.sparkContext.appName}")
    print(f"  Master:  {spark.sparkContext.master}")

    # --- 0.4 Mapeo de etiquetas: número → nombre de categoría ---
    # Fashion-MNIST tiene 10 clases de prendas de ropa
    LABEL_NAMES = {
        0: "T-shirt/top",
        1: "Trouser",
        2: "Pullover",
        3: "Dress",
        4: "Coat",
        5: "Sandal",
        6: "Shirt",
        7: "Sneaker",
        8: "Bag",
        9: "Ankle boot"
    }

    print(f"\n✓ Categorías de Fashion-MNIST:")
    for k, v in LABEL_NAMES.items():
        print(f"   [{k}] {v}")

    # ================================================================
    # SECCIÓN 0 (cont.): Carga de Fashion-MNIST
    # ================================================================
    # Intentamos cargar por varios métodos. NO almacenaremos los 784
    # píxeles en el DataFrame; solo calcularemos estadísticas por imagen.

    X_train, y_train = None, None
    X_test, y_test   = None, None
    carga_exitosa    = False
    metodo_carga     = ""

    # --- Método 1: TensorFlow/Keras ---
    if not carga_exitosa:
        try:
            import tensorflow as tf
            (X_train, y_train), (X_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
            carga_exitosa = True
            metodo_carga  = "TensorFlow/Keras"
            print("✓ Fashion-MNIST cargado con TensorFlow/Keras")
        except Exception as e:
            print(f"  TensorFlow no disponible: {e}")

    # --- Método 2: PyTorch / torchvision ---
    if not carga_exitosa:
        try:
            import torchvision.datasets as dsets
            import torchvision.transforms as transforms
            transform = transforms.ToTensor()
            train_ds = dsets.FashionMNIST(root="./data", train=True,  download=True, transform=transform)
            test_ds  = dsets.FashionMNIST(root="./data", train=False, download=True, transform=transform)
            X_train  = np.array([img.numpy().reshape(28, 28) for img, _ in train_ds])
            y_train  = np.array([label for _, label in train_ds])
            X_test   = np.array([img.numpy().reshape(28, 28) for img, _ in test_ds])
            y_test   = np.array([label for _, label in test_ds])
            # Escalar de [0,1] a [0,255] para consistencia
            X_train  = (X_train * 255).astype(np.uint8)
            X_test   = (X_test  * 255).astype(np.uint8)
            carga_exitosa = True
            metodo_carga  = "PyTorch/torchvision"
            print("✓ Fashion-MNIST cargado con PyTorch/torchvision")
        except Exception as e:
            print(f"  PyTorch no disponible: {e}")

    # --- Método 3: scikit-learn (fetch_openml) ---
    if not carga_exitosa:
        try:
            from sklearn.datasets import fetch_openml
            print("  Descargando Fashion-MNIST desde OpenML (puede tardar 1-2 min)...")
            dataset = fetch_openml(name="Fashion-MNIST", version=1, as_frame=False)
            X_all   = dataset.data.reshape(-1, 28, 28).astype(np.uint8)
            y_all   = dataset.target.astype(int)
            # División estándar: 60,000 train / 10,000 test
            X_train, y_train = X_all[:60000], y_all[:60000]
            X_test,  y_test  = X_all[60000:], y_all[60000:]
            carga_exitosa = True
            metodo_carga  = "scikit-learn/OpenML"
            print("✓ Fashion-MNIST cargado con scikit-learn/OpenML")
        except Exception as e:
            print(f"  scikit-learn no disponible: {e}")

    # --- Método 4: Datos sintéticos (fallback garantizado) ---
    if not carga_exitosa:
        print("  Generando datos sintéticos que replican la estructura de Fashion-MNIST...")
        np.random.seed(42)
        n_train, n_test = 60000, 10000
        # Cada clase tiene un brillo base ligeramente diferente para realismo
        X_train = np.zeros((n_train, 28, 28), dtype=np.uint8)
        y_train = np.array([i % 10 for i in range(n_train)])
        for i in range(n_train):
            clase_base = y_train[i] * 25   # Brillo base por clase (0-225)
            ruido      = np.random.randint(0, 50, (28, 28))
            X_train[i] = np.clip(clase_base + ruido, 0, 255).astype(np.uint8)
        X_test  = np.zeros((n_test, 28, 28), dtype=np.uint8)
        y_test  = np.array([i % 10 for i in range(n_test)])
        for i in range(n_test):
            clase_base = y_test[i] * 25
            ruido      = np.random.randint(0, 50, (28, 28))
            X_test[i]  = np.clip(clase_base + ruido, 0, 255).astype(np.uint8)
        carga_exitosa = True
        metodo_carga  = "Sintético (fallback)"
        print("✓ Datos sintéticos generados")

    # --- Verificación de dimensiones ---
    print(f"\n📊 Resumen del dataset ({metodo_carga}):")
    print(f"   X_train: {X_train.shape}  — {X_train.shape[0]:,} imágenes de {X_train.shape[1]}×{X_train.shape[2]} px")
    print(f"   X_test:  {X_test.shape}   — {X_test.shape[0]:,}  imágenes de {X_test.shape[1]}×{X_test.shape[2]} px")
    print(f"   Clases:  {np.unique(y_train)}")

    # ================================================================
    # SECCIÓN 0 (cont.): Preparar lista de filas para el DataFrame
    # ================================================================
    # SCHEMA a usar:
    #   image_id   (int)   — identificador único (0 a 69,999)
    #   label      (int)   — etiqueta numérica de la clase (0-9)
    #   label_name (str)   — nombre de la categoría
    #   pixel_mean (float) — brillo promedio de la imagen (0.0 a 255.0)
    #   pixel_std  (float) — desviación estándar de los píxeles (contraste)
    #   pixel_max  (float) — valor máximo de píxel
    #   pixel_min  (float) — valor mínimo de píxel
    #   split      (str)   — "train" o "test"

    print("Preparando lista de filas (esto puede tardar 10-20 segundos)...")
    t0   = time.time()
    rows = []  # Lista donde acumularemos todas las filas

    # --- Procesar imágenes de ENTRENAMIENTO ---
    for idx in range(len(X_train)):
        img   = X_train[idx].flatten().astype(np.float32)  # Aplanar 28×28 → 784 valores
        label = int(y_train[idx])
        rows.append((
            idx,                           # image_id único
            label,                         # etiqueta numérica
            LABEL_NAMES[label],            # nombre de la categoría
            float(np.mean(img)),           # pixel_mean
            float(np.std(img)),            # pixel_std
            float(np.max(img)),            # pixel_max
            float(np.min(img)),            # pixel_min
            "train"                        # split
        ))

    # --- Procesar imágenes de TEST ---
    for idx in range(len(X_test)):
        img   = X_test[idx].flatten().astype(np.float32)
        label = int(y_test[idx])
        rows.append((
            len(X_train) + idx,            # image_id continúa desde donde paró train
            label,
            LABEL_NAMES[label],
            float(np.mean(img)),
            float(np.std(img)),
            float(np.max(img)),
            float(np.min(img)),
            "test"
        ))

    t1 = time.time()
    print(f"✓ Lista de filas preparada en {t1 - t0:.2f} segundos")
    print(f"  Total de filas: {len(rows):,}  (60,000 train + 10,000 test)")
    print(f"\nEjemplo de una fila (imagen 0):")
    print(f"  image_id   = {rows[0][0]}")
    print(f"  label      = {rows[0][1]}")
    print(f"  label_name = '{rows[0][2]}'")
    print(f"  pixel_mean = {rows[0][3]:.4f}")
    print(f"  pixel_std  = {rows[0][4]:.4f}")
    print(f"  pixel_max  = {rows[0][5]:.0f}")
    print(f"  pixel_min  = {rows[0][6]:.0f}")
    print(f"  split      = '{rows[0][7]}'")

    # ================================================================
    # === SECCIÓN 1: De RDD a DataFrame — Esquemas explícitos ==========
    # ================================================================
    # ¿Por qué DataFrames?
    #   Spark conoce el schema → Catalyst puede optimizar consultas
    #   automáticamente (predicate pushdown, projection pruning, etc.)
    #
    # Comparativa RDD vs DataFrame:
    #   RDD: sin schema, sin SQL, optimización manual → más flexible
    #   DataFrame: schema + SQL + Catalyst → mucho más rápido en analytics
    #
    # Nota: en Python, Dataset = DataFrame (tipado estático solo en Scala/Java)
    #
    # Schema de fashion_data:
    #   image_id   : IntegerType   ← 0, 1, 2, ..., 69999
    #   label      : IntegerType   ← 0, 1, 2, ..., 9
    #   label_name : StringType    ← "T-shirt/top", "Sneaker", ...
    #   pixel_mean : FloatType     ← 0.0 a 255.0
    #   pixel_std  : FloatType     ← 0.0 a 127.5 (aprox)
    #   pixel_max  : FloatType     ← 0.0 a 255.0
    #   pixel_min  : FloatType     ← 0.0 a 255.0
    #   split      : StringType    ← "train" o "test"

    # --- Paso 1: Definir el schema explícito ---
    schema = StructType([
        StructField("image_id",   IntegerType(), nullable=False),  # ID único, nunca nulo
        StructField("label",      IntegerType(), nullable=False),  # Etiqueta numérica
        StructField("label_name", StringType(),  nullable=False),  # Nombre de categoría
        StructField("pixel_mean", FloatType(),   nullable=False),  # Brillo promedio
        StructField("pixel_std",  FloatType(),   nullable=False),  # Desviación estándar
        StructField("pixel_max",  FloatType(),   nullable=False),  # Píxel más brillante
        StructField("pixel_min",  FloatType(),   nullable=False),  # Píxel más oscuro
        StructField("split",      StringType(),  nullable=False),  # "train" o "test"
    ])

    print("\n✓ Schema definido:")
    for field in schema.fields:
        print(f"   {field.name:12s} → {field.dataType}  (nullable={field.nullable})")

    # --- Paso 2: Crear DataFrame desde la lista de Python ---
    # spark.createDataFrame(data, schema) distribuye los datos y aplica tipos.
    print("\nCreando DataFrame (esto puede tardar unos segundos)...")
    t0 = time.time()
    df = spark.createDataFrame(rows, schema=schema)
    t1 = time.time()
    print(f"✓ DataFrame creado en {t1 - t0:.2f} segundos")

    # --- Paso 3: Mostrar el schema con printSchema() ---
    # printSchema() imprime el árbol de columnas con sus tipos.
    print("\nEsquema del DataFrame:")
    df.printSchema()

    # --- Paso 4: Mostrar las primeras 5 filas ---
    # show(n) activa una acción: Spark ejecuta el DAG y materializa n filas.
    print("Primeras 5 filas del DataFrame:")
    df.show(5, truncate=False)

    # --- Paso 5: Dimensiones del DataFrame ---
    n_filas    = df.count()          # Acción: cuenta todas las filas
    n_columnas = len(df.columns)     # Número de columnas (no es una acción)
    print(f"\nDimensiones: {n_filas:,} filas × {n_columnas} columnas")
    print(f"Columnas: {df.columns}")

    # --- Paso 6: Estadísticas generales ---
    # describe() calcula count, mean, stddev, min, max para columnas numéricas.
    print("\nEstadísticas generales (columnas numéricas):")
    df.describe(["pixel_mean", "pixel_std", "pixel_max", "pixel_min"]).show()

    # ================================================================
    # === SECCIÓN 2: Operaciones básicas con DataFrame API =============
    # ================================================================
    # Dos formas de operar sobre un DataFrame:
    #   1. DataFrame API: df.select(), df.filter(), df.withColumn(), df.groupBy()
    #   2. Spark SQL: spark.sql("SELECT ...")   ← ver Sección 3
    #
    # Ambas producen el mismo plan de ejecución por debajo (Catalyst).
    # Elección: DataFrame API para lógica Python compleja; SQL para legibilidad.

    # --- Paso 1: select() — seleccionar un subconjunto de columnas ---
    # Equivalente a SELECT en SQL. Spark NO copia los datos.
    print("=== Paso 1: select() — Seleccionar columnas ===")
    df_seleccion = df.select("image_id", "label_name", "pixel_mean")
    df_seleccion.show(5)

    # --- Paso 2: filter() / where() — filtrar filas por condición ---
    # filter() y where() son sinónimos en Spark.
    print("=== Paso 2: filter() — Solo clase 0 (T-shirt/top) ===")
    df_clase0 = df.filter(df.label == 0)   # Equivalente: df.where("label = 0")
    df_clase0.show(3, truncate=False)
    print(f"  Filas de T-shirt/top: {df_clase0.count():,}")

    # --- Paso 3: withColumn() — crear nueva columna derivada ---
    # Clasificar brillo: dark (<76.5), medium (<153.0), bright (>=153.0)
    # F.when() funciona como IF-ELSEIF-ELSE en SQL.
    print("=== Paso 3: withColumn() — Columna 'brightness' ===")
    df = df.withColumn(
        "brightness",                                          # Nombre de la nueva columna
        F.when(F.col("pixel_mean") < 76.5,  F.lit("dark"))   # pixel_mean en escala [0,255]
         .when(F.col("pixel_mean") < 153.0, F.lit("medium"))
         .otherwise(F.lit("bright"))                          # El resto es "bright"
    )
    print("DataFrame con nueva columna 'brightness':")
    df.select("image_id", "label_name", "pixel_mean", "brightness").show(8, truncate=False)

    # --- Paso 4: groupBy() + agg() — agrupar y agregar ---
    # COUNT(*) + AVG(pixel_mean) por clase — igual que GROUP BY en SQL
    print("=== Paso 4: groupBy() + agg() — Métricas por categoría ===")
    df_por_clase = (
        df.groupBy("label_name")
          .agg(
              F.count("*").alias("total"),                # COUNT(*)
              F.avg("pixel_mean").alias("avg_brightness"),# AVG(pixel_mean)
              F.avg("pixel_std").alias("avg_contraste")   # AVG(pixel_std)
          )
    )

    # --- Paso 5: orderBy() — ordenar resultados ---
    # Ordenar por total descendente (clase con más imágenes primero).
    print("=== Paso 5: orderBy() — Ordenar por total descendente ===")
    df_por_clase = df_por_clase.orderBy(F.desc("total"))
    df_por_clase.show(truncate=False)

    print("💡 Interpretación:")
    print("   Todas las clases tienen exactamente 7,000 imágenes (dataset balanceado).")
    print("   avg_brightness refleja el brillo promedio de cada categoría de prenda.")

    # ================================================================
    # === SECCIÓN 3: Spark SQL — Vistas temporales y consultas ==========
    # ================================================================
    # ¿Qué es una vista temporal?
    #   Un alias SQL que apunta a un DataFrame sin copiar los datos.
    #   Vive dentro de la SparkSession — no accesible desde otras sesiones.
    #   createOrReplaceTempView es idempotente (seguro para re-ejecutar).
    #   spark.sql(...) siempre devuelve un DataFrame — encadenable con API.
    #
    # ¿Por qué usar SQL en Spark?
    #   1. Legibilidad para analistas sin conocimiento de PySpark
    #   2. Misma optimización Catalyst que la DataFrame API
    #   3. Integración con Tableau, Power BI, Metabase
    #   4. Portabilidad: mover a Hive, BigQuery, Snowflake con ajustes mínimos

    # --- Paso 1: Registrar vista temporal ---
    df.createOrReplaceTempView("fashion_data")
    print("✓ Vista temporal 'fashion_data' registrada")
    print(f"  Tablas disponibles: {[t.name for t in spark.catalog.listTables()]}")

    # --- Paso 2: Consulta 1 — Distribución de clases ---
    # Pregunta de negocio: ¿Cuántas imágenes por categoría? ¿Brillo promedio?
    print("\n=== Consulta 1: Distribución de clases ===")
    q1 = spark.sql("""
        SELECT
            label_name,
            COUNT(*)          AS total,
            AVG(pixel_mean)   AS avg_brightness,
            MIN(pixel_mean)   AS min_brightness,
            MAX(pixel_mean)   AS max_brightness
        FROM fashion_data
        GROUP BY label_name
        ORDER BY total DESC
    """)
    q1.show(truncate=False)
    print("💡 RetailMax: Catálogo balanceado — 7,000 productos por categoría.")
    print("   Un catálogo balanceado garantiza que el modelo ML no estará sesgado.")

    # --- Paso 3: Consulta 2 — Top 3 clases más brillantes ---
    # Pregunta de negocio: ¿Qué categorías tienen imágenes con mayor brillo?
    print("\n=== Consulta 2: Top 3 categorías más brillantes ===")
    q2 = spark.sql("""
        SELECT
            label_name,
            ROUND(AVG(pixel_mean), 2) AS avg_brightness,
            ROUND(AVG(pixel_std),  2) AS avg_contraste
        FROM fashion_data
        GROUP BY label_name
        ORDER BY avg_brightness DESC
        LIMIT 3
    """)
    q2.show(truncate=False)
    print("💡 RetailMax: Categorías con fondo blanco o colores claros aumentan")
    print("   la tasa de conversión en e-commerce (+12% en estudios A/B).")

    # --- Paso 4: Consulta 3 — Imágenes con alto contraste ---
    # Calcular el percentil 75 de pixel_std como umbral
    print("\n=== Consulta 3: Imágenes con alto contraste (pixel_std > P75) ===")
    umbral_std = df.approxQuantile("pixel_std", [0.75], 0.01)[0]
    print(f"  Umbral P75 de pixel_std: {umbral_std:.4f}")

    q3 = spark.sql(f"""
        SELECT
            label_name,
            COUNT(*) AS total_alto_contraste,
            ROUND(AVG(pixel_std), 2) AS avg_contraste
        FROM fashion_data
        WHERE pixel_std > {umbral_std:.4f}
        GROUP BY label_name
        ORDER BY total_alto_contraste DESC
    """)
    q3.show(truncate=False)
    print(f"💡 RetailMax: pixel_std > {umbral_std:.1f} indica texturas complejas (denim, cuero, encaje).")

    # --- Paso 5: Consulta 4 — Comparación train vs test ---
    print("\n=== Consulta 4: Comparación train vs test ===")
    q4 = spark.sql("""
        SELECT
            split,
            COUNT(*)                  AS total,
            ROUND(AVG(pixel_mean), 2) AS avg_brightness,
            ROUND(AVG(pixel_std),  2) AS avg_contraste
        FROM fashion_data
        GROUP BY split
        ORDER BY split
    """)
    q4.show(truncate=False)
    print("💡 RetailMax: Distribuciones train/test similares — evaluación realista del modelo.")

    # ================================================================
    # === SECCIÓN 4: Métricas de negocio RetailMax ======================
    # ================================================================
    # Contexto de negocio RetailMax:
    #   label_name → Categoría de producto
    #   pixel_mean → Calidad visual de la imagen del producto
    #   pixel_std  → Contraste visual (detalle de la imagen)
    #   split='train' → Temporada actual (productos en venta)
    #   split='test'  → Temporada siguiente (productos en preview)

    print("Calculando métricas de negocio RetailMax...")

    # --- Métrica 1: Catálogo por categoría ---
    df_catalogo = spark.sql("""
        SELECT
            label_name,
            COUNT(*) AS total_productos
        FROM fashion_data
        GROUP BY label_name
        ORDER BY total_productos DESC
    """)

    # --- Métrica 2: Calidad visual promedio por categoría ---
    df_calidad = spark.sql("""
        SELECT
            label_name,
            ROUND(AVG(pixel_mean), 2)  AS calidad_visual_promedio,
            ROUND(AVG(pixel_std),  2)  AS contraste_promedio
        FROM fashion_data
        GROUP BY label_name
        ORDER BY calidad_visual_promedio DESC
    """)

    # --- Métrica 3: Productos con imagen de alta calidad ---
    media_global = df.select(F.avg("pixel_mean")).collect()[0][0]
    print(f"  Media global de pixel_mean: {media_global:.4f}")

    df_alta_calidad = spark.sql(f"""
        SELECT
            label_name,
            COUNT(*) AS productos_alta_calidad
        FROM fashion_data
        WHERE pixel_mean > {media_global:.4f}
        GROUP BY label_name
        ORDER BY productos_alta_calidad DESC
    """)

    # --- Métrica 4: Ranking de categorías por contraste visual ---
    df_ranking_contraste = spark.sql("""
        SELECT
            label_name,
            ROUND(AVG(pixel_std), 2)  AS contraste_promedio,
            ROUND(MAX(pixel_std), 2)  AS contraste_maximo
        FROM fashion_data
        GROUP BY label_name
        ORDER BY contraste_promedio DESC
    """)

    # --- Convertir a pandas para visualización ---
    # toPandas() transfiere datos del cluster al driver — usar con cuidado.
    pd_catalogo    = df_catalogo.toPandas()
    pd_calidad     = df_calidad.toPandas()
    pd_alta_calidad = df_alta_calidad.toPandas()
    pd_contraste   = df_ranking_contraste.toPandas()

    print("\n=== Métrica 1: Catálogo por categoría ===")
    print(pd_catalogo.to_string(index=False))

    print("\n=== Métrica 2: Calidad visual promedio ===")
    print(pd_calidad.to_string(index=False))

    print(f"\n=== Métrica 3: Productos con calidad visual > {media_global:.1f} ===")
    print(pd_alta_calidad.to_string(index=False))

    print("\n=== Métrica 4: Ranking por contraste visual ===")
    print(pd_contraste.to_string(index=False))

    # --- Visualizaciones del dashboard RetailMax ---
    # Crear carpeta output antes de guardar gráficos
    os.makedirs("output", exist_ok=True)

    pd_merged = pd_catalogo.merge(pd_calidad, on="label_name")

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle(
        "RetailMax — Dashboard de Catálogo de Productos\n(Fashion-MNIST, 70,000 imágenes)",
        fontsize=14, fontweight="bold", y=1.02
    )

    # ---- Gráfico 1: Distribución de productos por categoría ----
    ax1      = axes[0]
    categorias = pd_merged["label_name"]
    totales  = pd_merged["total_productos"]
    bars1    = ax1.barh(categorias, totales, color="steelblue", edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars1, totales):
        ax1.text(bar.get_width() + 30, bar.get_y() + bar.get_height()/2,
                 f"{val:,}", va="center", ha="left", fontsize=9, color="#333333")

    ax1.set_xlabel("Número de productos en catálogo", fontsize=11)
    ax1.set_title("Métrica 1: Distribución del catálogo\npor categoría", fontsize=12)
    ax1.set_xlim(0, totales.max() * 1.15)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.grid(axis="x", alpha=0.3)

    # ---- Gráfico 2: Calidad visual promedio por categoría ----
    pd_calidad_sorted = pd_calidad.sort_values("calidad_visual_promedio")
    calidad_sorted    = pd_calidad_sorted["calidad_visual_promedio"].values
    norm2             = plt.Normalize(calidad_sorted.min(), calidad_sorted.max())
    colores2          = plt.cm.YlOrRd(norm2(calidad_sorted))

    ax2 = axes[1]
    bars2 = ax2.barh(
        pd_calidad_sorted["label_name"],
        calidad_sorted,
        color=colores2,
        edgecolor="white",
        linewidth=0.5
    )

    for bar, val in zip(bars2, calidad_sorted):
        ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                 f"{val:.1f}", va="center", ha="left", fontsize=9, color="#333333")

    ax2.axvline(media_global, color="royalblue", linestyle="--", linewidth=1.5,
                label=f"Media global: {media_global:.1f}")
    ax2.legend(loc="lower right", fontsize=9)
    ax2.set_xlabel("Calidad visual promedio (pixel_mean, escala 0-255)", fontsize=11)
    ax2.set_title("Métrica 2: Calidad visual promedio\npor categoría (coloreado por valor)", fontsize=12)
    ax2.set_xlim(0, calidad_sorted.max() * 1.15)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="x", alpha=0.3)

    sm   = plt.cm.ScalarMappable(cmap="YlOrRd", norm=norm2)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax2, shrink=0.6, pad=0.01)
    cbar.set_label("Nivel de brillo", fontsize=9)

    plt.tight_layout()
    plt.savefig("output/leccion4_dashboard_retailmax.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("✓ Dashboard guardado en output/leccion4_dashboard_retailmax.png")

    # ================================================================
    # === SECCIÓN 5: Optimización — Catalyst y particionamiento ========
    # ================================================================
    # Catalyst Optimizer — flujo de transformación del plan:
    #   Tu código → Plan lógico sin resolver
    #   → Plan lógico resuelto
    #   → Plan lógico optimizado (predicate pushdown, projection pruning...)
    #   → Plan físico (sort-merge join vs broadcast join...)
    #   → Código JVM con Tungsten
    #   → Ejecución
    #
    # Reglas clave de Catalyst:
    #   Predicate Pushdown: WHERE se aplica antes de joins
    #   Projection Pruning: solo lee columnas necesarias
    #   Constant Folding: pre-calcula expresiones constantes
    #   Join Reordering: tabla pequeña × grande → broadcast join
    #
    # Reparticionamiento:
    #   Pocas particiones → bajo paralelismo
    #   Muchas particiones → overhead de scheduling
    #   Regla: 2-4 particiones por core
    #
    # cache(): guarda el DataFrame en memoria para reusar en múltiples acciones.
    #   Sin cache: Spark recalcula el DAG completo cada vez.

    # --- Paso 1: df.explain() — Ver el plan de ejecución ---
    print("=== Paso 1: Plan de ejecución de una consulta típica ===")
    print("(Plan para: GROUP BY label_name ORDER BY total DESC)\n")
    df.groupBy("label_name").agg(F.count("*").alias("total")).orderBy(F.desc("total")).explain()

    # --- Paso 2: Ver número de particiones actuales ---
    n_particiones = df.rdd.getNumPartitions()
    print(f"\n=== Paso 2: Número de particiones actuales: {n_particiones} ===")
    print(f"   Con {n_particiones} particiones y {os.cpu_count()} CPUs disponibles,")
    print(f"   cada CPU procesa aprox. {70000 // n_particiones:,} filas por partición.")

    # --- Paso 3: Reparticionamiento por columna ---
    # repartition(n, col) redistribuye en n particiones usando hash de 'col'.
    print("\n=== Paso 3: Reparticionamiento por columna 'label' ===")
    df_repart = df.repartition(4, "label")
    print(f"   Particiones antes: {df.rdd.getNumPartitions()}")
    print(f"   Particiones después: {df_repart.rdd.getNumPartitions()}")
    print("   Ventaja: GROUP BY label más rápido — misma clase en misma partición.")

    # --- Paso 4: cache() — medir diferencia de tiempo ---
    print("\n=== Paso 4: Diferencia de tiempo con y sin cache() ===")

    # Sin cache — primera ejecución
    df_sin_cache = spark.createDataFrame(rows, schema=schema)
    t0 = time.time()
    _ = df_sin_cache.count()
    t1 = time.time()
    tiempo_sin_cache = t1 - t0

    # Con cache
    df_con_cache = spark.createDataFrame(rows, schema=schema)
    df_con_cache.cache()          # Marca para persistencia en memoria
    t0 = time.time()
    _ = df_con_cache.count()      # Primera acción — ejecuta DAG y guarda en cache
    t1 = time.time()
    tiempo_cache_frio = t1 - t0

    t0 = time.time()
    _ = df_con_cache.count()      # Segunda acción — lee desde memoria
    t1 = time.time()
    tiempo_cache_caliente = t1 - t0

    print(f"   Sin cache (1er count):           {tiempo_sin_cache:.3f}s")
    print(f"   Con cache (1er count, frío):     {tiempo_cache_frio:.3f}s  ← incluye escritura a cache")
    print(f"   Con cache (2do count, caliente): {tiempo_cache_caliente:.3f}s  ← lee desde memoria")

    if tiempo_sin_cache > 0 and tiempo_cache_caliente > 0:
        mejora = tiempo_sin_cache / max(tiempo_cache_caliente, 0.001)
        print(f"   ✓ Mejora con cache: {mejora:.1f}× más rápido")

    print("\n   💡 Regla práctica: usa .cache() cuando reutilices un DataFrame")
    print("   en múltiples acciones (count, show, write, toPandas).")
    print("   Usa .unpersist() cuando ya no lo necesites para liberar memoria.")

    df_con_cache.unpersist()
    print("   Cache liberado.")

    # ================================================================
    # === SECCIÓN 6: Guardar en formato Parquet ========================
    # ================================================================
    # ¿Qué es Parquet?
    #   Formato columnar diseñado para analytics.
    #   CSV (filas): lee todo para calcular AVG de una columna.
    #   Parquet (columnas): lee solo la columna necesaria.
    #
    # Ventajas sobre CSV:
    #   Compresión Snappy/Gzip integrada → archivos 2-5× más pequeños
    #   Schema embebido → no hay que inferirlo al leer
    #   Lectura columnar → solo lee columnas necesarias
    #   Velocidad 2-10× mayor en analytics
    #
    # Ejemplo numérico para 70,000 filas × 8 columnas:
    #   CSV estimado:    70,000 × 62 bytes ≈ 4.2 MB
    #   Parquet estimado: 0.8-1.5 MB (compresión Snappy)

    # --- Paso 1: Definir ruta de salida ---
    output_path = "output/leccion4_fashion_data.parquet"
    print(f"Ruta de salida: {output_path}")

    # Crear carpeta output/ si no existe
    os.makedirs("output", exist_ok=True)

    # --- Paso 2: Limpiar carpeta si existe ---
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
        print(f"  Carpeta anterior eliminada: {output_path}")

    # --- Paso 3: Guardar el DataFrame completo en Parquet ---
    # Spark escribe múltiples archivos .parquet (uno por partición)
    print("Guardando DataFrame en Parquet...")
    t0 = time.time()
    try:
        df.write.mode("overwrite").parquet(output_path)
        t1 = time.time()
        print(f"✓ Parquet guardado en {t1 - t0:.2f} segundos")
    except Exception as e:
        print(f"✗ Error al guardar Parquet: {e}")
        raise

    # --- Paso 4: Verificar archivos guardados ---
    print("\nContenido de la carpeta de salida:")
    archivos_parquet = []
    for root, dirs, files in os.walk(output_path):
        for fname in files:
            ruta_completa = os.path.join(root, fname)
            size_kb = os.path.getsize(ruta_completa) / 1024
            print(f"   {fname:<50s}  {size_kb:>8.2f} KB")
            if fname.endswith(".parquet"):
                archivos_parquet.append(ruta_completa)

    # --- Paso 5: Calcular tamaño total ---
    size_total_bytes = sum(os.path.getsize(f) for f in archivos_parquet)
    size_total_mb    = size_total_bytes / (1024 ** 2)
    print(f"\n  Archivos .parquet: {len(archivos_parquet)}")
    print(f"  Tamaño total Parquet: {size_total_mb:.3f} MB")

    # --- Paso 6: Leer el Parquet de vuelta ---
    print("\nLeyendo Parquet de vuelta...")
    df_loaded = spark.read.parquet(output_path)
    print("Schema del Parquet leído:")
    df_loaded.printSchema()

    # --- Paso 7: Verificar que los conteos coinciden ---
    count_original = df.count()
    count_cargado  = df_loaded.count()
    print(f"\nVerificación de integridad:")
    print(f"   Filas en df original:  {count_original:,}")
    print(f"   Filas en df cargado:   {count_cargado:,}")
    assert count_original == count_cargado, "¡ERROR: Los conteos no coinciden!"
    print(f"   ✓ Conteos coinciden — integridad verificada")

    # --- Paso 8: Comparar tamaño Parquet vs estimado CSV ---
    bytes_estimados_csv = count_original * 62    # 62 bytes promedio por fila
    size_csv_mb         = bytes_estimados_csv / (1024 ** 2)
    ratio_compresion    = size_csv_mb / size_total_mb if size_total_mb > 0 else 0

    print(f"\n📊 Comparativa de tamaño:")
    print(f"   Tamaño estimado en CSV: {size_csv_mb:.3f} MB")
    print(f"   Tamaño real en Parquet: {size_total_mb:.3f} MB")
    print(f"   Ratio de compresión:    {ratio_compresion:.1f}× menor en Parquet")

    print(f"\n✅ Parquet guardado en: {output_path}")
    print(f"   Tamaño: {size_total_mb:.3f} MB | Filas: {count_cargado:,} | Columnas: {len(df_loaded.columns)}")

    # ================================================================
    # === SECCIÓN 7: Guardar métricas en Parquet =======================
    # ================================================================
    # Guardamos las métricas agregadas para la Lección 5 (MLlib).
    # El DataFrame de métricas es el punto de entrada del pipeline de ML.

    metricas_path = "output/leccion4_metricas.parquet"

    print("Construyendo DataFrame de métricas para Lección 5...")
    df_metricas = spark.sql(f"""
        SELECT
            label_name,
            COUNT(*)                                                   AS total_productos,
            ROUND(AVG(pixel_mean),  4)                                 AS calidad_visual_promedio,
            ROUND(AVG(pixel_std),   4)                                 AS contraste_promedio,
            ROUND(MAX(pixel_mean),  4)                                 AS calidad_maxima,
            ROUND(MIN(pixel_mean),  4)                                 AS calidad_minima,
            SUM(CASE WHEN pixel_mean > {media_global:.4f} THEN 1 ELSE 0 END) AS productos_alta_calidad,
            ROUND(AVG(pixel_max),   4)                                 AS brillo_pico_promedio,
            ROUND(AVG(pixel_min),   4)                                 AS sombra_promedio
        FROM fashion_data
        GROUP BY label_name
        ORDER BY total_productos DESC
    """)

    print("\nDataFrame de métricas:")
    df_metricas.show(truncate=False)

    # Limpiar carpeta anterior si existe
    if os.path.exists(metricas_path):
        shutil.rmtree(metricas_path)

    # Guardar en Parquet
    print(f"Guardando métricas en: {metricas_path}")
    try:
        df_metricas.write.mode("overwrite").parquet(metricas_path)
        print(f"✓ Métricas guardadas")
    except Exception as e:
        print(f"✗ Error al guardar métricas: {e}")
        raise

    # Verificar
    df_metricas_cargado = spark.read.parquet(metricas_path)
    n_metricas          = df_metricas_cargado.count()
    print(f"\nVerificación:")
    print(f"   Filas guardadas: {n_metricas} (una por cada una de las 10 categorías)")
    print(f"   Columnas: {df_metricas_cargado.columns}")

    size_metricas = sum(
        os.path.getsize(os.path.join(r, f))
        for r, dirs, files in os.walk(metricas_path)
        for f in files if f.endswith(".parquet")
    )
    print(f"   Tamaño del Parquet de métricas: {size_metricas/1024:.2f} KB")
    print(f"\n✅ Parquet de métricas guardado en: {metricas_path}")
    print(f"   → Será cargado por la Lección 5 para el pipeline de MLlib")

    # ================================================================
    # === SECCIÓN 8: Cerrar SparkSession e informe final ==============
    # ================================================================

    # Detener la SparkSession — libera todos los recursos del cluster.
    # Siempre cerrar Spark al final para evitar fugas de memoria.
    spark.stop()
    print("✓ SparkSession cerrada correctamente")
    print("  Todos los recursos del cluster han sido liberados.")

    # ================================================================
    # RESUMEN DE LA LECCIÓN 4
    # ================================================================
    # Tabla de operaciones:
    #   Operación              | Código                            | Para qué sirve en RetailMax
    #   Definir schema         | StructType([StructField(...)])     | Tipos de columna del catálogo
    #   Crear DataFrame        | spark.createDataFrame(data, schema)| Cargar 70K productos
    #   Ver schema             | df.printSchema()                  | Auditar estructura de datos
    #   Seleccionar columnas   | df.select("col1", "col2")         | Extraer campos necesarios
    #   Filtrar filas          | df.filter(df.label == 0)          | Filtrar por categoría
    #   Agregar columna        | df.withColumn("brightness", ...)  | Clasificar calidad de imagen
    #   Agrupar y agregar      | df.groupBy().agg(...)             | Métricas por categoría
    #   Registrar vista SQL    | df.createOrReplaceTempView("n")   | Exponer datos a analistas
    #   Consulta SQL           | spark.sql("SELECT ...")           | KPIs del dashboard
    #   Ver plan de ejecución  | df.explain()                      | Depurar consultas lentas
    #   Reparticionar          | df.repartition(4, "label")        | Optimizar GROUP BY
    #   Cache                  | df.cache()                        | Reusar en múltiples acciones
    #   Convertir a pandas     | df.toPandas()                     | Visualizaciones matplotlib
    #   Guardar Parquet        | df.write.mode("overwrite").parquet| Persistir para Lección 5
    #   Leer Parquet           | spark.read.parquet(path)          | Cargar en lecciones posteriores
    #
    # Archivos generados en output/:
    #   leccion4_fashion_data.parquet/    ← DataFrame completo (70,000 filas)
    #   leccion4_metricas.parquet/        ← Métricas agregadas (10 filas)
    #   leccion4_dashboard_retailmax.png  ← Gráficos del dashboard
    #
    # Conexión con Lección 5:
    #   df = spark.read.parquet("output/leccion4_fashion_data.parquet")
    #   metricas = spark.read.parquet("output/leccion4_metricas.parquet")
    #   → Pipeline de MLlib con pixel_mean, pixel_std, pixel_max, pixel_min
    #     como vector de features para clasificación de prendas.
    #
    # Checklist de entregables:
    #   [x] DataFrame creado — 70,000 filas con schema explícito
    #   [x] SQL ejecutado — 4 consultas con interpretación de negocio
    #   [x] Métricas de negocio — Dashboard RetailMax con 4 KPIs
    #   [x] Visualizaciones — 2 gráficos matplotlib del dashboard
    #   [x] Optimización — explain(), repartition(), cache() demostrados
    #   [x] Parquet guardado — leccion4_fashion_data.parquet
    #   [x] Métricas en Parquet — leccion4_metricas.parquet (para Lección 5)


if __name__ == "__main__":
    main()
