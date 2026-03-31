# =============================================================================
# RETAIL ANALYTICS PIPELINE — MÓDULO 9
# Lección 3: Transformaciones RDD — map, filter, flatMap, distinct, sortBy,
#             Pair RDDs, reduceByKey, acciones, DAG y cache
# Empresa ficticia: RetailMax (e-commerce de moda)
# Dataset: Fashion-MNIST (estadísticas precalculadas — SIN array de píxeles)
# Entorno: VS Code Windows · .venv_spark · Python 3.10 · PySpark
# =============================================================================
# RESTRICCIÓN CRÍTICA: El RDD base NO contiene la clave "pixels".
# Cada registro tiene EXACTAMENTE:
#   image_id, label, label_name, split,
#   pixel_mean, pixel_std, pixel_max, pixel_min
# NUNCA usar r["pixels"] en ninguna celda de este notebook.
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 0 — Configuración inicial y carga de datos
# ─────────────────────────────────────────────────────────────────────────────

# Paso 0.1 — Importaciones y variables de entorno de Hadoop
import os, sys, time
import numpy as np

# HADOOP_HOME debe configurarse ANTES de importar pyspark
os.environ["HADOOP_HOME"]     = r"D:\hadoop"         # ruta de winutils.exe
os.environ["hadoop.home.dir"] = r"D:\hadoop"         # alias requerido por Spark
os.environ["PATH"]            = r"D:\hadoop\bin;" + os.environ.get("PATH", "")

# Paso 0.2 — Crear la SparkSession (punto de entrada único en Spark 2+)
from pyspark.sql import SparkSession

spark = (SparkSession.builder
         .master("local[*]")                              # usar todos los núcleos locales
         .appName("RetailMax_L3_RDDs")                   # nombre en la Spark UI
         .config("spark.driver.memory", "2g")            # memoria del driver
         .config("spark.sql.shuffle.partitions", "4")    # particiones para shuffles
         .config("spark.ui.showConsoleProgress", "false") # silenciar barra de progreso
         .getOrCreate())                                  # reutilizar sesión existente si hay una

sc = spark.sparkContext   # SparkContext: API de RDDs de bajo nivel
sc.setLogLevel("ERROR")   # sólo mostrar errores, no warnings ni INFO

print("✓ SparkSession creada correctamente")
print(f"  Versión Spark : {spark.version}")
print(f"  App ID        : {sc.applicationId}")

# Paso 0.3 — Diccionario de etiquetas Fashion-MNIST
label_names = {
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
print(f"✓ {len(label_names)} clases de ropa registradas")

# Paso 0.4 — Carga de Fashion-MNIST con fallback en cadena
#            TensorFlow → PyTorch (torchvision) → scikit-learn → datos sintéticos
X_train = X_test = y_train = y_test = None   # inicializar como None

# Intento 1: TensorFlow / Keras
try:
    import tensorflow as tf
    (X_train, y_train), (X_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
    print("✓ Datos cargados con TensorFlow/Keras")
except Exception as e_tf:
    print(f"  TensorFlow no disponible: {e_tf}")

    # Intento 2: PyTorch + torchvision
    try:
        import torchvision, torch
        ds_train = torchvision.datasets.FashionMNIST(
            root="./data", train=True,  download=True)
        ds_test  = torchvision.datasets.FashionMNIST(
            root="./data", train=False, download=True)
        X_train = ds_train.data.numpy()
        y_train = ds_train.targets.numpy()
        X_test  = ds_test.data.numpy()
        y_test  = ds_test.targets.numpy()
        print("✓ Datos cargados con PyTorch/torchvision")
    except Exception as e_pt:
        print(f"  PyTorch no disponible: {e_pt}")

        # Intento 3: scikit-learn (OpenML)
        try:
            from sklearn.datasets import fetch_openml
            fmnist = fetch_openml("Fashion-MNIST", version=1, as_frame=False, parser="auto")
            X_all  = fmnist.data.reshape(-1, 28, 28).astype(np.uint8)
            y_all  = fmnist.target.astype(int)
            X_train, y_train = X_all[:60000], y_all[:60000]
            X_test,  y_test  = X_all[60000:], y_all[60000:]
            print("✓ Datos cargados con scikit-learn / OpenML")
        except Exception as e_sk:
            print(f"  scikit-learn no disponible: {e_sk}")

            # Fallback final: datos sintéticos reproducibles
            print("⚠ Usando datos SINTÉTICOS (ninguna biblioteca ML disponible)")
            rng = np.random.default_rng(seed=42)            # semilla fija para reproducibilidad
            # 60 000 imágenes 28×28 de entrenamiento
            X_train = rng.integers(0, 256, (60000, 28, 28), dtype=np.uint8)
            y_train = rng.integers(0, 10, 60000, dtype=np.uint8)
            # 10 000 imágenes 28×28 de test
            X_test  = rng.integers(0, 256, (10000, 28, 28), dtype=np.uint8)
            y_test  = rng.integers(0, 10, 10000, dtype=np.uint8)

print(f"  X_train shape: {X_train.shape}  y_train shape: {y_train.shape}")
print(f"  X_test  shape: {X_test.shape}   y_test  shape: {y_test.shape}")

# Paso 0.5 — Normalizar valores de píxel al rango [0, 1]
#            Las imágenes crudas tienen valores uint8 en [0, 255]
if X_train.max() > 1.0:
    X_train = X_train.astype(np.float32) / 255.0   # 0-255 → 0.0-1.0
    X_test  = X_test.astype(np.float32)  / 255.0   # ídem para test
    print("✓ Píxeles normalizados a [0, 1]")

# Paso 0.6 — Construir registros estadísticos SIN columna "pixels"
#            Cada imagen → 1 diccionario con 8 campos (estadísticas agregadas)
def construir_registro(i, X, y, split):
    """
    Convierte la imagen i en un dict con estadísticas precalculadas.
    NO incluye el array de píxeles para mantener el RDD ligero.
    """
    px = X[i]                                          # array 2D (28,28) de float32
    return {
        "image_id":   int(i) if split == "train" else int(60000 + i),
        "label":      int(y[i]),
        "label_name": label_names[int(y[i])],          # nombre legible de la clase
        "split":      split,                           # "train" o "test"
        "pixel_mean": float(np.mean(px)),              # brillo promedio
        "pixel_std":  float(np.std(px)),               # varianza del brillo
        "pixel_max":  float(np.max(px)),               # píxel más brillante
        "pixel_min":  float(np.min(px)),               # píxel más oscuro
    }

# Usar subconjunto para agilizar el notebook en entorno local
N_TRAIN, N_TEST = 10_000, 2_000

# Construir lista plana de registros (train + test)
data = (
    [construir_registro(i, X_train, y_train, "train") for i in range(N_TRAIN)] +
    [construir_registro(i, X_test,  y_test,  "test")  for i in range(N_TEST)]
)

# Paso 0.7 — Paralelizar en un RDD distribuido
rdd_base = sc.parallelize(data, numSlices=4)   # 4 particiones → 4 tasks en local[*]

print(f"\n✓ RDD base creado")
print(f"  Total registros  : {rdd_base.count()}")
print(f"  Particiones      : {rdd_base.getNumPartitions()}")
print(f"  Ejemplo (first()): {rdd_base.first()}")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 1 — Transformación map
# Concepto: aplica una función a CADA elemento → mismo número de elementos
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECCIÓN 1 — Transformación map")
print("="*60)

# Paso 1.1 — Extraer sólo los metadatos de identificación
#            Resultado: RDD de tuplas (image_id, label, label_name, split)
rdd_metadata = rdd_base.map(
    lambda r: (r["image_id"], r["label"], r["label_name"], r["split"])
    # ↑ cada registro → tupla de 4 campos (de 8 originales)
)
print("\n[1.1] Primeros 3 registros de metadatos:")
for rec in rdd_metadata.take(3):
    print(f"  {rec}")

# Paso 1.2 — Calcular "brightness_score" como promedio de mean y max
#            Fórmula: brightness_score = (pixel_mean + pixel_max) / 2
#            Representa el brillo general de la imagen en RetailMax
rdd_brightness = rdd_base.map(
    lambda r: {
        **r,                                                    # conservar todos los campos originales
        "brightness_score": round((r["pixel_mean"] + r["pixel_max"]) / 2, 6)
        #                          ↑ pixel_mean: brillo promedio
        #                                         ↑ pixel_max: píxel más brillante
    }
)
print("\n[1.2] Brightness score — primeros 2 registros (campos relevantes):")
for rec in rdd_brightness.take(2):
    print(f"  image_id={rec['image_id']:>6} | label_name={rec['label_name']:<12} | "
          f"pixel_mean={rec['pixel_mean']:.4f} | pixel_max={rec['pixel_max']:.4f} | "
          f"brightness_score={rec['brightness_score']:.6f}")

# Paso 1.3 — Re-normalizar de [0,1] a [-1,1] usando la fórmula afín
#            Formula: valor_norm = valor * 2 - 1
#            Mini-ejemplo: 0.3 → 0.3*2-1 = -0.4  |  0.8 → 0.8*2-1 = 0.6
print("\n[1.3] Mini-ejemplo de normalización [-1, 1]:")
for v in [0.0, 0.3, 0.5, 0.8, 1.0]:
    print(f"  {v:.1f} → {v*2-1:.2f}")

rdd_normalized = rdd_base.map(
    lambda r: {
        **r,                                                          # campos originales
        "pixel_mean_norm": round(r["pixel_mean"] * 2 - 1, 4),        # media normalizada
        "pixel_std_norm":  round(r["pixel_std"]  * 2 - 1, 4),        # desv. estándar normalizada
    }
)
print("\n  Tabla comparativa (primeros 3 registros):")
print(f"  {'label_name':<14} {'pixel_mean_orig':>16} {'pixel_mean_norm':>16}")
print(f"  {'-'*50}")
for rec in rdd_normalized.take(3):
    print(f"  {rec['label_name']:<14} {rec['pixel_mean']:>16.4f} {rec['pixel_mean_norm']:>16.4f}")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 2 — Transformación filter
# Concepto: selecciona elementos que cumplan una condición booleana
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECCIÓN 2 — Transformación filter")
print("="*60)

total = rdd_base.count()   # total de registros para calcular porcentajes

# Paso 2.1 — Filtrar sólo imágenes de la clase Bag (label == 8)
#            Caso de uso RetailMax: analizar sólo el catálogo de bolsos
rdd_bags = rdd_base.filter(
    lambda r: r["label"] == 8    # label 8 = "Bag" según label_names
)
n_bags = rdd_bags.count()
print(f"\n[2.1] Imágenes de Bag (label=8):")
print(f"  Cantidad : {n_bags}")
print(f"  Porcentaje: {n_bags/total*100:.2f}% del total")
print(f"  Primer registro: {rdd_bags.first()}")

# Paso 2.2 — Filtrar imágenes con brillo promedio superior a 0.5
#            Caso de uso: detectar imágenes "claras" (fondo blanco o prendas claras)
rdd_bright = rdd_base.filter(
    lambda r: r["pixel_mean"] > 0.5    # pixel_mean > 0.5 → imagen relativamente brillante
)
n_bright = rdd_bright.count()
print(f"\n[2.2] Imágenes con pixel_mean > 0.5 (imágenes brillantes):")
print(f"  Cantidad  : {n_bright}")
print(f"  Porcentaje: {n_bright/total*100:.2f}% del total")

# Paso 2.3 — Filtrar sólo el conjunto de test
#            Caso de uso: evaluar métricas solo sobre datos no vistos en entrenamiento
rdd_test = rdd_base.filter(
    lambda r: r["split"] == "test"    # split "test" → imágenes de evaluación
)
n_test = rdd_test.count()
print(f"\n[2.3] Imágenes del split 'test':")
print(f"  Cantidad  : {n_test}")
print(f"  Porcentaje: {n_test/total*100:.2f}% del total")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 3 — Transformación flatMap
# Concepto: 1 elemento de entrada → N elementos de salida (aplanado)
#           Diferencia con map: map produce 1→1, flatMap produce 1→N
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECCIÓN 3 — Transformación flatMap")
print("="*60)
print("Concepto: cada imagen produce 4 tuplas (una por estadística de píxel)")
print("         map:     1 registro → 1 registro")
print("         flatMap: 1 registro → N registros (aquí N=4)")

# Paso 3.1 — Explotar cada registro en 4 tuplas de estadísticas
rdd_pixels_flat = rdd_base.flatMap(
    lambda r: [
        # Tupla: (image_id, label_name, nombre_estadistica, valor)
        (r["image_id"], r["label_name"], "pixel_mean", r["pixel_mean"]),
        (r["image_id"], r["label_name"], "pixel_std",  r["pixel_std"]),
        (r["image_id"], r["label_name"], "pixel_max",  r["pixel_max"]),
        (r["image_id"], r["label_name"], "pixel_min",  r["pixel_min"]),
        # ↑ NUNCA usar r["pixels"] — sólo campos precalculados
    ]
)

# Paso 3.2 — Verificar el factor de expansión 4x
count_original = rdd_base.count()          # número de imágenes
count_flat     = rdd_pixels_flat.count()   # número de tuplas estadísticas

print(f"\n[3.2] Factor de expansión flatMap:")
print(f"  Registros originales : {count_original}")
print(f"  Registros tras flatMap: {count_flat}")
print(f"  Factor               : {count_flat // count_original}x (esperado: 4x)")

# Paso 3.3 — Mostrar las primeras 8 tuplas (= 2 imágenes × 4 estadísticas)
print(f"\n[3.3] Primeras 8 tuplas del RDD aplanado:")
print(f"  {'image_id':>10} {'label_name':<14} {'stat':<12} {'valor':>8}")
print(f"  {'-'*50}")
for tup in rdd_pixels_flat.take(8):
    print(f"  {tup[0]:>10} {tup[1]:<14} {tup[2]:<12} {tup[3]:>8.6f}")

print("\n[3.3] Diferencia map vs flatMap:")
print("  map    → transforma, preserva estructura (1 entrada → 1 salida)")
print("  flatMap→ transforma Y aplana (1 entrada → N salidas concatenadas)")
print("  Uso RetailMax: analizar cada estadística por separado, "
      "filtrar sólo pixel_max, etc.")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 4 — distinct y sortBy
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECCIÓN 4 — distinct y sortBy + visualización")
print("="*60)

# Paso 4.1 — Obtener clases únicas (distinct elimina duplicados)
clases_unicas = rdd_base.map(lambda r: r["label_name"]).distinct().collect()
clases_unicas.sort()   # ordenar alfabéticamente para presentación
print(f"\n[4.1] Clases únicas en el dataset ({len(clases_unicas)} total):")
for c in clases_unicas:
    print(f"  • {c}")

# Paso 4.2 — Contar registros por clase con map + reduceByKey
#            rdd de pares (clase, 1) → suma por clave
rdd_label_counts = (
    rdd_base
    .map(lambda r: (r["label_name"], 1))           # cada registro → (clase, 1)
    .reduceByKey(lambda a, b: a + b)                # sumar los 1s por clase
)

# Paso 4.3 — Ordenar de mayor a menor conteo
rdd_sorted = rdd_label_counts.sortBy(
    lambda x: x[1],    # x = (clase, conteo) → ordenar por conteo
    ascending=False     # mayor conteo primero
)

conteos = rdd_sorted.collect()   # traer al driver como lista de (clase, n)
print(f"\n[4.3] Distribución de clases (ordenada descendente):")
print(f"  {'Clase':<14} {'Conteo':>7}")
print(f"  {'-'*25}")
for clase, n in conteos:
    print(f"  {clase:<14} {n:>7}")

# Paso 4.4 — Visualización: bar chart horizontal con matplotlib
import matplotlib
matplotlib.use("Agg")   # backend sin ventana gráfica (compatible con entornos headless)
import matplotlib.pyplot as plt

clases_graf  = [c[0] for c in conteos]   # etiquetas del eje Y
conteos_graf = [c[1] for c in conteos]   # valores del eje X

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(clases_graf, conteos_graf, color="#4C72B0", edgecolor="white", height=0.7)

# Añadir etiquetas numéricas dentro de cada barra
for bar, val in zip(bars, conteos_graf):
    ax.text(bar.get_width() - max(conteos_graf)*0.02, bar.get_y() + bar.get_height()/2,
            f"{val}", va="center", ha="right", color="white", fontsize=9, fontweight="bold")

ax.set_xlabel("Número de imágenes", fontsize=11)
ax.set_title("RetailMax — Distribución de clases Fashion-MNIST\n(Lección 3: RDD sortBy)", fontsize=12)
ax.set_xlim(0, max(conteos_graf) * 1.08)
ax.invert_yaxis()   # clase con más registros arriba
plt.tight_layout()
plt.savefig("output_leccion3_clases.png", dpi=120, bbox_inches="tight")
plt.show()
print("✓ Gráfico guardado: output_leccion3_clases.png")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 5 — Pair RDDs y reduceByKey
# Concepto: RDD de pares (clave, valor) → operaciones por clave
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECCIÓN 5 — Pair RDDs y reduceByKey")
print("="*60)

# Paso 5.1 — Crear Pair RDD de (clase, pixel_mean)
#            IMPORTANTE: sólo se usa pixel_mean (campo precalculado)
#            NUNCA r["pixels"]
rdd_pair_means = rdd_base.map(
    lambda r: (r["label_name"], r["pixel_mean"])
    # clave  = nombre de clase (str)
    # valor  = pixel_mean (float) — brillo promedio de esa imagen
    # ↑ NO usar r["pixels"] bajo ninguna circunstancia
)
print(f"\n[5.1] Primeros 3 pares (label_name, pixel_mean):")
for par in rdd_pair_means.take(3):
    print(f"  {par}")

# Paso 5.2 — Acumular suma y conteo para calcular media por clase
#            Emitir (clase, (suma_means, count)) y reducir
rdd_pair_sum_count = rdd_base.map(
    lambda r: (r["label_name"], (r["pixel_mean"], 1))
    # valor = (pixel_mean de esta imagen, 1 imagen)
)

rdd_aggregated = rdd_pair_sum_count.reduceByKey(
    lambda a, b: (a[0] + b[0],   # sumar pixel_means
                  a[1] + b[1])    # sumar conteos
)
print(f"\n[5.2] Agregados por clase (suma, conteo) — primeros 3:")
for item in rdd_aggregated.take(3):
    print(f"  {item}")

# Paso 5.3 — Calcular media por clase dividiendo suma / conteo
rdd_class_means = (
    rdd_aggregated
    .mapValues(lambda v: round(v[0] / v[1], 6))    # media = suma / conteo
    .sortBy(lambda x: x[1], ascending=False)        # ordenar de mayor a menor brillo
)

# Paso 5.4 — Tabla con barras ASCII de brillo
class_means_list = rdd_class_means.collect()
print(f"\n[5.4] Brillo promedio por clase de ropa (RetailMax):")
print(f"  {'Clase':<14} {'pixel_mean_avg':>14}  Barra de brillo")
print(f"  {'-'*60}")
max_val = max(v for _, v in class_means_list)
for clase, media in class_means_list:
    barra_len = int((media / max_val) * 30)           # escalar a 30 chars
    barra     = "█" * barra_len + "░" * (30 - barra_len)
    print(f"  {clase:<14} {media:>14.6f}  {barra}")

clase_brillante = class_means_list[0][0]
print(f"\n  → Clase más brillante: {clase_brillante}")
print(f"    Interpretación RetailMax: las imágenes de {clase_brillante} "
      f"tienen mayor brillo promedio,\n    lo que puede indicar fondos claros "
      f"o prendas de color claro en el catálogo.")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 6 — Acciones: count, sum, mean, stdev
# Concepto: las acciones desencadenan la ejecución del DAG y devuelven resultados
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECCIÓN 6 — Acciones de RDD")
print("="*60)

# Crear RDD de valores numéricos (sólo floats de pixel_mean)
# Acción: cualquier operación que devuelva datos al driver
rdd_values = rdd_base.map(lambda r: r["pixel_mean"])   # RDD de float32

print("\n[6.1] Ejecutando acciones sobre rdd_values (pixel_mean):\n")

# count() — número total de elementos
t0 = time.time()
n = rdd_values.count()
t_count = time.time() - t0
print(f"  count()  = {n}           ({t_count:.3f}s)")

# sum() — suma de todos los valores
t0 = time.time()
total_sum = rdd_values.sum()
t_sum = time.time() - t0
print(f"  sum()    = {total_sum:.4f}     ({t_sum:.3f}s)")

# mean() — media aritmética
t0 = time.time()
media = rdd_values.mean()
t_mean = time.time() - t0
print(f"  mean()   = {media:.6f}  ({t_mean:.3f}s)")

# stdev() — desviación estándar de la población
t0 = time.time()
desv = rdd_values.stdev()
t_stdev = time.time() - t0
print(f"  stdev()  = {desv:.6f}  ({t_stdev:.3f}s)")

# max() — valor máximo
t0 = time.time()
maximo = rdd_values.max()
t_max = time.time() - t0
print(f"  max()    = {maximo:.6f}  ({t_max:.3f}s)")

# min() — valor mínimo
t0 = time.time()
minimo = rdd_values.min()
t_min = time.time() - t0
print(f"  min()    = {minimo:.6f}  ({t_min:.3f}s)")

# Mini-ejemplo de la fórmula de desviación estándar
print("\n[6.2] Fórmula desviación estándar (mini-ejemplo):")
muestra = [0.2, 0.4, 0.6, 0.8]
mu      = sum(muestra) / len(muestra)
varianza = sum((x - mu)**2 for x in muestra) / len(muestra)
desv_manual = varianza ** 0.5
print(f"  Datos  : {muestra}")
print(f"  μ (media)    = {mu:.2f}")
print(f"  σ² (varianza) = Σ(xᵢ - μ)² / N = {varianza:.4f}")
print(f"  σ (desv.est.) = √σ² = {desv_manual:.4f}")

# Tabla resumen estadístico
print(f"\n[6.3] Resumen estadístico de pixel_mean en el dataset RetailMax:")
print(f"  {'Estadístico':<12} {'Valor':>12}  {'Tiempo':>8}")
print(f"  {'-'*36}")
stats = [
    ("count",  n,         t_count),
    ("sum",    total_sum, t_sum),
    ("mean",   media,     t_mean),
    ("stdev",  desv,      t_stdev),
    ("max",    maximo,    t_max),
    ("min",    minimo,    t_min),
]
for nombre, valor, t in stats:
    if nombre == "count":
        print(f"  {nombre:<12} {int(valor):>12}  {t:>7.3f}s")
    else:
        print(f"  {nombre:<12} {valor:>12.6f}  {t:>7.3f}s")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 7 — DAG y linaje
# Concepto: Spark construye un grafo de ejecución (DAG) de transformaciones lazy
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECCIÓN 7 — DAG y linaje (toDebugString)")
print("="*60)

# Paso 7.1 — Construir una cadena de transformaciones para visualizar el DAG
rdd_final = (
    rdd_base                                                       # nivel 0: datos crudos
    .map(lambda r: (r["image_id"], r["label"], r["label_name"],
                    r["split"]))                                    # nivel 1: metadata
    .filter(lambda r: r[1] == 8)                                   # nivel 2: sólo Bags
    .map(lambda r: (r[0], r[2], "Bag detectado"))                  # nivel 3: enriquecer
    .sortBy(lambda r: r[0])                                        # nivel 4: ordenar (WIDE)
)

# Paso 7.2 — Obtener representación del DAG
debug_str = rdd_final.toDebugString().decode("utf-8")
print("\n[7.2] toDebugString() — Linaje del RDD:")
print(debug_str)

# Paso 7.3 — Diagrama ASCII del DAG
print("\n[7.3] Diagrama ASCII del DAG de rdd_final:")
print("""
  ┌─────────────────────────────┐
  │   rdd_base (parallelized)   │  ← sc.parallelize() — 4 particiones
  └─────────────┬───────────────┘
                │ NARROW (map)
                ▼
  ┌─────────────────────────────┐
  │   map(metadata tuple)       │  ← 1 registro → 1 tupla (4 campos)
  └─────────────┬───────────────┘
                │ NARROW (filter)
                ▼
  ┌─────────────────────────────┐
  │   filter(label == 8)        │  ← elimina registros que no sean Bag
  └─────────────┬───────────────┘
                │ NARROW (map)
                ▼
  ┌─────────────────────────────┐
  │   map(enriquecer)           │  ← añade texto "Bag detectado"
  └─────────────┬───────────────┘
                │ WIDE (shuffle)
                ▼
  ┌─────────────────────────────┐
  │   sortBy(image_id)          │  ← requiere redistribución de datos
  └─────────────────────────────┘
""")

# Paso 7.4 — Explicación narrow vs wide
print("[7.4] Narrow vs Wide transformations:")
print("""
  NARROW (sin shuffle):
    • map, filter, flatMap, mapValues
    • Cada partición de salida depende de UNA sola partición de entrada
    • Rápidas: no mueven datos entre nodos
    • Ejemplo: map(lambda r: r["pixel_mean"])

  WIDE (con shuffle):
    • reduceByKey, groupByKey, sortBy, join
    • Cada partición de salida puede necesitar datos de MÚLTIPLES particiones
    • Más lentas: implican I/O de red (shuffle)
    • Spark crea un nuevo "stage" en el DAG por cada wide transformation
    • Ejemplo: sortBy(lambda x: x[1], ascending=False)

  Regla práctica RetailMax: minimizar wide transformations en pipelines críticos.
""")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 8 — cache() y persistencia
# Concepto: guardar un RDD en memoria para reutilizarlo sin recomputarlo
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECCIÓN 8 — cache() y persistencia")
print("="*60)

# Paso 8.1 — Medir tiempo SIN cache (recomputa el RDD cada vez)
rdd_sin_cache = rdd_base.filter(lambda r: r["split"] == "train")

print("\n[8.1] SIN cache — dos count() consecutivos:")
t0 = time.time()
n1 = rdd_sin_cache.count()   # primera ejecución: recorre datos desde rdd_base
t1 = time.time() - t0
print(f"  count() #1 = {n1}  →  {t1:.3f}s  (computa desde cero)")

t0 = time.time()
n2 = rdd_sin_cache.count()   # segunda ejecución: vuelve a recorrer datos desde rdd_base
t2 = time.time() - t0
print(f"  count() #2 = {n2}  →  {t2:.3f}s  (vuelve a computar desde cero)")

# Paso 8.2 — Medir tiempo CON cache
rdd_con_cache = rdd_base.filter(lambda r: r["split"] == "train").cache()
#                                                                  ↑ persist(MEMORY_AND_DISK)

print("\n[8.2] CON cache — dos count() consecutivos:")
t0 = time.time()
n3 = rdd_con_cache.count()   # primera llamada: computa Y guarda en memoria
t3 = time.time() - t0
print(f"  count() #1 = {n3}  →  {t3:.3f}s  (computa + guarda en caché)")

t0 = time.time()
n4 = rdd_con_cache.count()   # segunda llamada: lee directamente desde memoria
t4 = time.time() - t0
print(f"  count() #2 = {n4}  →  {t4:.3f}s  (lee desde caché)")

# Comparativa
mejora_primera = (t1 / t3) if t3 > 0 else float("inf")
mejora_segunda = (t2 / t4) if t4 > 0 else float("inf")
print(f"\n[8.3] Comparativa:")
print(f"  {'Escenario':<30} {'1ra vez':>8}  {'2da vez':>8}")
print(f"  {'-'*50}")
print(f"  {'Sin cache':<30} {t1:>7.3f}s  {t2:>7.3f}s")
print(f"  {'Con cache':<30} {t3:>7.3f}s  {t4:>7.3f}s")
print(f"\n  Cuándo usar cache(): cuando el mismo RDD se usa en múltiples acciones")
print(f"  o iteraciones (p.ej., algoritmos de ML iterativos en RetailMax).")

# Liberar caché explícitamente para no consumir memoria innecesariamente
rdd_con_cache.unpersist()
print("  ✓ Caché liberada con unpersist()")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 9 — Guardar RDD a disco con saveAsTextFile
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECCIÓN 9 — Guardar resultados a disco")
print("="*60)

import shutil

RUTA_OUTPUT = "output/leccion3_muestra"   # directorio destino

# Paso 9.1 — Crear RDD ligero: strings en formato CSV
#            Sólo campos básicos + pixel_mean, pixel_std (sin pixel_max, pixel_min para brevedad)
rdd_csv = rdd_base.map(
    lambda r: (
        f"{r['image_id']},"        # image_id
        f"{r['label']},"           # label numérico
        f"{r['label_name']},"      # nombre de clase
        f"{r['split']},"           # train o test
        f"{r['pixel_mean']:.6f},"  # pixel_mean con 6 decimales
        f"{r['pixel_std']:.6f}"    # pixel_std con 6 decimales
    )
)

# Paso 9.2 — Limpiar directorio previo si existe
if os.path.exists(RUTA_OUTPUT):
    shutil.rmtree(RUTA_OUTPUT)      # eliminar directorio y todo su contenido
    print(f"  Directorio previo eliminado: {RUTA_OUTPUT}")

os.makedirs("output", exist_ok=True)   # crear carpeta "output" si no existe

# Paso 9.3 — Guardar como texto con 1 partición (1 archivo part-00000)
rdd_csv.coalesce(1).saveAsTextFile(RUTA_OUTPUT)
#        ↑ coalesce(1): consolidar en un solo archivo antes de guardar

# Paso 9.4 — Agregar cabecera CSV manualmente (Spark no la añade automáticamente)
part = os.path.join(RUTA_OUTPUT, "part-00000")   # ruta del único archivo de datos
header = "image_id,label,label_name,split,pixel_mean,pixel_std"

with open(part, "r", encoding="utf-8") as f:
    contenido = f.read()                           # leer datos existentes

with open(part, "w", encoding="utf-8") as f:
    f.write(header + "\n" + contenido)             # escribir header + datos

print(f"  ✓ Datos guardados en: {RUTA_OUTPUT}/part-00000")

# Verificar primeras líneas del archivo guardado
print(f"\n[9.5] Primeras 5 líneas del archivo guardado:")
with open(part, "r", encoding="utf-8") as f:
    for i, linea in enumerate(f):
        if i >= 5:
            break
        print(f"  {linea.rstrip()}")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 10 — Cierre de Spark e Informe final
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECCIÓN 10 — Informe final y cierre")
print("="*60)

# Tabla resumen de operaciones vistas en esta lección
print("""
┌─────────────────┬──────────────┬───────┬──────────────────────────────────────────────┐
│ Operación       │ Tipo         │ Lazy? │ Para qué sirve en RetailMax                  │
├─────────────────┼──────────────┼───────┼──────────────────────────────────────────────┤
│ map             │ Narrow       │ Sí    │ Enriquecer registros: calcular brightness     │
│ filter          │ Narrow       │ Sí    │ Segmentar catálogo: sólo Bags, sólo test      │
│ flatMap         │ Narrow       │ Sí    │ Explotar estadísticas (1 imagen → 4 filas)    │
│ distinct        │ Wide         │ Sí    │ Obtener clases únicas de producto             │
│ sortBy          │ Wide         │ Sí    │ Ranking de categorías por brillo              │
│ reduceByKey     │ Wide         │ Sí    │ Agregar métricas por categoría de ropa        │
│ mapValues       │ Narrow       │ Sí    │ Aplicar función sólo al valor del par         │
│ count           │ Acción       │ No    │ Contar imágenes por clase/split               │
│ sum/mean/stdev  │ Acción       │ No    │ Estadísticas globales de brillo               │
│ collect         │ Acción       │ No    │ Traer resultados al driver para graficar      │
│ saveAsTextFile  │ Acción       │ No    │ Exportar resultados a disco / S3              │
│ cache           │ Persistencia │ N/A   │ Acelerar pipelines iterativos de ML           │
└─────────────────┴──────────────┴───────┴──────────────────────────────────────────────┘
""")

# Conexión con Lección 4
print("─" * 60)
print("PRÓXIMA LECCIÓN — Lección 4: DataFrames y Spark SQL")
print("─" * 60)
print("""
  En la Lección 4 pasaremos de RDDs de bajo nivel a DataFrames,
  que ofrecen:
    • Schema tipado y optimización automática (Catalyst Optimizer)
    • API de alto nivel similar a pandas
    • Soporte completo de SQL con spark.sql("SELECT ...")
    • Mejor rendimiento gracias al Project Tungsten
    • Integración nativa con Parquet, Delta Lake, etc.

  El RDD base de esta lección se convertirá en DataFrame con:
    df = spark.createDataFrame(rdd_base)
""")

# Checklist de entregables
print("─" * 60)
print("CHECKLIST DE ENTREGABLES")
print("─" * 60)
print("""
  [✓] Sección 0  — SparkSession + carga datos (TF/PT/sklearn/sintéticos)
  [✓] Sección 1  — map: metadata, brightness_score, normalización [-1,1]
  [✓] Sección 2  — filter: Bags, imágenes brillantes, split test
  [✓] Sección 3  — flatMap: 1 imagen → 4 tuplas estadísticas
  [✓] Sección 4  — distinct + sortBy + bar chart horizontal matplotlib
  [✓] Sección 5  — Pair RDDs + reduceByKey + tabla de brillo por clase
  [✓] Sección 6  — Acciones: count, sum, mean, stdev, max, min
  [✓] Sección 7  — DAG toDebugString + diagrama ASCII narrow vs wide
  [✓] Sección 8  — cache(): comparativa de tiempos sin/con caché
  [✓] Sección 9  — saveAsTextFile + header CSV manual
  [✓] Sección 10 — Informe final + conexión Lección 4
""")

# Cierre de SparkSession
print("Cerrando SparkSession...")
spark.stop()
print("✓ SparkSession cerrada. ¡Lección 3 completada!")
