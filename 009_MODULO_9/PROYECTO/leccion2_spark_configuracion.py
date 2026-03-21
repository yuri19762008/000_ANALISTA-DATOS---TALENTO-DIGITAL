# =============================================================================
# Lección 2: Apache Spark — Introducción y Configuración
# Módulo 9 | Retail Analytics Pipeline | RetailMax E-Commerce
# =============================================================================
#
# PORTADA
# =============================================================================
# Lección 2: Apache Spark — Introducción y Configuración
#
# Módulo 9 | Retail Analytics Pipeline | RetailMax E-Commerce
#
# Recap: ¿Qué vimos en la Lección 1?
#
# En la Lección 1 establecimos los fundamentos del Big Data aplicados a RetailMax:
#
# - Las 5V del Big Data: Volumen, Velocidad, Variedad, Veracidad y Valor.
# - Por qué Fashion-MNIST: 70,000 imágenes de 28x28 px (784 píxeles/imagen)
#   → 54.8 MB solo en píxeles, sin contar metadatos ni etiquetas.
# - Arquitectura distribuida: entendimos la diferencia entre procesamiento
#   monolítico (un solo nodo) y distribuido (múltiples workers en paralelo).
#
# ¿Qué haremos en esta Lección 2?
#
# Paso 1: Verificar el entorno (Python, PySpark, Java)
# Paso 2: Crear una SparkSession configurada para Windows local
# Paso 3: Preparar Fashion-MNIST como datos distribuibles
# Paso 4: Crear un RDD desde datos en memoria
# Paso 5: Ejecutar acciones básicas sobre el RDD
# Paso 6: Guardar resultados en disco
#
# Conexión con Lección 3:
# Una vez que el RDD está creado y validado (lo que hacemos aquí), en la
# Lección 3 aplicaremos transformaciones (map, filter, flatMap, reduceByKey)
# para limpiar, filtrar y agregar los datos de Fashion-MNIST a escala.
# =============================================================================


# =============================================================================
# SECCIÓN 1: ¿QUÉ ES SPARK Y POR QUÉ LO NECESITAMOS?
# =============================================================================
#
# Apache Spark en una línea:
# Apache Spark es un motor de procesamiento distribuido en memoria, diseñado
# para analizar grandes volúmenes de datos de forma paralela y tolerante a fallos.
#
# SparkContext vs. SparkSession
#
# Concepto         | SparkContext            | SparkSession
# -----------------|-------------------------|-----------------------------
# Introducido en   | Spark 1.x               | Spark 2.0+
# Propósito        | RDDs / bajo nivel        | Unificado: RDDs+DF+SQL
# ¿Se usa solo?    | Sí (legado)             | Sí (moderno)
# Acceso al otro   | Independiente            | spark.sparkContext
# ¿Cuándo usar?    | Solo RDDs (legado)       | Siempre en código nuevo
#
# Regla práctica: Crear siempre SparkSession, obtener SparkContext desde ella.
#
# Arquitectura: Driver -> Master -> Workers
#
# ┌─────────────────────────────────────────────────────────────┐
# │                        DRIVER PROGRAM                       │
# │   (Tu script Python / Jupyter Notebook)                     │
# │   SparkContext / SparkSession                               │
# │   ┌─────────────────────────────┐                           │
# │   │  DAG Scheduler              │  ← construye el plan      │
# │   │  Task Scheduler             │  ← distribuye tareas      │
# │   └─────────────────────────────┘                           │
# └───────────────────┬─────────────────────────────────────────┘
#                     │  (envía tareas)
#                     ▼
# ┌─────────────────────────────────────────────────────────────┐
# │                     CLUSTER MANAGER                         │
# │   (en local[*]: el mismo proceso; en prod: YARN/Kubernetes) │
# └───────┬───────────────────┬───────────────────┬─────────────┘
#         │                   │                   │
#         ▼                   ▼                   ▼
# ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
# │   WORKER 1   │  │   WORKER 2   │  │   WORKER N   │
# │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │
# │ │Executor  │ │  │ │Executor  │ │  │ │Executor  │ │
# │ │Task Task │ │  │ │Task Task │ │  │ │Task Task │ │
# │ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │
# │  Partición 0 │  │  Partición 1 │  │  Partición N │
# └──────────────┘  └──────────────┘  └──────────────┘
#
# Hadoop MapReduce vs. Apache Spark
#
# Característica        | Hadoop MapReduce | Apache Spark
# ----------------------|------------------|----------------------
# Almacenamiento interm | Disco (HDFS)     | Memoria RAM
# Velocidad típica      | Línea base (1x)  | 10x–100x más rápido
# API principal         | Java verboso     | Python/Scala/Java fluido
# Evaluación            | Eager            | Lazy (optimiza primero)
# Soporte ML            | Mahout (limitado)| MLlib integrado
# Tolerancia a fallos   | Reescribe disco  | Linaje de RDDs
#
# Mini-ejemplo numérico: calcular promedio de píxeles en 70,000 imágenes:
#   MapReduce: ~45 segundos (lectura/escritura HDFS entre Map y Reduce)
#   Spark (en memoria): ~2 segundos → ~22x más rápido
#
# Modo local vs. clúster:
#   local      → 1 hilo (sin paralelismo real)
#   local[2]   → 2 hilos
#   local[*]   → todos los cores del PC  ← USAMOS ESTO
#   spark://.. → clúster standalone
#   yarn       → Hadoop YARN
#   k8s://..   → Kubernetes
# =============================================================================


# =============================================================================
# SECCIÓN 2: INSTALACIÓN Y VERIFICACIÓN DEL ENTORNO
# =============================================================================

def verificar_entorno():
    """
    Verifica que el entorno tiene Python, PySpark y Java correctamente instalados.
    Imprime un reporte en formato tabla con el estado de cada componente.
    """
    import sys          # Para obtener versión de Python y ruta del intérprete
    import os           # Para leer variables de entorno del sistema operativo
    import subprocess   # Para ejecutar comandos externos (java -version)
    import platform     # Para obtener información del sistema operativo

    print("=" * 60)
    print("   REPORTE DE ENTORNO — RetailMax Analytics Pipeline")
    print("=" * 60)

    # -------------------------------------------------------------------
    # PASO 1: Verificar la versión de Python
    # Spark 3.x requiere Python 3.8+. Recomendamos 3.10+ para compatibilidad.
    # -------------------------------------------------------------------
    python_version = sys.version          # Cadena completa: '3.10.12 (main, ...)'
    python_short   = sys.version_info     # Tupla: (3, 10, 12, 'final', 0)
    python_exec    = sys.executable       # Ruta al intérprete activo (tu .venv)

    print(f"\n{'Componente':<25} {'Estado':<15} {'Detalle'}")
    print("-" * 60)

    # Verificamos que la versión sea al menos 3.8
    if python_short >= (3, 8):
        estado_python = "OK"
    else:
        estado_python = "ACTUALIZAR"

    print(f"{'Python':<25} {estado_python:<15} {python_short.major}.{python_short.minor}.{python_short.micro}")
    print(f"{'  → Ejecutable':<25} {'INFO':<15} {python_exec}")

    # -------------------------------------------------------------------
    # PASO 2: Verificar PySpark
    # Si no está instalado, ejecuta: pip install pyspark en tu .venv
    # -------------------------------------------------------------------
    try:
        import pyspark                          # Intentamos importar PySpark
        pyspark_version = pyspark.__version__   # Leemos la versión instalada
        print(f"{'PySpark':<25} {'OK':<15} {pyspark_version}")
    except ImportError:
        # Si falla: PySpark no está instalado en este entorno virtual
        print(f"{'PySpark':<25} {'NO ENCONTRADO':<15} Ejecuta: pip install pyspark")
        print("\n[ERROR] PySpark no está instalado. Detén aquí y ejecuta:")
        print("        pip install pyspark==3.5.1")
        raise  # Relanzamos la excepción para detener el script

    # -------------------------------------------------------------------
    # PASO 3: Verificar JAVA_HOME
    # Spark requiere una JDK instalada. En Windows, debes tener JAVA_HOME.
    # Descarga JDK 11 desde: https://adoptium.net/
    # -------------------------------------------------------------------
    java_home = os.environ.get("JAVA_HOME", None)  # Leemos la variable de entorno

    if java_home:
        print(f"{'JAVA_HOME':<25} {'OK':<15} {java_home}")
    else:
        # JAVA_HOME no definida: Spark no podrá iniciar
        print(f"{'JAVA_HOME':<25} {'NO DEFINIDA':<15} Ver instrucciones abajo")
        print("\n[ADVERTENCIA] JAVA_HOME no está definida en las variables de entorno.")
        print("  Solución en Windows:")
        print("  1. Instala JDK 11+: https://adoptium.net/")
        print("  2. En Inicio → 'Variables de entorno del sistema'")
        print("  3. Agrega JAVA_HOME = C:\\Program Files\\Eclipse Adoptium\\jdk-11...")
        print("  4. Agrega %JAVA_HOME%\\bin al PATH")
        print("  5. Reinicia VS Code / terminal")

    # -------------------------------------------------------------------
    # Verificamos la versión de Java ejecutando 'java -version' en terminal
    # subprocess.run() ejecuta un comando del sistema operativo desde Python
    # -------------------------------------------------------------------
    try:
        # capture_output=True captura stdout y stderr
        # text=True convierte bytes a string automáticamente
        resultado_java = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True
        )
        # Java imprime su versión en stderr (comportamiento estándar de Java)
        java_info = resultado_java.stderr.split("\n")[0]  # Primera línea del output
        print(f"{'Java (ejecutable)':<25} {'OK':<15} {java_info}")
    except FileNotFoundError:
        # 'java' no está en el PATH: no se puede ejecutar desde la terminal
        print(f"{'Java (ejecutable)':<25} {'NO EN PATH':<15} java no encontrado en PATH")

    # -------------------------------------------------------------------
    # PASO 4: Información adicional del sistema
    # -------------------------------------------------------------------
    so        = platform.system()   # 'Windows', 'Linux' o 'Darwin' (macOS)
    cpu_cores = os.cpu_count()      # Número de núcleos lógicos (hyper-threading)

    print(f"{'Sistema Operativo':<25} {'INFO':<15} {so}")
    print(f"{'Cores disponibles':<25} {'INFO':<15} {cpu_cores} (local[*] usará todos)")
    print("=" * 60)
    print("Verificación completada. Revisa cualquier error antes de continuar.")


# =============================================================================
# SECCIÓN 3: CREAR SPARKSESSION
# =============================================================================
#
# SparkSession: el punto de entrada unificado (Spark 2.0+)
#
# Desde Spark 2.0, SparkSession unifica todos los puntos de entrada anteriores:
#   SparkContext (RDDs) + SQLContext (DataFrames) + HiveContext (Hive)
#
# Parámetros clave:
#
# Parámetro                        | Valor            | Significado
# ----------------------------------|------------------|---------------------------
# master                           | local[*]         | Todos los cores del PC
# appName                          | RetailMax_...    | Visible en Spark UI
# spark.driver.memory              | 2g               | RAM para el Driver (2 GB)
# spark.sql.shuffle.partitions     | 4                | Bajo para modo local
# spark.ui.showConsoleProgress     | false            | Output más limpio
#
# ¿Qué significa local[*]?
#   local      → 1 hilo  (sin paralelismo)
#   local[2]   → 2 hilos (simula 2 workers)
#   local[*]   → TODOS los cores del CPU  ← RECOMENDADO para desarrollo
#
# Spark UI disponible en: http://localhost:4040
# =============================================================================

def crear_spark_session():
    """
    Crea y retorna una SparkSession con configuración optimizada para Windows local.
    Imprime información de la sesión creada y la URL de la Spark UI.
    """
    # PASO 1: Importar los módulos necesarios de PySpark
    from pyspark.sql import SparkSession   # Punto de entrada principal de Spark 2.0+

    # -------------------------------------------------------------------
    # Configuración especial para Windows:
    # En algunos sistemas Windows, Spark necesita winutils.exe para
    # operaciones de archivos. Si ves errores de 'winutils', instala:
    # https://github.com/steveloughran/winutils
    # y define: os.environ["HADOOP_HOME"] = r"C:\ruta\a\winutils"
    # -------------------------------------------------------------------
    # import os
    # os.environ["HADOOP_HOME"] = r"C:\hadoop"  # Descomenta si es necesario

    # PASO 2: Crear la SparkSession con configuración optimizada para desarrollo local
    try:
        spark = (
            SparkSession.builder
            # master: dónde corre Spark. local[*] = todos los cores del PC
            .master("local[*]")
            # appName: nombre que aparece en la Spark UI (localhost:4040)
            .appName("RetailMax_Analytics")
            # Memoria RAM para el proceso Driver (quien coordina todo)
            # Para datasets grandes, aumenta a 4g o 8g según disponibilidad
            .config("spark.driver.memory", "2g")
            # Particiones para operaciones de shuffle (join, groupBy, agg)
            # Valor por defecto: 200. Para local con pocos datos: 4 es suficiente
            .config("spark.sql.shuffle.partitions", "4")
            # Desactivar la barra de progreso en consola (output más limpio)
            .config("spark.ui.showConsoleProgress", "false")
            # getOrCreate(): si ya existe una SparkSession activa, la reutiliza
            .getOrCreate()
        )
        print("SparkSession creada exitosamente.")

    except Exception as e:
        print(f"Error al crear SparkSession: {e}")
        print("\nPosibles causas y soluciones:")
        print("  1. Java no instalado → instala JDK 11+ desde https://adoptium.net/")
        print("  2. JAVA_HOME no definida → revisa la Sección 2")
        print("  3. Puerto 4040 en uso → cierra otras sesiones de Spark")
        print("  4. Memoria insuficiente → reduce spark.driver.memory a '1g'")
        raise

    # -------------------------------------------------------------------
    # PASO 3: Mostrar información de la SparkSession activa
    # Confirmamos que todo está configurado como esperamos
    # -------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("   INFORMACIÓN DE LA SPARKSESSION")
    print("=" * 60)
    print(f"  Versión de Spark : {spark.version}")
    print(f"  Master           : {spark.sparkContext.master}")
    print(f"  App Name         : {spark.sparkContext.appName}")
    print(f"  App ID           : {spark.sparkContext.applicationId}")
    print(f"  Cores disponibles: {spark.sparkContext.defaultParallelism}")
    print("=" * 60)

    # -------------------------------------------------------------------
    # PASO 4: Mostrar la URL de la Spark UI
    # La Spark UI permite visualizar jobs, stages, tasks y consumo de memoria
    # -------------------------------------------------------------------
    spark_ui_url = spark.sparkContext.uiWebUrl  # URL de la interfaz web
    if spark_ui_url:
        print(f"\n  Spark UI disponible en: {spark_ui_url}")
    else:
        print("\n  Spark UI disponible en: http://localhost:4040")
    print("  (Abre esta URL en tu navegador mientras el script esté activo)")
    print("\nSparkSession lista para usar.")

    return spark  # Retornamos la sesión para usarla en las secciones siguientes


# =============================================================================
# SECCIÓN 4: PREPARAR FASHION-MNIST COMO DATOS DISTRIBUIDOS
# =============================================================================
#
# ¿Por qué convertir Fashion-MNIST a un formato que Spark procese?
#
# Fashion-MNIST originalmente viene como archivos binarios IDX o tensores
# de NumPy/PyTorch. Spark no entiende ese formato directamente, pero sí puede
# paralelizar listas de Python.
#
# Estrategia de conversión:
#
# Keras/PyTorch/sklearn
#         │
#         │  cargar Fashion-MNIST
#         ▼
#   NumPy arrays
#   X_train: (60000, 28, 28)  → píxeles
#   y_train: (60000,)         → etiquetas (0-9)
#         │
#         │  convertir cada imagen
#         ▼
#   Lista de diccionarios Python
#   [{image_id, label, label_name, pixels, split}, ...]
#         │
#         │  sc.parallelize()
#         ▼
#   RDD distribuido en N particiones
#   [partición 0] [partición 1] [partición 2] [partición 3]
#
# ¿Por qué solo 10,000 registros en modo local?
#   Fashion-MNIST completo train: 60,000 imágenes × 784 píxeles = ~360 MB en RAM
#   Con 10,000 imágenes: ~60 MB → manejable en cualquier laptop de desarrollo
#
# Etiquetas de Fashion-MNIST → categorías de RetailMax:
#   0: Camiseta_Top   1: Pantalon          2: Sueter
#   3: Vestido         4: Abrigo            5: Sandalia
#   6: Camisa          7: Zapatilla_Deport  8: Bolso_Cartera
#   9: Botin
# =============================================================================

def cargar_fashion_mnist():
    """
    Carga Fashion-MNIST intentando múltiples fuentes:
    1. TensorFlow/Keras
    2. PyTorch/torchvision
    3. scikit-learn/OpenML
    4. Datos sintéticos (fallback)
    Retorna (X_train, y_train, X_test, y_test) como arrays NumPy.
    """
    import numpy as np  # Para manipulación de arrays numéricos

    X_train, y_train, X_test, y_test = None, None, None, None
    fuente_usada = None

    # --- Intento 1: TensorFlow/Keras ---
    try:
        from tensorflow.keras.datasets import fashion_mnist  # Descarga automática
        (X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
        fuente_usada = "TensorFlow/Keras"
        print(f"Dataset cargado desde: {fuente_usada}")
    except ImportError:
        print("  TensorFlow no disponible, intentando PyTorch...")
    except Exception as e:
        print(f"  Error con TensorFlow: {e}. Intentando PyTorch...")

    # --- Intento 2: PyTorch/torchvision ---
    if X_train is None:
        try:
            import torchvision
            import torch

            # Descargar dataset de Fashion-MNIST (se guarda en ./data/)
            train_ds = torchvision.datasets.FashionMNIST(
                root="./data", train=True, download=True,
                transform=torchvision.transforms.ToTensor()
            )
            test_ds = torchvision.datasets.FashionMNIST(
                root="./data", train=False, download=True,
                transform=torchvision.transforms.ToTensor()
            )

            # Convertir tensores PyTorch a arrays NumPy
            X_train = train_ds.data.numpy()    # Shape: (60000, 28, 28)
            y_train = train_ds.targets.numpy() # Shape: (60000,)
            X_test  = test_ds.data.numpy()     # Shape: (10000, 28, 28)
            y_test  = test_ds.targets.numpy()  # Shape: (10000,)
            fuente_usada = "PyTorch/torchvision"
            print(f"Dataset cargado desde: {fuente_usada}")
        except ImportError:
            print("  PyTorch no disponible, intentando scikit-learn...")
        except Exception as e:
            print(f"  Error con PyTorch: {e}. Intentando scikit-learn...")

    # --- Intento 3: scikit-learn + OpenML ---
    if X_train is None:
        try:
            from sklearn.datasets import fetch_openml
            print("  Descargando Fashion-MNIST desde OpenML (puede tardar ~1 min)...")

            # Fashion-MNIST en OpenML tiene ID 40996
            fmnist = fetch_openml(name='Fashion-MNIST', version=1, as_frame=False, parser='auto')
            X = fmnist.data.astype(np.float32)    # Shape: (70000, 784)
            y = fmnist.target.astype(int)         # Shape: (70000,)

            # OpenML devuelve todos los datos juntos; dividimos manualmente
            X_train = X[:60000].reshape(-1, 28, 28)  # Primeros 60,000 → train
            y_train = y[:60000]
            X_test  = X[60000:].reshape(-1, 28, 28)  # Últimos 10,000 → test
            y_test  = y[60000:]
            fuente_usada = "scikit-learn/OpenML"
            print(f"Dataset cargado desde: {fuente_usada}")
        except Exception as e:
            print(f"  Error con sklearn/OpenML: {e}")

    # --- Intento 4: Datos sintéticos (fallback de emergencia) ---
    if X_train is None:
        print("\nNo se pudo cargar Fashion-MNIST real.")
        print("  Generando datos SINTETICOS para continuar la práctica...")
        print("  (En producción, asegúrate de instalar tensorflow o torchvision)")

        # Datos sintéticos con la misma estructura que Fashion-MNIST
        np.random.seed(42)  # Semilla para reproducibilidad
        N_TRAIN, N_TEST = 60000, 10000
        X_train = np.random.randint(0, 256, (N_TRAIN, 28, 28), dtype=np.uint8)
        y_train = np.random.randint(0, 10,  (N_TRAIN,), dtype=np.int64)
        X_test  = np.random.randint(0, 256, (N_TEST,  28, 28), dtype=np.uint8)
        y_test  = np.random.randint(0, 10,  (N_TEST,),  dtype=np.int64)
        fuente_usada = "Datos SINTETICOS (estructura idéntica a Fashion-MNIST)"
        print(f"Usando: {fuente_usada}")

    return X_train, y_train, X_test, y_test, fuente_usada


def preparar_datos(X_train, y_train, fuente_usada, limite=10_000):
    """
    Convierte los arrays NumPy de Fashion-MNIST a una lista de diccionarios
    estructurados para ser paralelizados por Spark.
    Retorna la lista de diccionarios.
    """
    import numpy as np
    import sys as _sys

    # Mapa de etiquetas numéricas (0-9) a nombres de categorías de ropa
    LABEL_NAMES = {
        0: "Camiseta_Top",
        1: "Pantalon",
        2: "Sueter",
        3: "Vestido",
        4: "Abrigo",
        5: "Sandalia",
        6: "Camisa",
        7: "Zapatilla_Deportiva",
        8: "Bolso_Cartera",
        9: "Botin"
    }

    print(f"\nConvirtiendo primeros {limite:,} registros a formato diccionario...")

    data = []  # Lista que contendrá todos los diccionarios

    for i in range(limite):
        imagen_raw  = X_train[i]           # Array NumPy de shape (28, 28)
        imagen_flat = imagen_raw.flatten() # Aplanar a shape (784,)

        # Normalizar píxeles de [0, 255] a [0.0, 1.0]
        # División por 255.0 → cada valor queda entre 0.0 y 1.0
        # Importante para algoritmos de ML que son sensibles a la escala
        pixels_norm = (imagen_flat / 255.0).tolist()  # .tolist() convierte a lista Python

        registro = {
            "image_id"   : i,                          # ID único
            "label"      : int(y_train[i]),             # Etiqueta como int Python
            "label_name" : LABEL_NAMES[int(y_train[i])],  # Nombre de la categoría
            "pixels"     : pixels_norm,                 # Lista de 784 floats [0.0, 1.0]
            "split"      : "train"                      # Partición del dataset
        }
        data.append(registro)  # Agregar a la lista principal

    print("Conversión completada.")

    # -------------------------------------------------------------------
    # PASO 4: Mostrar un ejemplo del diccionario (sin los 784 pixels)
    # Mostramos solo los primeros 5 pixels para no saturar el output
    # -------------------------------------------------------------------
    ejemplo = data[0].copy()               # Copiamos para no modificar el original
    ejemplo["pixels"] = ejemplo["pixels"][:5]  # Solo los primeros 5 pixels
    ejemplo["pixels"].append("... (784 valores en total)")

    print("\n--- Ejemplo de un registro (imagen 0) ---")
    for clave, valor in ejemplo.items():
        print(f"  {clave:<15}: {valor}")

    # -------------------------------------------------------------------
    # PASO 5: Estadísticas del dataset preparado
    # -------------------------------------------------------------------
    num_registros     = len(data)                         # Cantidad de registros
    bytes_por_registro = _sys.getsizeof(data[0])          # Tamaño aproximado por registro
    bytes_total        = bytes_por_registro * num_registros  # Total estimado
    mb_total           = bytes_total / (1024 * 1024)      # Convertir a MB

    print(f"\n--- Estadísticas del dataset preparado ---")
    print(f"  Registros totales   : {num_registros:,}")
    print(f"  Fuente              : {fuente_usada}")
    print(f"  Campos por registro : image_id, label, label_name, pixels (784), split")
    print(f"  Tamaño estimado RAM : ~{mb_total:.1f} MB (referencia)")
    print(f"  Píxeles totales     : {num_registros * 784:,} valores float")

    return data


# =============================================================================
# SECCIÓN 5: CREAR RDD DESDE LOS DATOS
# =============================================================================
#
# ¿Qué es un RDD?
# RDD (Resilient Distributed Dataset) es la estructura de datos fundamental
# de Apache Spark: una colección INMUTABLE, DISTRIBUIDA y TOLERANTE A FALLOS
# de elementos que pueden procesarse en paralelo.
#
# - Resilient: si un worker falla, Spark puede reconstruir los datos usando
#   el LINAJE (registro de transformaciones aplicadas).
# - Distributed: los datos se dividen en PARTICIONES distribuidas entre workers.
# - Dataset: una colección de datos de cualquier tipo Python.
#
# parallelize() vs. textFile():
#
# Método              | Fuente          | Cuándo usarlo
# --------------------|-----------------|----------------------------------
# sc.parallelize()    | Datos en memoria | Datos en Python, pruebas
# sc.textFile("ruta") | Datos en disco   | CSVs/JSONs grandes, HDFS, S3
#
# Concepto de particiones:
#
# Lista de 10,000 registros
# ├── Partición 0: registros [0     – 2,499]  → Worker/Core 0
# ├── Partición 1: registros [2,500 – 4,999]  → Worker/Core 1
# ├── Partición 2: registros [5,000 – 7,499]  → Worker/Core 2
# └── Partición 3: registros [7,500 – 9,999]  → Worker/Core 3
#
# Mini-ejemplo numérico: con 4 particiones y 4 cores, un count():
#   Core 0 cuenta 2,500 → Core 1 cuenta 2,500 → ... → Driver suma: 10,000
# =============================================================================

def crear_rdd(spark, data):
    """
    Crea un RDD desde la lista de diccionarios usando sc.parallelize().
    Retorna el RDD creado.
    """
    # PASO 1: Obtener el SparkContext desde la SparkSession
    # SparkContext (sc) es la conexión de bajo nivel con el motor Spark
    sc = spark.sparkContext  # Accedemos al SparkContext embebido en la SparkSession
    print(f"SparkContext obtenido. App ID: {sc.applicationId}")

    # -------------------------------------------------------------------
    # PASO 2: Crear el RDD usando parallelize()
    # parallelize() toma una lista Python y la distribuye en N particiones
    # numSlices=4 → creamos exactamente 4 particiones
    # -------------------------------------------------------------------
    rdd = sc.parallelize(
        data,         # Lista de 10,000 diccionarios preparada en la Sección 4
        numSlices=4   # Número de particiones (= número de tareas paralelas)
    )
    print("RDD creado con sc.parallelize()")

    # -------------------------------------------------------------------
    # PASO 3: Verificar el número de particiones
    # getNumPartitions() devuelve cuántas particiones tiene el RDD
    # -------------------------------------------------------------------
    num_particiones = rdd.getNumPartitions()  # Debe ser 4 (lo que pedimos)
    print(f"Número de particiones : {num_particiones}")
    print(f"  Registros por partición ≈ {len(data) // num_particiones:,}")

    # -------------------------------------------------------------------
    # PASO 4: Ver el linaje del RDD (toDebugString)
    # El linaje es el grafo de transformaciones que generaron este RDD
    # -------------------------------------------------------------------
    print("\n--- Linaje del RDD (toDebugString) ---")
    linaje_bytes = rdd.toDebugString()  # Devuelve bytes con la representación

    # Decodificamos de bytes a string para mostrar legiblemente
    if isinstance(linaje_bytes, bytes):
        linaje_str = linaje_bytes.decode("utf-8")  # .decode() convierte bytes → str
    else:
        linaje_str = linaje_bytes  # En algunas versiones ya viene como string

    print(linaje_str)
    print("\nInterpretación:")
    print("  ParallelCollectionRDD = RDD creado desde colección Python en memoria")
    print("  [4] = número de particiones")
    print("\nRDD listo para ejecutar acciones y transformaciones.")

    return rdd, sc


# =============================================================================
# SECCIÓN 6: ACCIONES BÁSICAS SOBRE EL RDD
# =============================================================================
#
# Transformaciones vs. Acciones — El corazón de la evaluación Lazy
#
# TRANSFORMACIONES (LAZY — no ejecutan el job):
#   map(f)         → Aplica función f a cada elemento, devuelve nuevo RDD
#   filter(f)      → Filtra elementos donde f devuelve True
#   flatMap(f)     → Como map, pero aplana el resultado
#   groupByKey()   → Agrupa valores por clave
#   reduceByKey(f) → Agrega valores por clave con función f
#
# ACCIONES (EAGER — disparan la ejecución del job):
#   count()        → Número total de elementos (int)
#   take(n)        → Lista con los primeros n elementos
#   first()        → El primer elemento
#   collect()      → TODOS los elementos (cuidado con RAM)
#   countByValue() → Diccionario {valor: frecuencia}
#   takeSample()   → Muestra aleatoria de n elementos
#   saveAsTextFile → Guarda en disco
#
# Analogía:
#   Transformación = planear una receta (escribirla en papel)
#   Acción         = cocinar la receta (usar ingredientes, calor, tiempo)
# =============================================================================

def ejecutar_acciones(rdd):
    """
    Ejecuta las acciones básicas del RDD de Fashion-MNIST y muestra resultados.
    Retorna el total de registros contados.
    """
    import time  # Para medir el tiempo de ejecución de cada acción

    print("=" * 60)
    print("   EJECUTANDO ACCIONES SOBRE EL RDD")
    print("=" * 60)

    # -------------------------------------------------------------------
    # PASO 1: count() — contar total de registros
    # count() es una ACCION: recorre todas las particiones, cuenta
    # los elementos en cada una y suma los resultados en el Driver.
    # -------------------------------------------------------------------
    print("\n[Acción 1] rdd.count()")
    t_inicio = time.time()          # Registramos el tiempo de inicio
    total = rdd.count()             # ← AQUI Spark ejecuta el job
    t_fin = time.time()             # Registramos el tiempo de fin
    tiempo_count = t_fin - t_inicio # Calculamos la duración

    print(f"  Resultado       : {total:,} registros")
    print(f"  Tiempo de ejecución: {tiempo_count:.3f} segundos")
    print(f"  Interpretación: el RDD contiene {total:,} imágenes de Fashion-MNIST")
    print(f"    distribuidas en {rdd.getNumPartitions()} particiones.")

    # -------------------------------------------------------------------
    # PASO 2: take(n) — obtener los primeros N registros
    # take(3) NO trae todos los datos al Driver (eficiente).
    # -------------------------------------------------------------------
    print("\n[Acción 2] rdd.take(3)")
    t_inicio = time.time()
    primeros_3 = rdd.take(3)        # ← AQUI Spark ejecuta el job
    t_fin = time.time()
    tiempo_take = t_fin - t_inicio

    print(f"  Tiempo de ejecución: {tiempo_take:.3f} segundos")
    print("  Primeros 3 registros (sin campo 'pixels' para brevedad):")

    for i, registro in enumerate(primeros_3):
        # Creamos una versión resumida sin los 784 pixels
        resumen = {k: v for k, v in registro.items() if k != "pixels"}
        resumen["pixels_preview"] = f"{registro['pixels'][:3]}... ({len(registro['pixels'])} valores)"
        print(f"  Registro {i}: {resumen}")

    print("  Interpretacion: take(n) es útil para inspeccionar los datos sin")
    print("    traer todo el dataset al Driver (a diferencia de collect()).")

    # -------------------------------------------------------------------
    # PASO 3: first() — obtener el primer registro
    # Equivalente a take(1)[0]. Más expresivo y ligeramente más eficiente.
    # -------------------------------------------------------------------
    print("\n[Acción 3] rdd.first()")
    t_inicio = time.time()
    primer_registro = rdd.first()   # ← AQUI Spark ejecuta el job
    t_fin = time.time()

    print(f"  Tiempo de ejecución: {t_fin - t_inicio:.3f} segundos")
    print("  Primer registro:")
    print(f"    image_id  : {primer_registro['image_id']}")
    print(f"    label     : {primer_registro['label']}")
    print(f"    label_name: {primer_registro['label_name']}")
    print(f"    split     : {primer_registro['split']}")
    print(f"    pixels[0] : {primer_registro['pixels'][0]:.4f} (normalizado de {int(primer_registro['pixels'][0]*255)}/255)")
    print(f"  Interpretacion: esta imagen pertenece a la categoría")
    print(f"    '{primer_registro['label_name']}' (label={primer_registro['label']}).")

    # -------------------------------------------------------------------
    # PASO 4: countByValue() — distribución de clases
    # map() es una TRANSFORMACION (lazy), countByValue() es la ACCION.
    # -------------------------------------------------------------------
    print("\n[Acción 4] rdd_labels.countByValue() — distribución de clases")
    t_inicio = time.time()

    # map() → TRANSFORMACION: crea un nuevo RDD con solo los label_name
    # Aún no ejecuta nada, solo construye el plan
    rdd_labels = rdd.map(lambda x: x["label_name"])

    # countByValue() → ACCION: ejecuta el job y devuelve dict {valor: count}
    distribucion = rdd_labels.countByValue()  # ← AQUI Spark ejecuta
    t_fin = time.time()

    print(f"  Tiempo de ejecución: {t_fin - t_inicio:.3f} segundos")
    print("  Distribución de clases en los 10,000 registros:")
    print(f"  {'Categoría':<25} {'Cantidad':>10} {'Porcentaje':>12}")
    print("  " + "-" * 50)

    # Ordenamos por nombre de categoría para consistencia
    for categoria, cantidad in sorted(distribucion.items()):
        porcentaje = (cantidad / total) * 100
        barra = "#" * int(porcentaje / 2)  # Barra visual proporcional
        print(f"  {categoria:<25} {cantidad:>10,} {porcentaje:>10.1f}%  {barra}")

    print("  Interpretacion: si la distribución es ~1,000 por clase,")
    print("    el dataset está balanceado (ideal para entrenar modelos ML).")

    # -------------------------------------------------------------------
    # PASO 5: takeSample() — muestra aleatoria reproducible
    # takeSample(withReplacement, num, seed)
    #   withReplacement=False → sin repetición
    #   num=5                 → tomamos 5 elementos
    #   seed=42               → semilla para reproducibilidad
    # -------------------------------------------------------------------
    print("\n[Acción 5] rdd.takeSample(False, 5, seed=42) — muestra aleatoria")
    t_inicio = time.time()

    muestra = rdd.takeSample(
        False,   # withReplacement: False = sin reemplazo
        5,       # Número de elementos a tomar
        seed=42  # Semilla para reproducibilidad
    )  # ← AQUI Spark ejecuta el job

    t_fin = time.time()
    print(f"  Tiempo de ejecución: {t_fin - t_inicio:.3f} segundos")
    print("  5 registros aleatorios (campos no-pixels):")
    print(f"  {'#':<4} {'image_id':<12} {'label':<8} {'label_name':<25} {'split'}")
    print("  " + "-" * 60)
    for j, reg in enumerate(muestra):
        print(f"  {j+1:<4} {reg['image_id']:<12} {reg['label']:<8} {reg['label_name']:<25} {reg['split']}")

    print("\n" + "=" * 60)
    print("Todas las acciones ejecutadas correctamente.")
    print("  (Revisa la Spark UI en http://localhost:4040 → pestaña 'Jobs')")

    return total


# =============================================================================
# SECCIÓN 7: GUARDAR RDD A DISCO (CSV)
# =============================================================================
#
# ¿Por qué guardar resultados intermedios?
#
# En un pipeline real de RetailMax, los checkpoints sirven para:
# 1. Tolerancia a fallos: si una etapa posterior falla, no recomputamos
#    desde cero.
# 2. Colaboración: otros equipos pueden usar los resultados.
# 3. Auditoría: tener registros de cada etapa.
# 4. Eficiencia: Spark puede recargar desde disco.
#
# Sobre saveAsTextFile():
# - Guarda UNA LINEA por elemento del RDD como string.
# - Crea UN ARCHIVO por partición: part-00000, part-00001, etc.
# - Requiere que los elementos sean strings.
# =============================================================================

def guardar_rdd(spark, rdd):
    """
    Crea un RDD simplificado (sin pixels), lo convierte a CSV string
    y lo guarda a disco con saveAsTextFile().
    """
    import os        # Para operaciones de sistema de archivos
    import shutil    # Para eliminar directorios completos (rmtree)
    import time      # Para medir tiempo de guardado

    # Obtener el SparkContext
    sc = spark.sparkContext

    # Ruta donde guardaremos el output
    RUTA_OUTPUT = "output/leccion2_muestra"

    # -------------------------------------------------------------------
    # PASO 1: Crear RDD simplificado (solo metadatos, sin pixels)
    # map() → TRANSFORMACION que crea un nuevo RDD desde el original
    # -------------------------------------------------------------------
    rdd_simple = rdd.map(
        lambda x: (x["image_id"], x["label"], x["label_name"], x["split"])
    )  # ← Transformación LAZY: aún no ejecuta nada

    print("RDD simplificado creado (image_id, label, label_name, split)")

    # -------------------------------------------------------------------
    # PASO 2: Convertir tuplas a strings CSV
    # saveAsTextFile() guarda cada elemento como una línea de texto
    # -------------------------------------------------------------------
    rdd_csv = rdd_simple.map(
        lambda t: f"{t[0]},{t[1]},{t[2]},{t[3]}"  # Formato: id,label,nombre,split
    )  # ← Otra transformación LAZY encadenada

    # Añadimos un header (encabezado CSV)
    header_rdd    = sc.parallelize(["image_id,label,label_name,split"])  # RDD de 1 elemento
    rdd_con_header = header_rdd.union(rdd_csv)  # union() concatena dos RDDs

    print("RDD convertido a formato CSV string con header")

    # -------------------------------------------------------------------
    # PASO 3: Manejar directorio existente
    # saveAsTextFile() FALLA si el directorio ya existe.
    # -------------------------------------------------------------------
    if os.path.exists(RUTA_OUTPUT):
        shutil.rmtree(RUTA_OUTPUT)  # Elimina el directorio y todo su contenido
        print(f"Directorio existente eliminado: {RUTA_OUTPUT}")
    else:
        print(f"Directorio de destino limpio: {RUTA_OUTPUT}")

    # Crear directorio padre si no existe
    os.makedirs("output", exist_ok=True)  # exist_ok=True evita error si ya existe

    # -------------------------------------------------------------------
    # PASO 4: Guardar con saveAsTextFile()
    # Esta es una ACCION → dispara la ejecución de todo el plan lazy
    # -------------------------------------------------------------------
    print(f"\nGuardando RDD en: {RUTA_OUTPUT}/")
    print("  (Spark creará un archivo 'part-XXXXX' por cada partición)")

    t_inicio = time.time()
    rdd_con_header.saveAsTextFile(RUTA_OUTPUT)  # ← AQUI Spark ejecuta TODO el pipeline
    t_fin = time.time()

    print(f"Guardado completado en {t_fin - t_inicio:.3f} segundos")

    # -------------------------------------------------------------------
    # PASO 5: Verificar que los archivos se crearon correctamente
    # -------------------------------------------------------------------
    print(f"\n--- Archivos creados en '{RUTA_OUTPUT}/' ---")

    archivos       = sorted(os.listdir(RUTA_OUTPUT))  # Ordenados alfabéticamente
    tamanio_total  = 0

    for archivo in archivos:
        ruta_completa = os.path.join(RUTA_OUTPUT, archivo)  # Ruta completa al archivo
        if os.path.isfile(ruta_completa):
            tamano_bytes = os.path.getsize(ruta_completa)    # Tamaño en bytes
            tamanio_total += tamano_bytes
            print(f"  {archivo:<30} {tamano_bytes:>10,} bytes")
        else:
            print(f"  {archivo:<30} (directorio)")

    archivos_data = [a for a in archivos if not a.startswith('.')]
    print(f"\n  Total: {len(archivos_data)} archivos, "
          f"{tamanio_total:,} bytes ({tamanio_total/1024:.1f} KB)")
    print("\n  Nota: part-00000 tiene el header + datos de la partición 0")
    print("  _SUCCESS = archivo vacío que Spark crea para indicar éxito")

    # Mostrar las primeras 3 líneas del primer archivo de datos
    primer_part = os.path.join(RUTA_OUTPUT, "part-00000")
    if os.path.exists(primer_part):
        print(f"\n  Primeras 3 líneas de part-00000:")
        with open(primer_part, "r", encoding="utf-8") as f:
            for i, linea in enumerate(f):
                if i >= 3:
                    break
                print(f"    {linea.rstrip()}")

    print("\nDatos guardados exitosamente en disco.")


# =============================================================================
# SECCIÓN 8: CERRAR SPARKSESSION
# =============================================================================
#
# Siempre cerrar Spark al terminar para:
# 1. Liberar memoria RAM y recursos del sistema
# 2. Detener el servidor de la Spark UI (puerto 4040)
# 3. Evitar conflictos si vuelves a iniciar Spark en la misma sesión
# =============================================================================

def cerrar_spark(spark):
    """
    Detiene la SparkSession limpiamente y libera todos los recursos.
    """
    print("Cerrando SparkSession...")

    try:
        spark.stop()  # Detiene la SparkSession y libera todos los recursos
        print("SparkSession detenida correctamente.")
        print("  La Spark UI (http://localhost:4040) ya no estará disponible.")
        print("  Para reiniciar Spark, vuelve a llamar a crear_spark_session().")
    except Exception as e:
        # Si ya estaba detenida o hubo un error, lo reportamos sin fallar
        print(f"  Nota al cerrar: {e}")
        print("  (Puede ser que la sesión ya estaba cerrada — no es un error crítico)")

    print("\n" + "=" * 60)
    print("   FIN DE LA LECCION 2")
    print("=" * 60)


# =============================================================================
# SECCIÓN 9: INFORME DE LA LECCIÓN
# =============================================================================
#
# Resumen de lo logrado:
# 1. Entorno verificado: Python 3.10+, PySpark y Java correctamente configurados.
# 2. SparkSession creada con configuración optimizada para Windows local.
# 3. Fashion-MNIST cargado: 10,000 imágenes convertidas a diccionarios Python.
# 4. RDD creado: datos distribuidos en 4 particiones con sc.parallelize().
# 5. Acciones ejecutadas: count, take, first, countByValue, takeSample.
# 6. Resultados guardados: CSV en output/leccion2_muestra/
#
# Tabla de conceptos:
#
# Concepto              | Código usado                  | Para qué sirve en RetailMax
# ----------------------|-------------------------------|------------------------------
# SparkSession          | SparkSession.builder...       | Punto de entrada al pipeline
# Modo local[*]         | .master("local[*]")           | Dev sin clúster
# RDD                   | sc.parallelize(data, 4)       | Distribuir catálogo imágenes
# Particiones           | numSlices=4                   | Dividir trabajo entre cores
# Linaje                | rdd.toDebugString()           | Tolerancia a fallos
# count()               | rdd.count()                   | Validar carga de registros
# take()                | rdd.take(3)                   | Inspeccionar sin sobrecargar RAM
# countByValue()        | rdd_labels.countByValue()     | Detectar desbalance de clases
# takeSample()          | rdd.takeSample(False, 5, 42)  | Muestreo reproducible
# saveAsTextFile        | rdd.saveAsTextFile(ruta)      | Persistir resultados intermedios
# Lazy evaluation       | map() + accion                | Optimizar plan de ejecución
#
# Conexión con Lección 3:
# En la Lección 3 aplicaremos transformaciones sobre el mismo RDD:
#   map()       → normalizar y limpiar píxeles
#   filter()    → filtrar por categoría de ropa
#   flatMap()   → extraer características por píxel
#   reduceByKey → calcular estadísticas por categoría
#   sortBy()    → ordenar resultados
#
# CHECKLIST FINAL:
# [ ] Entorno verificado: Python >= 3.8, PySpark instalado, JAVA_HOME definida
# [ ] SparkSession creada con appName="RetailMax_Analytics" y master="local[*]"
# [ ] Fashion-MNIST cargado y convertido a lista de diccionarios
# [ ] RDD creado con sc.parallelize(data, numSlices=4)
# [ ] rdd.count() ejecutado → resultado: 10,000 registros
# [ ] rdd.take(3) ejecutado → 3 registros inspeccionados
# [ ] countByValue() ejecutado → distribución de clases verificada
# [ ] takeSample() ejecutado → muestra aleatoria reproducible obtenida
# [ ] CSV guardado en output/leccion2_muestra/ con archivos part-XXXXX
# [ ] SparkSession cerrada con spark.stop()
# [ ] Spark UI visitada en http://localhost:4040 durante la ejecución
# =============================================================================


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """
    Función principal que ejecuta todas las secciones de la Lección 2
    en orden secuencial:
    1. Verificación del entorno
    2. Creación de SparkSession
    3. Carga de Fashion-MNIST
    4. Preparación de datos (conversión a dicts)
    5. Creación del RDD
    6. Ejecución de acciones básicas
    7. Guardado a disco
    8. Cierre de SparkSession
    """
    print("\n" + "=" * 60)
    print("   LECCION 2: Apache Spark — Introducción y Configuración")
    print("   Retail Analytics Pipeline | RetailMax E-Commerce")
    print("=" * 60 + "\n")

    # --- SECCIÓN 2: Verificar entorno ---
    print("\n" + "─" * 60)
    print("SECCION 2: Verificación del entorno")
    print("─" * 60)
    verificar_entorno()

    # --- SECCIÓN 3: Crear SparkSession ---
    print("\n" + "─" * 60)
    print("SECCION 3: Crear SparkSession")
    print("─" * 60)
    spark = crear_spark_session()

    # --- SECCIÓN 4: Cargar y preparar Fashion-MNIST ---
    print("\n" + "─" * 60)
    print("SECCION 4: Cargar y preparar Fashion-MNIST")
    print("─" * 60)
    X_train, y_train, X_test, y_test, fuente_usada = cargar_fashion_mnist()
    data = preparar_datos(X_train, y_train, fuente_usada, limite=10_000)

    # --- SECCIÓN 5: Crear RDD ---
    print("\n" + "─" * 60)
    print("SECCION 5: Crear RDD desde los datos")
    print("─" * 60)
    rdd, sc = crear_rdd(spark, data)

    # --- SECCIÓN 6: Acciones básicas ---
    print("\n" + "─" * 60)
    print("SECCION 6: Acciones básicas sobre el RDD")
    print("─" * 60)
    total = ejecutar_acciones(rdd)

    # --- SECCIÓN 7: Guardar a disco ---
    print("\n" + "─" * 60)
    print("SECCION 7: Guardar RDD a disco (CSV)")
    print("─" * 60)
    guardar_rdd(spark, rdd)

    # --- SECCIÓN 8: Cerrar Spark ---
    print("\n" + "─" * 60)
    print("SECCION 8: Cerrar SparkSession")
    print("─" * 60)
    cerrar_spark(spark)

    print("\nLección 2 completada exitosamente.")
    print("Próximo paso: Lección 3 — Transformaciones RDD (map, filter, reduceByKey)")


# =============================================================================
# PUNTO DE ENTRADA DEL SCRIPT
# =============================================================================

if __name__ == "__main__":
    main()
