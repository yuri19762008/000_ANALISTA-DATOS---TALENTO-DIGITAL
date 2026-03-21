"""
# Lección 3: Elementos básicos de Spark — RDD, Transformaciones y Acciones
# Módulo 9 · Retail Analytics Pipeline · RetailMax E-commerce
#
# Recap de Lección 2:
#   - Configuramos Spark, creamos SparkSession y primer RDD básico
#
# En esta Lección 3:
#   - Transformaciones: map, filter, flatMap, distinct, sortBy
#   - Pair RDDs y reduceByKey
#   - Acciones: collect, sum, mean, stdev
#   - Linaje del RDD (DAG) con toDebugString()
#   - cache() y persist()
#
# Conexión con Lección 4:
#   - Convertiremos estos RDDs a DataFrames para usar Spark SQL
"""

# ============================================================
# SECCIÓN 0: CONFIGURACIÓN INICIAL
# ============================================================

# --- 0.1 Importaciones ---
import os                          # Operaciones del sistema operativo
import time                        # Medición de tiempos de ejecución
import numpy as np                 # Operaciones numéricas vectorizadas
import pandas as pd                # Tablas y análisis exploratorio
import matplotlib.pyplot as plt    # Visualizaciones
import matplotlib.patches as mpatches  # Leyendas en gráficos

# PySpark
from pyspark.sql import SparkSession
from pyspark import StorageLevel    # Niveles de persist() para Sección 8


def main():
    print("=" * 60)
    print("LECCIÓN 3 — RDD TRANSFORMACIONES Y ACCIONES")
    print("RetailMax · Módulo 9 · Retail Analytics Pipeline")
    print("=" * 60)

    print("\n✅ Librerías importadas correctamente")

    # --- 0.2 Crear SparkSession (igual que Lección 2) ---
    spark = (
        SparkSession.builder
        .appName("RetailMax_Leccion3_RDD")       # Nombre de la aplicación
        .master("local[*]")                       # Usa todos los núcleos disponibles
        .config("spark.driver.memory", "2g")      # 2 GB para el driver
        .config("spark.executor.memory", "2g")    # 2 GB para los executors
        .config("spark.sql.shuffle.partitions", "4")  # Reducir particiones para datos locales
        .config("spark.ui.showConsoleProgress", "false")  # Limpiar la salida en consola
        .getOrCreate()                            # Crea o reutiliza sesión existente
    )

    # Acceder al SparkContext (nivel bajo, maneja RDDs)
    sc = spark.sparkContext
    sc.setLogLevel("WARN")  # Reducir verbosidad de logs

    print(f"✅ SparkSession creada: {spark.version}")
    print(f"   App Name : {sc.appName}")
    print(f"   Master   : {sc.master}")

    # ============================================================
    # SECCIÓN 0.3: Carga de Fashion-MNIST
    # Se intenta en orden: TensorFlow → PyTorch → scikit-learn → datos sintéticos
    # ============================================================

    # Mapa de etiquetas de Fashion-MNIST
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

    train_images = train_labels = test_images = test_labels = None
    fuente = None

    # --- Intento 1: TensorFlow/Keras ---
    try:
        import tensorflow as tf
        (train_images, train_labels), (test_images, test_labels) = \
            tf.keras.datasets.fashion_mnist.load_data()
        fuente = "TensorFlow/Keras"
        print(f"✅ Fashion-MNIST cargado desde {fuente}")
    except Exception as e:
        print(f"⚠️  TensorFlow no disponible: {e}")

    # --- Intento 2: PyTorch/torchvision ---
    if train_images is None:
        try:
            import torchvision
            import torchvision.transforms as transforms
            transform = transforms.ToTensor()
            _train = torchvision.datasets.FashionMNIST(
                root="./data", train=True, download=True, transform=transform)
            _test  = torchvision.datasets.FashionMNIST(
                root="./data", train=False, download=True, transform=transform)
            train_images = np.array([img.numpy().squeeze() for img, _ in _train])
            train_labels = np.array([lbl for _, lbl in _train])
            test_images  = np.array([img.numpy().squeeze() for img, _ in _test])
            test_labels  = np.array([lbl for _, lbl in _test])
            fuente = "PyTorch/torchvision"
            print(f"✅ Fashion-MNIST cargado desde {fuente}")
        except Exception as e:
            print(f"⚠️  PyTorch no disponible: {e}")

    # --- Intento 3: scikit-learn (fetch_openml) ---
    if train_images is None:
        try:
            from sklearn.datasets import fetch_openml
            print("⏳ Descargando Fashion-MNIST desde OpenML (puede tardar ~60s)...")
            fmnist = fetch_openml("Fashion-MNIST", version=1, as_frame=False, parser="liac-arff")
            X = fmnist.data.astype(np.float32)
            y = fmnist.target.astype(np.int32)
            train_images = X[:60000].reshape(-1, 28, 28)
            train_labels = y[:60000]
            test_images  = X[60000:].reshape(-1, 28, 28)
            test_labels  = y[60000:]
            fuente = "scikit-learn/OpenML"
            print(f"✅ Fashion-MNIST cargado desde {fuente}")
        except Exception as e:
            print(f"⚠️  scikit-learn OpenML no disponible: {e}")

    # --- Intento 4: Datos sintéticos (fallback garantizado) ---
    if train_images is None:
        print("🔄 Generando datos sintéticos (Fashion-MNIST simulado)...")
        np.random.seed(42)
        # 60,000 imágenes de entrenamiento sintéticas
        train_images = np.random.randint(0, 256, (60000, 28, 28), dtype=np.uint8)
        train_labels = np.random.randint(0, 10,  60000,            dtype=np.int32)
        # 10,000 imágenes de prueba sintéticas
        test_images  = np.random.randint(0, 256, (10000, 28, 28), dtype=np.uint8)
        test_labels  = np.random.randint(0, 10,  10000,           dtype=np.int32)
        fuente = "Datos sintéticos (fallback)"
        print(f"✅ Datos sintéticos generados desde {fuente}")

    print(f"\n📊 Forma del conjunto de entrenamiento : {train_images.shape}")
    print(f"📊 Forma del conjunto de prueba        : {test_images.shape}")
    print(f"📊 Fuente de datos                     : {fuente}")

    # ============================================================
    # SECCIÓN 0.4: Preparar la lista de diccionarios
    # Usamos 10,000 imágenes de train + 2,000 de test = 12,000 total
    # ============================================================

    N_TRAIN = 10_000  # Primeras 10,000 imágenes de entrenamiento
    N_TEST  =  2_000  # Primeros 2,000 imágenes de prueba

    data = []  # Lista de diccionarios que irá al RDD

    # --- Procesar imágenes de entrenamiento ---
    for i in range(N_TRAIN):
        img   = train_images[i]              # Imagen 28x28 (uint8)
        label = int(train_labels[i])         # Etiqueta numérica 0-9
        # Aplanar y normalizar al rango [0, 1]
        pixels = (img.flatten().astype(np.float32) / 255.0).tolist()
        data.append({
            "image_id"   : i,                    # Identificador único
            "label"      : label,                # Etiqueta numérica
            "label_name" : LABEL_NAMES[label],   # Nombre de la categoría
            "pixels"     : pixels,               # Lista de 784 floats [0,1]
            "split"      : "train"               # Partición del dataset
        })

    # --- Procesar imágenes de prueba ---
    for j in range(N_TEST):
        img   = test_images[j]
        label = int(test_labels[j])
        pixels = (img.flatten().astype(np.float32) / 255.0).tolist()
        data.append({
            "image_id"   : N_TRAIN + j,          # IDs continúan desde 10,000
            "label"      : label,
            "label_name" : LABEL_NAMES[label],
            "pixels"     : pixels,
            "split"      : "test"
        })

    TOTAL = len(data)
    print(f"\n✅ Lista de diccionarios preparada")
    print(f"   Total de registros : {TOTAL:,}")
    print(f"   Train              : {N_TRAIN:,}")
    print(f"   Test               : {N_TEST:,}")
    print(f"\n🔍 Ejemplo de un registro (sin los píxeles):")
    ejemplo = {k: v for k, v in data[0].items() if k != "pixels"}
    ejemplo["pixels"] = f"[{data[0]['pixels'][0]:.4f}, {data[0]['pixels'][1]:.4f}, ... ] (784 valores)"
    for k, v in ejemplo.items():
        print(f"   {k:12s}: {v}")

    # ============================================================
    # SECCIÓN 0.5: Crear el RDD base con sc.parallelize()
    # ============================================================

    NUM_SLICES = 4  # Número de particiones (una por núcleo en equipo estándar)

    # sc.parallelize() distribuye la colección Python en NUM_SLICES particiones
    rdd_base = sc.parallelize(data, numSlices=NUM_SLICES)

    # Verificar el RDD creado
    num_registros   = rdd_base.count()          # Acción: cuenta todos los elementos
    num_particiones = rdd_base.getNumPartitions()  # Número de particiones reales

    print(f"\n✅ RDD creado con {num_registros:,} registros en {num_particiones} particiones")
    print(f"\n🔍 Primer registro del RDD (sin píxeles):")

    primer = rdd_base.first()  # Acción: trae el primer elemento al driver
    for k, v in primer.items():
        if k == "pixels":
            print(f"   {k:12s}: [{v[0]:.4f}, {v[1]:.4f}, ..., {v[-1]:.4f}] ({len(v)} valores)")
        else:
            print(f"   {k:12s}: {v}")

    # ============================================================
    # SECCIÓN 1: TRANSFORMACIÓN map
    # ============================================================
    #
    # ¿Qué es map?
    # map aplica una función a cada elemento del RDD y devuelve un nuevo RDD
    # con los resultados transformados. La correspondencia es 1 entrada → 1 salida.
    #
    # Analogía: conveyor belt (línea de ensamblaje)
    # Cada pieza entra, se transforma, y sale. Ninguna se crea ni se elimina.
    #
    # Es LAZY: no ejecuta hasta que se llama una acción (.take, .count, etc.)
    #
    # Mini-ejemplo numérico:
    #   RDD original   : [1, 2, 3, 4, 5]
    #   map(x * 2)     : [2, 4, 6, 8, 10]
    #
    # ============================================================

    print("\n" + "=" * 60)
    print("SECCIÓN 1: TRANSFORMACIÓN map")
    print("=" * 60)

    print("\n" + "=" * 60)
    print("PASO 1: Extraer metadata con map")
    print("=" * 60)

    # map: extraer solo los campos de metadata (sin los 784 píxeles)
    # Esto es LAZY — solo registra la transformación, no ejecuta aún
    rdd_metadata = rdd_base.map(lambda r: (
        r["image_id"],    # ID único de la imagen
        r["label"],       # Etiqueta numérica (0-9)
        r["label_name"],  # Nombre de la categoría
        r["split"]        # "train" o "test"
    ))

    # .take(2) es una acción → DISPARA la ejecución del DAG
    print("\n🔍 Primeros 2 registros de rdd_metadata:")
    for registro in rdd_metadata.take(2):
        print(f"   image_id={registro[0]:5d} | label={registro[1]} | "
              f"label_name={registro[2]:12s} | split={registro[3]}")

    print(f"\n📝 Cambio: de diccionarios con 788 claves → tuplas de 4 campos")

    print("\n" + "=" * 60)
    print("PASO 2: Calcular la media de píxeles por imagen con map")
    print("=" * 60)

    # map: calcular la media de los 784 píxeles de cada imagen
    # Resultado: RDD de tuplas (image_id, pixel_mean)
    rdd_pixel_means = rdd_base.map(lambda r: (
        r["image_id"],
        sum(r["pixels"]) / len(r["pixels"])  # Media aritmética manual
    ))

    print("\n🔍 Primeros 2 registros de rdd_pixel_means:")
    for image_id, mean_val in rdd_pixel_means.take(2):
        print(f"   image_id={image_id:5d} | pixel_mean={mean_val:.6f}")
    print("\n📝 Cambio: cada imagen (784 píxeles) → un solo número (la media)")

    print("\n" + "=" * 60)
    print("PASO 3: Renormalizar píxeles de [0,1] a [-1,1] con map")
    print("=" * 60)

    # map: renormalizar píxeles aplicando la fórmula pixel_norm = pixel * 2 - 1
    #   Si pixel = 0.0  → norm = -1.0  (negro)
    #   Si pixel = 0.5  → norm =  0.0  (gris)
    #   Si pixel = 1.0  → norm =  1.0  (blanco)
    rdd_normalized = rdd_base.map(lambda r: {
        **r,  # Copiar todos los campos existentes del diccionario
        "pixels": [p * 2 - 1 for p in r["pixels"]]  # Renormalizar cada píxel
    })

    print("\n🔍 Verificación de la renormalización (primeros 5 píxeles):")
    original    = rdd_base.first()["pixels"][:5]
    normalizado = rdd_normalized.first()["pixels"][:5]
    print("   Rango original  [0,1] :", [f"{p:.4f}" for p in original])
    print("   Rango normaliz. [-1,1]:", [f"{p:.4f}" for p in normalizado])
    print("\n📝 Fórmula: pixel_norm = pixel * 2 - 1")

    # ============================================================
    # SECCIÓN 2: TRANSFORMACIÓN filter
    # ============================================================
    #
    # ¿Qué es filter?
    # filter selecciona únicamente los elementos que cumplen una condición
    # booleana. Los que no cumplen son descartados. (1 entrada → 0 o 1 salida)
    #
    # Analogía: un colador — solo pasan los elementos que cumplen la condición
    #
    # Mini-ejemplo numérico:
    #   RDD original    : [1, 2, 3, 4, 5]
    #   filter(x > 3)   : [4, 5]
    #
    # ============================================================

    print("\n" + "=" * 60)
    print("SECCIÓN 2: TRANSFORMACIÓN filter")
    print("=" * 60)

    total = rdd_base.count()  # Total de registros en el RDD base

    print("\n" + "=" * 60)
    print("PASO 1: Filtrar solo imágenes de la clase 'Bag' (label == 8)")
    print("=" * 60)

    # filter: conservar solo las imágenes cuya etiqueta sea 8 (Bag)
    rdd_bags = rdd_base.filter(lambda r: r["label"] == 8)

    total_bags = rdd_bags.count()
    pct_bags   = total_bags / total * 100

    print(f"   Registros ANTES del filtro  : {total:,}")
    print(f"   Registros DESPUÉS del filtro: {total_bags:,}")
    print(f"   Porcentaje que representa   : {pct_bags:.2f}%")

    print("\n" + "=" * 60)
    print("PASO 2: Filtrar imágenes 'brillantes' (pixel_mean > 0.5)")
    print("=" * 60)

    # Nota: rdd_pixel_means tiene tuplas (image_id, pixel_mean)
    rdd_bright = rdd_pixel_means.filter(lambda x: x[1] > 0.5)

    total_pm     = rdd_pixel_means.count()
    total_bright = rdd_bright.count()
    pct_bright   = total_bright / total_pm * 100

    print(f"   Registros ANTES del filtro  : {total_pm:,}")
    print(f"   Registros DESPUÉS del filtro: {total_bright:,}")
    print(f"   Porcentaje que representa   : {pct_bright:.2f}%")

    print("\n" + "=" * 60)
    print("PASO 3: Filtrar solo registros del split 'test'")
    print("=" * 60)

    # filter: conservar solo las imágenes del conjunto de prueba
    rdd_test = rdd_base.filter(lambda r: r["split"] == "test")

    total_test = rdd_test.count()
    pct_test   = total_test / total * 100

    print(f"   Registros ANTES del filtro  : {total:,}")
    print(f"   Registros DESPUÉS del filtro: {total_test:,}")
    print(f"   Porcentaje que representa   : {pct_test:.2f}%")

    print("\n📊 RESUMEN DE FILTROS:")
    resumen_filtros = pd.DataFrame([
        {"Filtro": "label == 8 (Bag)",  "Registros": total_bags,   "% del total": pct_bags},
        {"Filtro": "pixel_mean > 0.5",  "Registros": total_bright, "% del total": pct_bright},
        {"Filtro": "split == 'test'",   "Registros": total_test,   "% del total": pct_test},
    ])
    resumen_filtros["% del total"] = resumen_filtros["% del total"].map("{:.2f}%".format)
    print(resumen_filtros.to_string(index=False))

    # ============================================================
    # SECCIÓN 3: TRANSFORMACIÓN flatMap
    # ============================================================
    #
    # ¿Qué es flatMap?
    # flatMap aplica una función a cada elemento, pero puede devolver
    # 0 o más elementos por cada entrada. Los resultados se aplanan
    # en un único RDD de salida.
    #
    # Diferencia: map devuelve 1 elemento por entrada (1:1)
    #             flatMap devuelve 0 o más elementos (1:N)
    #
    # Analogía: map = doblar una hoja
    #           flatMap = desdoblar sobres y apilar todo junto
    #
    # Mini-ejemplo:
    #   ["hola mundo", "big data"].flatMap(s.split()) → ["hola","mundo","big","data"]
    #
    # ============================================================

    print("\n" + "=" * 60)
    print("SECCIÓN 3: TRANSFORMACIÓN flatMap")
    print("=" * 60)

    print("\n" + "=" * 60)
    print("PASO 1: Expandir cada imagen en tuplas (image_id, pixel_idx, pixel_val)")
    print("        usando los primeros 10 píxeles de cada imagen")
    print("=" * 60)

    # flatMap: cada imagen genera una LISTA de 10 tuplas (una por píxel)
    rdd_pixels_flat = rdd_base.flatMap(lambda r: [
        (r["image_id"], pixel_idx, r["pixels"][pixel_idx])
        for pixel_idx in range(10)  # Solo los primeros 10 píxeles por imagen
    ])

    print("\nPASO 2: Contar el total de tuplas generadas")
    count_original = rdd_base.count()       # Número de imágenes originales
    count_flat     = rdd_pixels_flat.count()  # Número de tuplas tras flatMap

    print(f"   RDD original (imágenes) : {count_original:,} registros")
    print(f"   RDD flat (tuplas pixel) : {count_flat:,} registros")
    print(f"   Factor de expansión     : {count_flat // count_original}x (10 píxeles/imagen)")
    if count_flat == count_original * 10:
        print(f"   Verificación            : {count_original:,} × 10 = {count_original * 10:,} ✅")

    print("\nPASO 3: Primeros 5 elementos del RDD aplanado")
    print("Formato: (image_id, pixel_index, pixel_value)")
    print("-" * 50)
    for image_id, pixel_idx, pixel_val in rdd_pixels_flat.take(5):
        print(f"   ({image_id:5d}, pixel[{pixel_idx:2d}], {pixel_val:.6f})")

    # ============================================================
    # SECCIÓN 4: distinct y sortBy
    # ============================================================
    #
    # distinct: elimina duplicados de un RDD
    # sortBy:   ordena los elementos del RDD por una clave
    #
    # Cuándo usar distinct: extraer categorías únicas, limpiar datos
    # Cuándo usar sortBy:   rankings, reportes ordenados, visualizaciones
    #
    # ============================================================

    print("\n" + "=" * 60)
    print("SECCIÓN 4: distinct y sortBy")
    print("=" * 60)

    print("\n" + "=" * 60)
    print("PASO 1: Extraer categorías únicas con distinct()")
    print("=" * 60)

    # map para extraer solo el label_name → luego distinct() para valores únicos
    rdd_categorias = (
        rdd_base
        .map(lambda r: r["label_name"])  # Extraer nombre de categoría
        .distinct()                       # Eliminar duplicados
    )

    categorias_unicas = sorted(rdd_categorias.collect())  # collect() trae al driver
    print(f"   Número de categorías únicas: {len(categorias_unicas)}")
    print(f"   Categorías: {categorias_unicas}")

    print("\n" + "=" * 60)
    print("PASO 2: Contar imágenes por clase con map + reduceByKey")
    print("=" * 60)

    # map: cada registro genera una tupla (nombre_clase, 1)
    # reduceByKey: suma los unos agrupando por clave (nombre_clase)
    rdd_label_counts = (
        rdd_base
        .map(lambda r: (r["label_name"], 1))  # (clase, 1) por cada imagen
        .reduceByKey(lambda a, b: a + b)       # Sumar conteos por clase
    )

    print("\n" + "=" * 60)
    print("PASO 3: Ordenar de mayor a menor frecuencia con sortBy")
    print("=" * 60)

    # sortBy(lambda x: x[1], ascending=False): ordena por el conteo, descendente
    rdd_sorted = rdd_label_counts.sortBy(lambda x: x[1], ascending=False)

    ranking = rdd_sorted.collect()  # Trae al driver los resultados ordenados

    print("   Ranking de clases por frecuencia (mayor → menor):")
    print(f"   {'Pos':>4} {'Clase':15s} {'Imágenes':>10} {'%':>8}")
    print("   " + "-" * 42)
    total_imagenes = sum(c for _, c in ranking)
    for pos, (clase, conteo) in enumerate(ranking, 1):
        barra = "█" * int(conteo / total_imagenes * 30)
        print(f"   {pos:>4} {clase:15s} {conteo:>10,} {conteo/total_imagenes*100:>7.1f}% {barra}")

    # Visualización con matplotlib
    clases  = [clase  for clase, _ in ranking]
    conteos = [conteo for _, conteo in ranking]
    colores = plt.cm.tab10(np.linspace(0, 1, len(clases)))

    fig, ax = plt.subplots(figsize=(10, 6))
    barras = ax.barh(clases[::-1], conteos[::-1], color=colores, edgecolor="white", linewidth=0.5)

    for barra, conteo in zip(barras, conteos[::-1]):
        ax.text(
            barra.get_width() + 10,
            barra.get_y() + barra.get_height() / 2,
            f"{conteo:,}",
            va="center", ha="left", fontsize=9
        )

    media_ideal = total_imagenes / len(clases)
    ax.axvline(media_ideal, color="red", linestyle="--", linewidth=1.2,
               label=f"Media ideal ({media_ideal:.0f} imgs/clase)")

    ax.set_xlabel("Número de imágenes", fontsize=11)
    ax.set_title(
        f"Distribución de clases en Fashion-MNIST\n"
        f"(RetailMax · {total_imagenes:,} imágenes · Lección 3)",
        fontsize=13, fontweight="bold"
    )
    ax.legend(fontsize=9)
    ax.set_xlim(0, max(conteos) * 1.15)
    ax.grid(axis="x", linestyle=":", alpha=0.5)
    ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    plt.savefig("distribucion_clases.png", dpi=120, bbox_inches="tight")
    plt.show()
    print("\n📊 Gráfico guardado como 'distribucion_clases.png'")

    # ============================================================
    # SECCIÓN 5: PAIR RDDs y reduceByKey
    # ============================================================
    #
    # ¿Qué es un Pair RDD?
    # Un RDD cuyos elementos son tuplas (clave, valor).
    # Habilita operaciones especiales: reduceByKey, groupByKey, mapValues
    #
    # Diferencia reduceByKey vs groupByKey:
    #   - reduceByKey combina localmente PRIMERO → eficiente
    #   - groupByKey mueve TODOS los valores al shuffle → costoso
    #
    # ============================================================

    print("\n" + "=" * 60)
    print("SECCIÓN 5: PAIR RDDs y reduceByKey")
    print("=" * 60)

    print("\nPASO 1: Crear Pair RDD (label_name, pixel_mean)")

    # map: cada imagen → tupla (nombre_clase, media_pixel)
    rdd_pair_means = rdd_base.map(lambda r: (
        r["label_name"],                               # Clave: nombre de la clase
        sum(r["pixels"]) / len(r["pixels"])            # Valor: media de los 784 píxeles
    ))

    print("🔍 Primeros 4 elementos del Pair RDD:")
    for clase, mean_val in rdd_pair_means.take(4):
        print(f"   ({clase!r:15s}, {mean_val:.6f})")

    print("\nPASO 2: Calcular (suma, conteo) por clase con reduceByKey")

    # Paso 2a: Crear (clase, (media_pixel, 1))
    rdd_pair_sum_count = rdd_base.map(lambda r: (
        r["label_name"],
        (sum(r["pixels"]) / len(r["pixels"]), 1)
    ))

    # Paso 2b: reduceByKey suma ambos componentes del par
    rdd_aggregated = rdd_pair_sum_count.reduceByKey(
        lambda a, b: (a[0] + b[0], a[1] + b[1])   # Sumar suma y conteo por separado
    )

    print("   Valores intermedios (suma_media, conteo) por clase:")
    for clase, (suma, cnt) in sorted(rdd_aggregated.collect(), key=lambda x: x[0]):
        print(f"   {clase:15s}: suma={suma:10.4f}, conteo={cnt:,}")

    print("\nPASO 3: Calcular media real con mapValues (suma / conteo)")

    # mapValues: aplica la función solo al valor, sin tocar la clave
    rdd_class_means = (
        rdd_aggregated
        .mapValues(lambda v: v[0] / v[1])   # Media = suma / conteo
        .sortBy(lambda x: x[1], ascending=False)  # Ordenar de mayor a menor media
    )

    print("\nPASO 4: Tabla clase → pixel_mean_promedio")
    resultados_clase = rdd_class_means.collect()

    print(f"\n   {'Clase':15s} {'Media Píxeles':>14} {'Brillo relativo':>16}")
    print("   " + "-" * 50)
    max_mean = max(m for _, m in resultados_clase)
    for clase, media in resultados_clase:
        barra = "█" * int(media / max_mean * 20)
        print(f"   {clase:15s} {media:>14.6f} {barra}")

    clase_mas_brillante = resultados_clase[0]
    clase_mas_oscura    = resultados_clase[-1]
    print(f"\n💡 Interpretación para RetailMax:")
    print(f"   Clase MÁS brillante  : '{clase_mas_brillante[0]}' (media={clase_mas_brillante[1]:.4f})")
    print(f"   Clase MÁS oscura     : '{clase_mas_oscura[0]}' (media={clase_mas_oscura[1]:.4f})")

    # ============================================================
    # SECCIÓN 6: ACCIONES — collect, sum, mean, stdev
    # ============================================================
    #
    # Las acciones DISPARAN la ejecución del DAG.
    # Hasta que no se llama una acción, Spark solo acumula transformaciones.
    #
    # ADVERTENCIA: collect() trae TODOS los datos al driver.
    # Solo usar en datasets que quepan en memoria del driver.
    #
    # Desviación estándar (σ):
    #   σ = √(Σ(xi - μ)² / N)
    #   σ pequeña → valores concentrados cerca de la media
    #   σ grande  → valores muy dispersos
    #
    # ============================================================

    print("\n" + "=" * 60)
    print("SECCIÓN 6: ACCIONES — collect, sum, mean, stdev")
    print("=" * 60)

    print("\nPASO 1: Extraer solo los valores numéricos de medias de píxeles")

    # rdd_pixel_means tiene tuplas (image_id, pixel_mean)
    # Extraemos solo el valor numérico (float) de la media
    rdd_values = rdd_pixel_means.map(lambda x: float(x[1]))
    print(f"   Primeros 5 valores: {rdd_values.take(5)}")

    print("\nPASO 2: count()")
    t0 = time.time()
    n  = rdd_values.count()   # ACCIÓN: dispara ejecución del DAG
    t1 = time.time()
    print(f"   count()         = {n:,} elementos")
    print(f"   Tiempo          : {t1 - t0:.3f} segundos")

    print("\nPASO 3: sum()")
    total_sum = rdd_values.sum()   # ACCIÓN
    print(f"   sum()           = {total_sum:.6f}")

    print("\nPASO 4: mean()")
    global_mean = rdd_values.mean()   # ACCIÓN
    print(f"   mean()          = {global_mean:.6f}")

    print("\nPASO 5: stdev()")
    stdev = rdd_values.stdev()   # ACCIÓN
    print(f"   stdev()         = {stdev:.6f}")
    print(f"   Fórmula: σ = √(Σ(xi - μ)² / N)")

    print("\nPASO 6: max() y min()")
    val_max = rdd_values.max()   # ACCIÓN
    val_min = rdd_values.min()   # ACCIÓN
    print(f"   max()           = {val_max:.6f}")
    print(f"   min()           = {val_min:.6f}")
    print(f"   Rango           = {val_max - val_min:.6f}")

    print("\nRESUMEN ESTADÍSTICO — Medias de píxeles por imagen")
    print("=" * 60)
    resumen = pd.DataFrame([{
        "Estadístico" : "count",
        "Valor"       : f"{n:,}",
        "Descripción" : "Número total de imágenes"
    }, {
        "Estadístico" : "sum",
        "Valor"       : f"{total_sum:.4f}",
        "Descripción" : "Suma total de medias de píxeles"
    }, {
        "Estadístico" : "mean (μ)",
        "Valor"       : f"{global_mean:.6f}",
        "Descripción" : "Media global de las medias de píxeles"
    }, {
        "Estadístico" : "stdev (σ)",
        "Valor"       : f"{stdev:.6f}",
        "Descripción" : "Dispersión de las medias de píxeles"
    }, {
        "Estadístico" : "min",
        "Valor"       : f"{val_min:.6f}",
        "Descripción" : "Imagen más oscura"
    }, {
        "Estadístico" : "max",
        "Valor"       : f"{val_max:.6f}",
        "Descripción" : "Imagen más clara"
    }])
    print(resumen.to_string(index=False))

    # ============================================================
    # SECCIÓN 7: LINAJE DEL RDD (DAG)
    # ============================================================
    #
    # ¿Qué es el DAG? (Directed Acyclic Graph)
    # Representación interna del plan de ejecución de Spark.
    #
    # Por qué Spark lo usa:
    # 1. Lazy Evaluation: acumula transformaciones y optimiza antes de ejecutar
    # 2. Optimización: puede reordenar filtros para reducir datos antes
    # 3. Tolerancia a fallos: puede reconstruir particiones usando el linaje
    #
    # Transformaciones NARROW: cada partición de salida depende de UNA
    #   partición de entrada → map, filter, flatMap → NO requieren shuffle
    #
    # Transformaciones WIDE: cada partición de salida puede depender de
    #   MÚLTIPLES particiones → sortBy, reduceByKey, distinct → requieren shuffle
    #
    # ============================================================

    print("\n" + "=" * 60)
    print("SECCIÓN 7: LINAJE DEL RDD (DAG)")
    print("=" * 60)

    print("\nPASO 1: Construir cadena de transformaciones para el pipeline")

    # Pipeline: rdd_base → map(metadata) → filter(bags) → map(pixel_mean) → sortBy
    rdd_dag_meta = rdd_base.map(lambda r: {
        "image_id"   : r["image_id"],
        "label"      : r["label"],
        "label_name" : r["label_name"],
        "pixels"     : r["pixels"]
    })
    rdd_dag_bags  = rdd_dag_meta.filter(lambda r: r["label"] == 8)
    rdd_dag_means = rdd_dag_bags.map(lambda r: (
        r["image_id"],
        sum(r["pixels"]) / len(r["pixels"])
    ))
    rdd_dag_sorted = rdd_dag_means.sortBy(lambda x: x[1], ascending=True)

    print("\nPASO 2: Inspeccionar el linaje con toDebugString()")
    debug_string = rdd_dag_sorted.toDebugString().decode("utf-8")
    print("\n--- toDebugString() ---")
    print(debug_string)
    print("-" * 40)

    print("\nPASO 3: DAG representado visualmente como texto ASCII")
    print()
    print("  DAG del pipeline RetailMax — Análisis de Bags (label=8):")
    print()
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │  rdd_base                                           │")
    print("  │  sc.parallelize(data, numSlices=4)                  │")
    print("  │  12,000 registros · 4 particiones                   │")
    print("  │  Tipo: ParallelCollectionRDD                        │")
    print("  └──────────────────────┬──────────────────────────────┘")
    print("                         │  NARROW (map)")
    print("                         ▼")
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │  rdd_dag_meta                                       │")
    print("  │  .map(lambda r: {image_id, label, label_name, ...}) │")
    print("  │  12,000 registros · 4 particiones                   │")
    print("  │  Tipo: MapPartitionsRDD                             │")
    print("  └──────────────────────┬──────────────────────────────┘")
    print("                         │  NARROW (filter)")
    print("                         ▼")
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │  rdd_dag_bags                                       │")
    print("  │  .filter(lambda r: r['label'] == 8)                 │")
    print("  │  ≈ 1,200 registros · 4 particiones                  │")
    print("  │  Tipo: MapPartitionsRDD                             │")
    print("  └──────────────────────┬──────────────────────────────┘")
    print("                         │  NARROW (map)")
    print("                         ▼")
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │  rdd_dag_means                                      │")
    print("  │  .map(lambda r: (image_id, pixel_mean))             │")
    print("  │  ≈ 1,200 tuplas (image_id, mean) · 4 particiones    │")
    print("  │  Tipo: MapPartitionsRDD                             │")
    print("  └──────────────────────┬──────────────────────────────┘")
    print("                         │  WIDE (sortBy → shuffle)")
    print("                         ▼")
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │  rdd_dag_sorted                                     │")
    print("  │  .sortBy(lambda x: x[1], ascending=True)            │")
    print("  │  ≈ 1,200 tuplas ordenadas por pixel_mean            │")
    print("  │  Tipo: ShuffledRDD (requiere shuffle entre nodos)   │")
    print("  └──────────────────────┬──────────────────────────────┘")
    print("                         │  ACCIÓN: .collect()")
    print("                         ▼")
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │  Driver: lista Python con resultados                │")
    print("  │  ← AQUÍ se dispara la ejecución del DAG completo   │")
    print("  └─────────────────────────────────────────────────────┘")

    print("\nPASO 4: Ejecutar .collect() y medir tiempo de ejecución")
    t0 = time.time()
    resultados_dag = rdd_dag_sorted.collect()   # ACCIÓN: ejecuta el DAG completo
    t1 = time.time()

    print(f"\n   Ejecución completada en: {t1 - t0:.3f} segundos")
    print(f"   Registros recuperados  : {len(resultados_dag):,}")
    print("\n🔍 Top 5 imágenes de Bag más oscuras (menor pixel_mean):")
    for image_id, mean_val in resultados_dag[:5]:
        print(f"   image_id={image_id:5d} | pixel_mean={mean_val:.6f}")
    print("\n🔍 Top 5 imágenes de Bag más brillantes (mayor pixel_mean):")
    for image_id, mean_val in resultados_dag[-5:]:
        print(f"   image_id={image_id:5d} | pixel_mean={mean_val:.6f}")

    # ============================================================
    # SECCIÓN 8: cache() y persist()
    # ============================================================
    #
    # Por qué cachear:
    # Por defecto, cada acción sobre un RDD recalcula TODO el linaje.
    # Si el mismo RDD se usa en múltiples acciones, esto es muy costoso.
    #
    # cache() = persist(MEMORY_ONLY)
    # persist() con niveles:
    #   MEMORY_ONLY       → RAM (default)
    #   MEMORY_AND_DISK   → RAM + disco si no cabe
    #   DISK_ONLY         → Solo disco
    #   MEMORY_ONLY_2     → RAM con 2 réplicas
    #
    # Cuándo NO cachear: si el RDD se usa solo una vez
    #
    # ============================================================

    print("\n" + "=" * 60)
    print("SECCIÓN 8: cache() y persist()")
    print("=" * 60)

    print("\nPASO 1: Cachear rdd_metadata con .cache()")
    # cache() es LAZY — solo marca el RDD para ser cacheado
    # El caching real ocurre la PRIMERA VEZ que se ejecuta una acción
    rdd_metadata_cached = rdd_metadata.cache()
    print("   rdd_metadata.cache() → RDD marcado para MEMORY_ONLY")

    print("\nPASO 2: Primera ejecución (frío) — cálculo + almacenamiento en cache")
    t_inicio_frio = time.time()
    conteo_frio   = rdd_metadata_cached.count()    # ACCIÓN: calcula + cachea
    t_fin_frio    = time.time()
    tiempo_frio   = t_fin_frio - t_inicio_frio
    print(f"   count() = {conteo_frio:,}")
    print(f"   ⏱️  Tiempo (frío): {tiempo_frio:.4f} segundos")

    print("\nPASO 3: Segunda ejecución (caliente) — solo lectura desde cache")
    t_inicio_caliente = time.time()
    conteo_caliente   = rdd_metadata_cached.count()   # ACCIÓN: lee desde cache
    t_fin_caliente    = time.time()
    tiempo_caliente   = t_fin_caliente - t_inicio_caliente
    print(f"   count() = {conteo_caliente:,}")
    print(f"   ⏱️  Tiempo (caliente): {tiempo_caliente:.4f} segundos")

    print("\nPASO 4: Comparación de tiempos")
    if tiempo_caliente > 0:
        factor = tiempo_frio / tiempo_caliente
    else:
        factor = float("inf")
    print(f"   Tiempo sin cache (frío)    : {tiempo_frio:.4f} s")
    print(f"   Tiempo con cache (caliente): {tiempo_caliente:.4f} s")
    if factor > 1:
        print(f"   El cache fue {factor:.1f}x más rápido")

    print("\n   Ejemplo con persist() y nivel explícito:")
    rdd_test_persist = rdd_test.persist(StorageLevel.MEMORY_AND_DISK)
    _ = rdd_test_persist.count()  # Materializar
    print(f"   rdd_test.persist(MEMORY_AND_DISK) → {rdd_test_persist.count():,} registros")

    # Liberar cache
    rdd_metadata_cached.unpersist()
    rdd_test_persist.unpersist()
    print("\n   Cache liberado con .unpersist()")

    # ============================================================
    # SECCIÓN 9: CERRAR SPARK
    # ============================================================

    print("\n" + "=" * 60)
    print("SECCIÓN 9: CERRAR SPARK")
    print("=" * 60)

    spark.stop()
    print("\n✅ SparkSession detenida correctamente")
    print("   Todos los RDDs han sido eliminados de memoria")
    print("   Los recursos del sistema han sido liberados")

    # ============================================================
    # RESUMEN FINAL
    # ============================================================
    print("\n" + "=" * 60)
    print("RESUMEN DE LA LECCIÓN 3")
    print("=" * 60)
    print()
    print("Operaciones cubiertas:")
    operaciones = [
        ("parallelize()", "Creación",       "No",  "sc.parallelize(data, 4)"),
        ("map()",         "Transformación", "Sí",  "rdd.map(lambda r: ...)"),
        ("filter()",      "Transformación", "Sí",  "rdd.filter(lambda r: cond)"),
        ("flatMap()",     "Transformación", "Sí",  "rdd.flatMap(lambda r: [...])"),
        ("distinct()",    "Transformación", "Sí",  "rdd.distinct()"),
        ("sortBy()",      "Transformación", "Sí",  "rdd.sortBy(lambda x: x[1])"),
        ("reduceByKey()", "Transformación", "Sí",  "rdd.reduceByKey(lambda a,b: a+b)"),
        ("mapValues()",   "Transformación", "Sí",  "rdd.mapValues(lambda v: v/n)"),
        ("cache()",       "Transformación", "Sí",  "rdd.cache()"),
        ("count()",       "Acción",         "No",  "rdd.count()"),
        ("collect()",     "Acción",         "No",  "rdd.collect()"),
        ("sum()",         "Acción",         "No",  "rdd.sum()"),
        ("mean()",        "Acción",         "No",  "rdd.mean()"),
        ("stdev()",       "Acción",         "No",  "rdd.stdev()"),
        ("max()/min()",   "Acción",         "No",  "rdd.max() / rdd.min()"),
    ]
    print(f"   {'Operación':16s} {'Tipo':14s} {'Lazy?':6s} {'Código'}")
    print("   " + "-" * 65)
    for op, tipo, lazy, codigo in operaciones:
        print(f"   {op:16s} {tipo:14s} {lazy:6s} {codigo}")

    print("\n✅ Lección 3 completada.")
    print("   Próxima lección: DataFrames y Spark SQL")


if __name__ == "__main__":
    main()
