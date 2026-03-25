"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   ANÁLISIS DE CASO – Machine Learning Escalable con Apache Spark MLlib      ║
║   Predicción de Compra en E-commerce                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

CONTEXTO:
  Una empresa de e-commerce quiere predecir si un cliente realizará una compra
  en los próximos días, usando datos de navegación, historial y perfil.
  Por el volumen de datos (millones de registros), la solución se implementa
  con Apache Spark MLlib, que permite procesamiento distribuido y escalable.

FLUJO DE TRABAJO:
  Paso 1  → Importar librerías y crear sesión Spark
  Paso 2  → Cargar y explorar los datos (CSV)
  Paso 3  → Limpiar y preparar los datos
  Paso 4  → Vectorizar las características (VectorAssembler)
  Paso 5  → Dividir en Train / Test
  Paso 6  → Entrenar Regresión Logística
  Paso 7  → Entrenar Random Forest
  Paso 8  → Ajuste de hiperparámetros con CrossValidator
  Paso 9  → Evaluar los modelos (AUC-ROC, Accuracy, F1)
  Paso 10 → Informe de resultados y recomendaciones
"""

# ══════════════════════════════════════════════════════════════════════════════
# PASO 1 – Importar librerías y crear la sesión Spark
# ══════════════════════════════════════════════════════════════════════════════
# PySpark es la interfaz Python de Apache Spark.
# SparkSession es el punto de entrada de toda aplicación Spark.

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, isnan, count
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml import Pipeline

# Creamos la sesión Spark (en entorno local usa todos los núcleos disponibles)
spark = SparkSession.builder \
    .appName("EcommercePurchasePrediction") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")   # silenciamos logs innecesarios
print("✅ Paso 1 – Sesión Spark creada correctamente")
print(f"   Versión de Spark: {spark.version}\n")


# ══════════════════════════════════════════════════════════════════════════════
# PASO 2 – Cargar y explorar los datos
# ══════════════════════════════════════════════════════════════════════════════
# Cargamos el dataset maestro, que ya integra clientes, navegación e historial.
# inferSchema=True le pide a Spark que detecte automáticamente los tipos.

print("─" * 60)
print("PASO 2 – Carga y exploración de datos")
print("─" * 60)

df = spark.read.csv("dataset_maestro.csv", header=True, inferSchema=True)

print(f"\n📊 Dimensiones del dataset: {df.count()} filas × {len(df.columns)} columnas\n")

# Verificar valores nulos por columna
# IMPORTANTE: isnan() solo aplica a columnas numéricas (DoubleType, FloatType).
# Para columnas de texto usamos solo isNull().
# Detectamos el tipo de cada columna con df.dtypes y aplicamos la lógica correcta.
print("🔍 Valores nulos por columna:")
from pyspark.sql.types import DoubleType, FloatType

def check_null(col_name, dtype):
    """Cuenta nulos de forma segura según el tipo de columna."""
    if dtype in ("double", "float"):
        # Numéricas de punto flotante: puede haber NaN o NULL
        return count(when(isnan(col(col_name)) | col(col_name).isNull(), col_name)).alias(col_name)
    else:
        # Enteros y strings: solo puede haber NULL (isnan no aplica)
        return count(when(col(col_name).isNull(), col_name)).alias(col_name)

df.select([
    check_null(c, t) for c, t in df.dtypes
]).show(vertical=True)

# Distribución del target
print("📈 Distribución de la variable objetivo 'comprara':")
df.groupBy("comprara").count().orderBy("comprara").show()

# Estadísticas descriptivas de las variables numéricas clave
print("📋 Estadísticas descriptivas (variables numéricas clave):")
df.select(
    "edad", "antiguedad_dias", "paginas_vistas_7d", "visitas_7d",
    "items_carrito", "compras_30d", "ticket_promedio"
).describe().show()


# ══════════════════════════════════════════════════════════════════════════════
# PASO 3 – Limpieza y preparación de datos
# ══════════════════════════════════════════════════════════════════════════════
# Seleccionamos SOLO las columnas numéricas relevantes para el modelo.
# Las variables categóricas ya fueron codificadas numéricamente en el CSV
# (genero_cod, membresia_cod, region_cod, categoria_cod).

print("─" * 60)
print("PASO 3 – Selección y limpieza de variables")
print("─" * 60)

# Variables predictoras (features) – elegidas por su relevancia de negocio
FEATURES = [
    # Perfil del cliente
    "edad",
    "antiguedad_dias",
    "genero_cod",          # 0=M, 1=F, 2=Otro
    "membresia_cod",       # 0=Bronce, 1=Plata, 2=Oro
    "region_cod",
    # Comportamiento de navegación
    "paginas_vistas_7d",
    "tiempo_sesion_min",
    "visitas_7d",
    "busquedas_7d",
    "items_carrito",
    "abandono_carrito",
    "categoria_cod",
    # Historial de compras
    "compras_30d",
    "compras_90d",
    "ticket_promedio",
    "devolucion_30d",
    "calificacion_promedio",
    "descuento_usado",
]

TARGET = "comprara"   # 1 = comprará, 0 = no comprará

# Seleccionamos solo las columnas que usaremos
df_modelo = df.select(FEATURES + [TARGET]).dropna()

print(f"\n✅ Variables seleccionadas: {len(FEATURES)} features + 1 target")
print(f"   Filas tras limpiar nulos: {df_modelo.count()}\n")


# ══════════════════════════════════════════════════════════════════════════════
# PASO 4 – Vectorización de características (VectorAssembler)
# ══════════════════════════════════════════════════════════════════════════════
# MLlib requiere que TODAS las features estén en UN SOLO vector por fila.
# VectorAssembler concatena las columnas seleccionadas en una columna "features".
#
# EJEMPLO:
#   edad=25, visitas_7d=10, items_carrito=3, …
#   → features = DenseVector([25.0, 10.0, 3.0, …])

print("─" * 60)
print("PASO 4 – Vectorización (VectorAssembler + StandardScaler)")
print("─" * 60)

assembler = VectorAssembler(inputCols=FEATURES, outputCol="features_raw")

# StandardScaler normaliza cada feature para media=0 y std=1.
# Esto es especialmente importante para Regresión Logística.
#   x_norm = (x − μ) / σ
scaler = StandardScaler(
    inputCol="features_raw",
    outputCol="features",
    withMean=True,
    withStd=True
)

print("✅ VectorAssembler y StandardScaler configurados\n")


# ══════════════════════════════════════════════════════════════════════════════
# PASO 5 – División Train / Test
# ══════════════════════════════════════════════════════════════════════════════
# Dividimos los datos: 80 % para entrenamiento, 20 % para evaluación.
# seed=42 garantiza reproducibilidad (siempre la misma división).

print("─" * 60)
print("PASO 5 – División Train / Test (80 % / 20 %)")
print("─" * 60)

train_df, test_df = df_modelo.randomSplit([0.8, 0.2], seed=42)

print(f"   Conjunto de entrenamiento : {train_df.count()} registros")
print(f"   Conjunto de prueba        : {test_df.count()} registros\n")


# ══════════════════════════════════════════════════════════════════════════════
# PASO 6 – Modelo 1: Regresión Logística
# ══════════════════════════════════════════════════════════════════════════════
# La Regresión Logística calcula la probabilidad de compra con la fórmula:
#
#   P(compra=1) = 1 / (1 + e^(−(β₀ + β₁x₁ + β₂x₂ + …)))
#
# Si P > 0.5  → predice "comprará" (clase 1)
# Si P ≤ 0.5  → predice "no comprará" (clase 0)
#
# maxIter=100 es el número máximo de iteraciones del optimizador.
# regParam=0.1 es el término de regularización (evita sobreajuste).

print("─" * 60)
print("PASO 6 – Entrenamiento: Regresión Logística")
print("─" * 60)

lr = LogisticRegression(
    featuresCol="features",
    labelCol=TARGET,
    maxIter=100,
    regParam=0.1,
    elasticNetParam=0.0   # 0=Ridge, 1=Lasso
)

# Pipeline: encadena assembler → scaler → modelo en un solo flujo
pipeline_lr = Pipeline(stages=[assembler, scaler, lr])

print("⏳ Entrenando Regresión Logística…")
model_lr = pipeline_lr.fit(train_df)
print("✅ Modelo de Regresión Logística entrenado\n")


# ══════════════════════════════════════════════════════════════════════════════
# PASO 7 – Modelo 2: Random Forest
# ══════════════════════════════════════════════════════════════════════════════
# Random Forest crea múltiples árboles de decisión y los combina por votación.
# Ventajas: robusto al sobreajuste, no requiere normalización.
#
# numTrees=100 → entrenamos 100 árboles y promediamos sus predicciones
# maxDepth=5   → profundidad máxima de cada árbol (controla complejidad)

print("─" * 60)
print("PASO 7 – Entrenamiento: Random Forest")
print("─" * 60)

rf = RandomForestClassifier(
    featuresCol="features_raw",   # RF no necesita normalización
    labelCol=TARGET,
    numTrees=100,
    maxDepth=5,
    seed=42
)

# Pipeline solo con assembler para RF (sin scaler)
pipeline_rf = Pipeline(stages=[assembler, rf])

print("⏳ Entrenando Random Forest…")
model_rf = pipeline_rf.fit(train_df)
print("✅ Modelo Random Forest entrenado\n")


# ══════════════════════════════════════════════════════════════════════════════
# PASO 8 – Ajuste de hiperparámetros con Cross-Validation
# ══════════════════════════════════════════════════════════════════════════════
# CrossValidator divide el conjunto de entrenamiento en K=3 partes (folds).
# Para cada combinación de hiperparámetros, entrena en K-1 partes y evalúa
# en la parte restante. Elige la configuración con mejor AUC-ROC promedio.
#
# ParamGrid define el espacio de búsqueda:
#   regParam ∈ {0.01, 0.1, 0.5}  ×  maxIter ∈ {50, 100}  → 6 combinaciones

print("─" * 60)
print("PASO 8 – Ajuste de hiperparámetros (CrossValidator, 3-fold)")
print("─" * 60)

# Re-definimos un LR fresco para la búsqueda
lr_cv = LogisticRegression(featuresCol="features", labelCol=TARGET)
pipeline_cv = Pipeline(stages=[assembler, scaler, lr_cv])

param_grid = (
    ParamGridBuilder()
    .addGrid(lr_cv.regParam,  [0.01, 0.1, 0.5])
    .addGrid(lr_cv.maxIter,   [50, 100])
    .build()
)

evaluator_auc = BinaryClassificationEvaluator(
    labelCol=TARGET,
    metricName="areaUnderROC"
)

cv = CrossValidator(
    estimator=pipeline_cv,
    estimatorParamMaps=param_grid,
    evaluator=evaluator_auc,
    numFolds=3,
    seed=42
)

print("⏳ Ejecutando validación cruzada (6 combinaciones × 3 folds = 18 entrenamientos)…")
cv_model = cv.fit(train_df)

# Mejores hiperparámetros encontrados
best_lr = cv_model.bestModel.stages[-1]
print(f"\n✅ Mejor regParam : {best_lr.getRegParam()}")
print(f"   Mejor maxIter  : {best_lr.getMaxIter()}\n")


# ══════════════════════════════════════════════════════════════════════════════
# PASO 9 – Evaluación de los modelos
# ══════════════════════════════════════════════════════════════════════════════
# Métricas usadas:
#   AUC-ROC : área bajo la curva ROC (1.0 = perfecto, 0.5 = aleatorio)
#             Mide qué tan bien el modelo separa clases positivas de negativas.
#   Accuracy: porcentaje de predicciones correctas.
#   F1-Score: media armónica entre Precisión y Recall.
#             Útil cuando las clases están desbalanceadas.

print("─" * 60)
print("PASO 9 – Evaluación de los modelos en Test")
print("─" * 60)

evaluator_acc = MulticlassClassificationEvaluator(labelCol=TARGET, metricName="accuracy")
evaluator_f1  = MulticlassClassificationEvaluator(labelCol=TARGET, metricName="f1")

def evaluar_modelo(modelo, nombre, test_data):
    preds = modelo.transform(test_data)
    auc  = evaluator_auc.evaluate(preds)
    acc  = evaluator_acc.evaluate(preds)
    f1   = evaluator_f1.evaluate(preds)
    print(f"\n  {'='*38}")
    print(f"  Modelo: {nombre}")
    print(f"  {'='*38}")
    print(f"  AUC-ROC  : {auc:.4f}  {'★★★' if auc>0.85 else '★★' if auc>0.75 else '★'}")
    print(f"  Accuracy : {acc:.4f}  ({acc*100:.1f}%)")
    print(f"  F1-Score : {f1:.4f}")
    return {"modelo": nombre, "AUC-ROC": round(auc,4),
            "Accuracy": round(acc,4), "F1-Score": round(f1,4)}

resultados = []
resultados.append(evaluar_modelo(model_lr,  "Regresión Logística",    test_df))
resultados.append(evaluar_modelo(model_rf,  "Random Forest",          test_df))
resultados.append(evaluar_modelo(cv_model,  "LR + CrossValidation",   test_df))

# Importancia de variables (Random Forest)
print("\n\n📊 Importancia de variables – Random Forest:")
rf_model = model_rf.stages[-1]
feature_imp = sorted(
    zip(FEATURES, rf_model.featureImportances.toArray()),
    key=lambda x: x[1], reverse=True
)
print(f"  {'Variable':<25} {'Importancia':>12}")
print(f"  {'-'*25} {'-'*12}")
for feat, imp in feature_imp:
    bar = "█" * int(imp * 200)
    print(f"  {feat:<25} {imp:>10.4f}  {bar}")


# ══════════════════════════════════════════════════════════════════════════════
# PASO 10 – Informe de resultados y recomendaciones
# ══════════════════════════════════════════════════════════════════════════════
print("\n\n" + "═" * 60)
print("  PASO 10 – INFORME FINAL")
print("═" * 60)

print("""
RESUMEN DEL FLUJO DE TRABAJO:
──────────────────────────────
1. Cargamos 1 000 registros de clientes de e-commerce con 18 features.
2. Vectorizamos y normalizamos las características con VectorAssembler
   y StandardScaler (pipeline reproducible).
3. Entrenamos y comparamos dos algoritmos:
   - Regresión Logística (modelo lineal, interpretable)
   - Random Forest      (ensemble, más flexible)
4. Optimizamos la Regresión Logística con CrossValidator (3-fold).
5. Evaluamos con AUC-ROC, Accuracy y F1-Score sobre el conjunto de test.

RECOMENDACIONES PARA MEJORAR EL MODELO:
────────────────────────────────────────
★ Más datos reales: con datos verdaderos de producción, los modelos
  aprenderán patrones más complejos y representativos.

★ Feature engineering: crear variables derivadas como
  - "ratio_compras_30d_90d" (tendencia de compra)
  - "ticket_promedio × descuento_usado" (interacción)
  puede mejorar significativamente el AUC.

★ Probar GBTClassifier: Gradient Boosted Trees de MLlib suele
  superar a Random Forest en datos tabulares de e-commerce.

★ Manejo de desbalance: si el target fuera muy desbalanceado,
  usar weightCol o sobremuestreo (SMOTE).

★ Monitoreo continuo: re-entrenar el modelo mensualmente para
  capturar cambios en el comportamiento de los clientes.

★ Infraestructura: en producción, escalar a un clúster Databricks
  o EMR de AWS para procesar millones de registros con el mismo código.
""")

print("✅ Script completado exitosamente.")
spark.stop()
