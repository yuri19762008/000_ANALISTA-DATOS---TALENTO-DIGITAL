# 🚀 Retail Analytics Pipeline — Módulo 9: Fundamentos de Big Data

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-3.5-E25A1C?style=flat&logo=apachespark&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-Big%20Data-E25A1C?style=flat&logo=apachespark&logoColor=white)
![Fashion-MNIST](https://img.shields.io/badge/Dataset-Fashion--MNIST-blue?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## 📑 Tabla de Contenidos

1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Arquitectura del Pipeline](#-arquitectura-del-pipeline)
3. [Tecnologías Utilizadas](#-tecnologías-utilizadas)
4. [Estructura del Repositorio](#-estructura-del-repositorio)
5. [Descripción de Cada Lección](#-descripción-de-cada-lección)
   - [Lección 1 — Fundamentos de Big Data](#lección-1--fundamentos-de-big-data)
   - [Lección 2 — Apache Spark Configuración](#lección-2--apache-spark-configuración)
   - [Lección 3 — RDDs Transformaciones y Acciones](#lección-3--rdds-transformaciones-y-acciones)
   - [Lección 4 — DataFrames y Spark SQL](#lección-4--dataframes-y-spark-sql)
   - [Lección 5 — MLlib Pipeline](#lección-5--mllib-pipeline)
6. [Dataset: Fashion-MNIST](#-dataset-fashion-mnist)
7. [Instalación y Configuración](#️-instalación-y-configuración)
8. [Resultados Obtenidos](#-resultados-obtenidos)
9. [Conclusiones](#-conclusiones)
10. [Referencias](#-referencias)
11. [Autor y Licencia](#-autor-y-licencia)

---

## 📝 Descripción del Proyecto

**Retail Analytics Pipeline** es un proyecto integral de Big Data y Machine Learning desarrollado como parte del Módulo 9 — Fundamentos de Big Data del bootcamp de Data Science de **Talento Digital / Alkemy**. El proyecto simula un escenario real de la empresa ficticia **RetailMax**, un e-commerce de gran escala que procesa millones de transacciones diarias y necesita herramientas escalables para analizar su catálogo de productos, segmentar su inventario y generar insights accionables para el área de marketing.

Utilizando el dataset **Fashion-MNIST** (70,000 imágenes de 28×28 píxeles distribuidas en 10 categorías de ropa y accesorios) como proxy del catálogo de productos de RetailMax, el proyecto construye un pipeline completo de extremo a extremo: desde la ingesta y exploración de datos con Apache Spark, pasando por transformaciones con RDDs y DataFrames, hasta la implementación de modelos de Machine Learning con Spark MLlib para clasificación binaria y segmentación de productos.

El objetivo principal es demostrar cómo las tecnologías de Big Data — en particular Apache Spark y PySpark — permiten escalar el procesamiento analítico más allá de las limitaciones de herramientas tradicionales como pandas, construyendo pipelines reproducibles, eficientes y listos para producción.

---

## 🏗 Arquitectura del Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    RETAIL ANALYTICS PIPELINE — RetailMax                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ┌──────────────┐    ┌──────────────────┐    ┌─────────────────────────────┐   │
│   │              │    │                  │    │                             │   │
│   │ Fashion-MNIST│───▶│  Ingesta (L1-L2) │───▶│   RDD Transformaciones (L3) │   │
│   │  70K imgs    │    │  SparkContext     │    │   map, filter, flatMap      │   │
│   │  28×28 px    │    │  SparkSession     │    │   Pair RDDs, reduceByKey    │   │
│   │              │    │                  │    │                             │   │
│   └──────────────┘    └──────────────────┘    └──────────────┬──────────────┘   │
│                                                              │                  │
│                                                              ▼                  │
│   ┌──────────────────────────────────────────────────────────────────────────┐   │
│   │                                                                          │   │
│   │                    DataFrames & Spark SQL (L4)                            │   │
│   │         StructType/StructField  ·  groupBy/agg  ·  SQL Queries           │   │
│   │              Métricas de negocio  ·  Exportación Parquet                  │   │
│   │                                                                          │   │
│   └──────────────────────────────────┬───────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│   ┌──────────────────────────────────────────────────────────────────────────┐   │
│   │                                                                          │   │
│   │                        MLlib Pipeline (L5)                               │   │
│   │     VectorAssembler  ·  StandardScaler  ·  Regresión Logística           │   │
│   │              K-Means (k=3)  ·  Evaluación de métricas                    │   │
│   │                                                                          │   │
│   └──────────────────────────────────┬───────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│                        ┌──────────────────────────┐                             │
│                        │  📊 Insights Marketing   │                             │
│                        │  Segmentación de productos│                             │
│                        │  Clasificación de catálogo│                             │
│                        │  Recomendaciones negocio  │                             │
│                        └──────────────────────────┘                             │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Flujo resumido:**

```
Fashion-MNIST ──▶ Ingesta (SparkContext) ──▶ RDDs (L3) ──▶ DataFrames/SQL (L4)
                                                                    │
                                                                    ▼
                   Insights Marketing  ◀── MLlib (L5) ◀── Parquet Storage
```

---

## 🛠 Tecnologías Utilizadas

| Tecnología | Versión | Uso en el Proyecto |
|---|---|---|
| **Python** | 3.10 | Lenguaje principal de desarrollo |
| **Apache Spark / PySpark** | 3.5.x | Motor de procesamiento distribuido para Big Data |
| **Spark MLlib** | 3.5.x | Biblioteca de Machine Learning distribuido (clasificación y clustering) |
| **Spark SQL** | 3.5.x | Consultas SQL sobre DataFrames distribuidos |
| **NumPy** | 1.24+ | Manipulación numérica y carga del dataset Fashion-MNIST |
| **Pandas** | 2.0+ | Exploración y análisis tabular complementario |
| **Matplotlib** | 3.7+ | Visualización de datos y gráficos estáticos |
| **Seaborn** | 0.12+ | Visualizaciones estadísticas avanzadas |
| **TensorFlow/Keras** | 2.x | Carga del dataset Fashion-MNIST (`keras.datasets`) |
| **Fashion-MNIST** | — | Dataset de 70,000 imágenes de ropa y accesorios (10 clases) |
| **Apache Parquet** | — | Formato columnar para almacenamiento eficiente de resultados |
| **Jupyter Notebook** | — | Entorno interactivo de desarrollo y documentación |

---

## 📁 Estructura del Repositorio

```
retail-analytics-pipeline/
│
├── README.md                                  # Documentación principal del proyecto
├── LICENSE                                    # Licencia MIT
│
├── leccion1_fundamentos_bigdata.ipynb         # Notebook: Fundamentos de Big Data y EDA
├── leccion1_fundamentos_bigdata.py            # Script Python equivalente
│
├── leccion2_spark_configuracion.ipynb         # Notebook: Configuración de Spark
├── leccion2_spark_configuracion.py            # Script Python equivalente
│
├── leccion3_rdd_transformaciones_v2.ipynb     # Notebook: RDDs — Transformaciones y Acciones
├── leccion3_rdd_transformaciones_v2.py        # Script Python equivalente
│
├── leccion4_dataframes_sql.ipynb              # Notebook: DataFrames y Spark SQL
├── leccion4_dataframes_sql.py                 # Script Python equivalente
│
├── leccion5_mllib_pipeline.ipynb              # Notebook: MLlib Pipeline (ML distribuido)
├── leccion5_mllib_pipeline.py                 # Script Python equivalente
│
└── output/                                    # Directorio de resultados generados
    ├── leccion2_muestra/                      # CSV de muestra generado en Lección 2
    │   └── *.csv                              # Archivos CSV particionados
    ├── leccion4_fashion_data.parquet           # Dataset completo en formato Parquet
    ├── leccion4_metricas.parquet               # Métricas de negocio calculadas
    ├── leccion5_predicciones_lr.parquet        # Predicciones del modelo de Regresión Logística
    └── leccion5_clusters_km.parquet            # Asignaciones de clusters K-Means
```

---

## 📚 Descripción de Cada Lección

### Lección 1 — Fundamentos de Big Data

**Objetivo:** Comprender los conceptos fundamentales de Big Data y realizar un análisis exploratorio inicial del dataset Fashion-MNIST en el contexto de RetailMax.

**Conceptos clave aprendidos:**
- Las **5V del Big Data**: Volumen, Velocidad, Variedad, Veracidad y Valor, aplicadas al escenario de un e-commerce con millones de transacciones.
- Diferencia entre procesamiento batch y streaming.
- Arquitectura general de un pipeline de datos: ingesta → procesamiento → almacenamiento → análisis → visualización.
- Ecosistema Hadoop y el rol de Apache Spark como motor de procesamiento en memoria.

**Técnicas y código implementado:**
- Carga del dataset Fashion-MNIST utilizando `tensorflow.keras.datasets`.
- Análisis exploratorio de datos (EDA): distribución de clases, visualización de imágenes de ejemplo, estadísticas descriptivas de los valores de píxeles.
- Visualizaciones con Matplotlib y Seaborn: histogramas de distribución, grillas de imágenes por categoría, heatmaps de intensidad promedio.
- Mapeo de las 10 clases del dataset a categorías de productos de RetailMax.

**Entregable:** `leccion1_fundamentos_bigdata.ipynb` / `.py`

---

### Lección 2 — Apache Spark Configuración

**Objetivo:** Instalar y configurar Apache Spark en un entorno local Windows, crear la primera SparkSession y SparkContext, y validar el funcionamiento con operaciones básicas sobre RDDs.

**Conceptos clave aprendidos:**
- **SparkSession** como punto de entrada unificado a Spark (desde Spark 2.0+).
- **SparkContext** como componente interno que gestiona la conexión con el clúster (modo local en este caso).
- Concepto de **RDD (Resilient Distributed Dataset)** como la abstracción fundamental de Spark.
- Configuración de `HADOOP_HOME` y `winutils.exe` para compatibilidad en Windows.
- Modo de ejecución `local[*]` para aprovechar todos los cores disponibles.

**Técnicas y código implementado:**
- Creación y configuración de `SparkSession` con `SparkSession.builder`.
- Generación de RDDs a partir de listas Python con `sc.parallelize()`.
- Acciones básicas: `count()`, `take()`, `collect()`, `first()`.
- Exportación de una muestra de datos a formato CSV.
- Verificación de la UI de Spark en `http://localhost:4040`.

**Entregable:** `leccion2_spark_configuracion.ipynb` / `.py`, `output/leccion2_muestra/` (CSV)

---

### Lección 3 — RDDs Transformaciones y Acciones

**Objetivo:** Dominar las transformaciones y acciones sobre RDDs, comprender la evaluación perezosa (lazy evaluation) y el grafo acíclico dirigido (DAG), y trabajar con Pair RDDs para operaciones clave-valor.

**Conceptos clave aprendidos:**
- **Transformaciones** (lazy): `map()`, `filter()`, `flatMap()`, `distinct()`, `sortBy()`, `groupByKey()`, `reduceByKey()`, `mapValues()`.
- **Acciones** (eager): `count()`, `collect()`, `take()`, `reduce()`, `countByKey()`, `saveAsTextFile()`.
- **Lazy evaluation**: las transformaciones no se ejecutan hasta que se invoca una acción, permitiendo a Spark optimizar el plan de ejecución.
- **DAG (Directed Acyclic Graph)**: Spark construye un grafo de dependencias entre transformaciones para optimizar la ejecución y tolerancia a fallos.
- **Pair RDDs**: RDDs de tuplas (clave, valor) que habilitan operaciones de agregación por clave.
- **Persistencia con `cache()`**: almacenar RDDs intermedios en memoria para evitar recálculos costosos.
- Diferencia conceptual entre **transformaciones estrechas** (narrow) y **amplias** (wide/shuffle).

**Técnicas y código implementado:**
- Aplanamiento de imágenes 28×28 a vectores de 784 dimensiones con `map()`.
- Filtrado de categorías específicas de productos con `filter()`.
- Creación de Pair RDDs `(label, pixel_data)` para agregar estadísticas por categoría.
- Cálculo de intensidad promedio de píxeles por categoría con `reduceByKey()`.
- Uso de `cache()` en RDDs frecuentemente reutilizados.
- Análisis del DAG a través de `toDebugString()`.
- Operaciones con `distinct()` para identificar categorías únicas y `sortBy()` para ordenar resultados.

**Entregable:** `leccion3_rdd_transformaciones_v2.ipynb` / `.py`

---

### Lección 4 — DataFrames y Spark SQL

**Objetivo:** Migrar el procesamiento de RDDs a DataFrames de Spark, definir esquemas explícitos, ejecutar consultas SQL sobre los datos y calcular métricas de negocio relevantes para RetailMax.

**Conceptos clave aprendidos:**
- **DataFrames** como abstracción tabular de alto nivel optimizada por el Catalyst Optimizer.
- Definición de esquemas con **`StructType`** y **`StructField`** para tipado explícito.
- Operaciones de agregación con `groupBy()` y `agg()`: count, mean, stddev, min, max.
- **Spark SQL**: registro de DataFrames como vistas temporales y ejecución de consultas SQL estándar.
- Ventajas de DataFrames sobre RDDs: optimización automática, API declarativa, interoperabilidad con SQL.
- **Apache Parquet** como formato columnar eficiente para almacenamiento y lectura de datos tabulares.
- Concepto de **Catalyst Optimizer** y cómo optimiza los planes de ejecución lógicos y físicos.

**Técnicas y código implementado:**
- Conversión de datos Fashion-MNIST a DataFrame con esquema definido (`StructType`).
- Consultas SQL para obtener distribución de productos por categoría, estadísticas de intensidad de píxeles, y métricas de negocio.
- Cálculo de métricas de negocio para RetailMax: distribución de inventario, categorías con mayor variabilidad visual, complejidad visual promedio por segmento.
- Exportación de datos procesados a formato Parquet: `leccion4_fashion_data.parquet` y `leccion4_metricas.parquet`.
- Comparación de rendimiento entre operaciones con RDDs y DataFrames.
- Uso de funciones de ventana (`Window`) para rankings y análisis avanzados.

**Entregable:** `leccion4_dataframes_sql.ipynb` / `.py`, `output/leccion4_fashion_data.parquet`, `output/leccion4_metricas.parquet`

---

### Lección 5 — MLlib Pipeline

**Objetivo:** Construir un pipeline completo de Machine Learning distribuido con Spark MLlib, implementando clasificación binaria con Regresión Logística y segmentación de productos con K-Means, generando insights accionables para el equipo de marketing de RetailMax.

**Conceptos clave aprendidos:**
- **Spark ML Pipeline API**: encadenamiento de etapas de preprocesamiento y modelado.
- **`VectorAssembler`**: ensamblaje de múltiples columnas de features en un vector denso.
- **`StandardScaler`**: estandarización de features para mejorar la convergencia de los modelos.
- **Regresión Logística** para clasificación binaria: ropa (T-shirt, Trouser, Pullover, Dress, Coat, Shirt) vs. accesorios (Sandal, Sneaker, Bag, Ankle boot).
- **K-Means** para clustering no supervisado: segmentación de productos en k=3 grupos basados en sus features visuales.
- Métricas de evaluación: **accuracy** para clasificación, **silhouette score** para clustering.
- Exportación de predicciones y asignaciones de clusters a formato Parquet.

**Técnicas y código implementado:**
- Construcción del pipeline: `VectorAssembler` → `StandardScaler` → Modelo.
- Entrenamiento de Regresión Logística con split train/test (80/20).
- Entrenamiento de K-Means con k=3 clusters y análisis de centros de clusters.
- Evaluación del modelo de clasificación con `MulticlassClassificationEvaluator` (accuracy).
- Evaluación del clustering con `ClusteringEvaluator` (silhouette score).
- Interpretación de resultados: perfil de cada cluster, distribución de categorías por cluster.
- Generación de insights para marketing: segmentos de productos con características visuales similares, recomendaciones de agrupación para campañas.
- Exportación de resultados: `leccion5_predicciones_lr.parquet`, `leccion5_clusters_km.parquet`.

**Entregable:** `leccion5_mllib_pipeline.ipynb` / `.py`, `output/leccion5_predicciones_lr.parquet`, `output/leccion5_clusters_km.parquet`

---

## 🗂 Dataset: Fashion-MNIST

### Descripción

**Fashion-MNIST** es un dataset de referencia creado por [Zalando Research](https://github.com/zalandoresearch/fashion-mnist) como alternativa moderna al clásico MNIST de dígitos escritos a mano. Contiene **70,000 imágenes en escala de grises** de 28×28 píxeles, distribuidas en 10 categorías de artículos de moda.

En el contexto de este proyecto, Fashion-MNIST representa el **catálogo visual de productos de RetailMax**, donde cada imagen es una fotografía de producto y cada categoría corresponde a una línea de negocio de la empresa.

### Clases del Dataset

| Label | Clase (inglés) | Categoría RetailMax | Segmento |
|:---:|---|---|---|
| 0 | T-shirt/top | Camisetas y Tops | Ropa |
| 1 | Trouser | Pantalones | Ropa |
| 2 | Pullover | Suéteres y Pullovers | Ropa |
| 3 | Dress | Vestidos | Ropa |
| 4 | Coat | Abrigos y Chaquetas | Ropa |
| 5 | Sandal | Sandalias | Accesorios |
| 6 | Shirt | Camisas | Ropa |
| 7 | Sneaker | Zapatillas deportivas | Accesorios |
| 8 | Bag | Bolsos y Carteras | Accesorios |
| 9 | Ankle boot | Botines | Accesorios |

### Estadísticas del Dataset

| Métrica | Valor |
|---|---|
| Total de imágenes | 70,000 |
| Imágenes de entrenamiento | 60,000 |
| Imágenes de prueba | 10,000 |
| Dimensiones por imagen | 28 × 28 píxeles |
| Canales de color | 1 (escala de grises) |
| Rango de valores de píxel | 0 – 255 |
| Número de clases | 10 |
| Imágenes por clase (aprox.) | 7,000 |
| Total de features por imagen | 784 (28 × 28) |

### Uso en el Proyecto RetailMax

- **Lección 1:** Exploración visual del catálogo de productos, distribución de inventario por categoría.
- **Lección 2:** Ingesta del dataset en Spark como RDD base.
- **Lección 3:** Transformaciones sobre los datos de productos (filtrado por categoría, cálculos de intensidad).
- **Lección 4:** Análisis SQL del catálogo, métricas de negocio por segmento de productos.
- **Lección 5:** Clasificación binaria (ropa vs. accesorios) y segmentación de productos (3 clusters) para campañas de marketing.

---

## ⚙️ Instalación y Configuración

### Prerrequisitos

- **Sistema operativo:** Windows 10/11
- **Python:** 3.10 (instalado y accesible desde `py -3.10`)
- **Java JDK:** 8 u 11 (requerido por Apache Spark)
- **Espacio en disco:** ~2 GB para dependencias y datos

### Pasos de Instalación

#### 1. Clonar el repositorio

```bash
git clone https://github.com/yuri19762008/000_ANALISTA_DATOS/tree/19f48de1c85ca9297d8d296b173bbd9efe679d93/009_BIG_DATA_9/PROYECTO

```

#### 2. Crear entorno virtual con Python 3.10

```bash
py -3.10 -m venv .venv_spark
.venv_spark\Scripts\activate
```

#### 3. Instalar dependencias

```bash
pip install pyspark numpy pandas matplotlib seaborn tensorflow
```

#### 4. Configurar winutils (solo Windows)

Apache Spark requiere `winutils.exe` para funcionar correctamente en Windows:

```bash
# Descargar winutils.exe desde:
# https://github.com/cdarlint/winutils
# Seleccionar la versión compatible con Hadoop 3.x

# Crear el directorio y colocar winutils.exe:
mkdir D:\hadoop\bin
# Copiar winutils.exe a D:\hadoop\bin\winutils.exe
```

#### 5. Configurar variables de entorno HADOOP_HOME

Cada notebook incluye la siguiente configuración en su primera celda para garantizar compatibilidad:

```python
import os
os.environ["HADOOP_HOME"] = r"D:\hadoop"
os.environ["hadoop.home.dir"] = r"D:\hadoop"
```

> **Nota:** Ajustar la ruta `D:\hadoop` según la ubicación elegida en tu sistema.

#### 6. Verificar la instalación

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Test") \
    .master("local[*]") \
    .getOrCreate()

print(f"Spark version: {spark.version}")
print("Instalación exitosa!")

spark.stop()
```

#### 7. Ejecutar los notebooks

Abrir los notebooks en orden secuencial:

```bash
jupyter notebook leccion1_fundamentos_bigdata.ipynb
```

> **Importante:** Ejecutar las lecciones en orden (L1 → L2 → L3 → L4 → L5) ya que algunas dependen de los archivos generados en lecciones anteriores.

---

## 📊 Resultados Obtenidos

### Modelo de Regresión Logística — Clasificación Binaria

Se entrenó un modelo de **Regresión Logística** para clasificar los productos del catálogo de RetailMax en dos segmentos principales:

- **Clase 0 — Ropa:** T-shirt, Trouser, Pullover, Dress, Coat, Shirt
- **Clase 1 — Accesorios:** Sandal, Sneaker, Bag, Ankle boot

| Métrica | Resultado |
|---|---|
| **Accuracy** | ~0.97 |
| Split de datos | 80% entrenamiento / 20% prueba |
| Features utilizados | 784 (píxeles normalizados) |
| Escalado | StandardScaler |

El modelo logra una **alta precisión** distinguiendo entre productos de ropa y accesorios, lo que permite a RetailMax automatizar la categorización inicial de nuevos productos ingresados al catálogo.

### Modelo K-Means — Segmentación de Productos

Se aplicó **K-Means con k=3 clusters** para identificar segmentos naturales de productos basados en sus características visuales:

| Cluster | Perfil identificado | Descripción |
|:---:|---|---|
| 0 | Productos de tonos claros / contornos simples | Artículos con diseños minimalistas, fondos uniformes |
| 1 | Productos de tonos oscuros / alta complejidad | Artículos con texturas detalladas, mayor contraste visual |
| 2 | Productos de complejidad intermedia | Artículos con balance entre simplicidad y detalle |

| Métrica | Resultado |
|---|---|
| **Silhouette Score** | ~0.05 – 0.10 |
| Número de clusters | 3 |
| Algoritmo | K-Means |

> **Nota:** El silhouette score relativamente bajo es esperado dado que las imágenes son de baja resolución (28×28) y las diferencias visuales entre categorías no siempre se capturan completamente con features de píxeles crudos.

### Archivos Parquet Generados

| Archivo | Contenido | Formato |
|---|---|---|
| `output/leccion4_fashion_data.parquet` | Dataset completo procesado con esquema tipado | Parquet |
| `output/leccion4_metricas.parquet` | Métricas de negocio por categoría de producto | Parquet |
| `output/leccion5_predicciones_lr.parquet` | Predicciones del modelo de Regresión Logística | Parquet |
| `output/leccion5_clusters_km.parquet` | Asignaciones de clusters K-Means por producto | Parquet |

### Insights para Marketing de RetailMax

Los resultados del pipeline generan valor directo para el equipo de marketing:

1. **Categorización automática del catálogo:** El modelo de clasificación binaria permite etiquetar automáticamente nuevos productos como "ropa" o "accesorios", agilizando la gestión del inventario.

2. **Segmentación visual de productos:** Los 3 clusters identificados por K-Means revelan agrupaciones naturales basadas en la complejidad visual, permitiendo diseñar campañas diferenciadas:
   - Campañas de productos minimalistas para consumidores de estilo sobrio.
   - Campañas de productos detallados para consumidores de alta gama.
   - Campañas mixtas para el segmento intermedio.

3. **Optimización de la presentación visual:** Conocer las características visuales predominantes de cada segmento permite optimizar las fotografías de productos para mejorar la conversión en el sitio web.

---

## 💡 Conclusiones

### Logros técnicos

A lo largo de las cinco lecciones de este módulo, se construyó un **pipeline completo de Big Data de extremo a extremo**, abarcando desde la ingesta y exploración de datos crudos hasta la generación de modelos de Machine Learning distribuidos y la exportación de resultados en formato Parquet. Este pipeline demuestra que es posible abordar problemas analíticos de escala empresarial utilizando herramientas de código abierto como Apache Spark, incluso desde un entorno de desarrollo local.

El proyecto integra de manera cohesiva las principales abstracciones de Spark: **SparkContext** para la ingesta, **RDDs** para transformaciones de bajo nivel, **DataFrames y Spark SQL** para análisis declarativo, y **MLlib** para Machine Learning distribuido. Esta progresión refleja la evolución natural de un proyecto de datos en un entorno real de producción.

### Apache Spark vs. pandas: escalabilidad

Uno de los aprendizajes más importantes del módulo es comprender **por qué Spark es superior a pandas para grandes volúmenes de datos**. Mientras que pandas carga todo el dataset en la memoria RAM de una sola máquina (lo cual se convierte en un cuello de botella con datasets de millones o miles de millones de registros), Spark distribuye el procesamiento en múltiples particiones que pueden ejecutarse en paralelo a través de un clúster de nodos.

Para el caso de RetailMax, un e-commerce con millones de transacciones diarias, el uso de pandas para analizar el historial completo sería inviable. Spark permite procesar esos volúmenes de forma eficiente, con tolerancia a fallos incorporada y optimización automática del plan de ejecución.

### RDDs vs. DataFrames: cuándo usar cada uno

El proyecto permitió experimentar con ambas abstracciones y entender sus diferencias:

- **RDDs** ofrecen control granular sobre las transformaciones y son ideales para operaciones de bajo nivel o datos no estructurados. Sin embargo, carecen de optimización automática y requieren que el programador gestione explícitamente la eficiencia.

- **DataFrames** proporcionan una API declarativa similar a SQL que el **Catalyst Optimizer** de Spark puede optimizar automáticamente. Son la opción recomendada para la mayoría de los casos de uso en producción, especialmente cuando los datos tienen estructura tabular.

En la práctica, los DataFrames son la abstracción preferida en proyectos modernos de Spark, reservando los RDDs para casos específicos que requieren control total sobre el procesamiento.

### Lazy evaluation como concepto clave

El concepto de **evaluación perezosa (lazy evaluation)** es fundamental para entender cómo Spark logra su eficiencia. Las transformaciones sobre RDDs y DataFrames no se ejecutan inmediatamente; en su lugar, Spark construye un **DAG (Directed Acyclic Graph)** que representa el plan de ejecución completo. Solo cuando se invoca una acción (`count()`, `collect()`, `show()`, `save()`) Spark optimiza el DAG y ejecuta las operaciones necesarias.

Este enfoque permite a Spark:
- **Fusionar operaciones** (pipeline fusion) para reducir pasos intermedios.
- **Eliminar operaciones innecesarias** (predicate pushdown, projection pruning).
- **Reutilizar cálculos intermedios** mediante `cache()` y `persist()`.
- **Recuperarse de fallos** recalculando solo las particiones perdidas a partir del linaje del DAG.

### Aplicabilidad real en e-commerce

Los conceptos y técnicas implementados en este proyecto tienen aplicación directa en empresas de e-commerce reales:

- **Categorización automática de productos:** Los modelos de clasificación pueden integrarse en pipelines de ingesta de catálogo para etiquetar automáticamente productos nuevos subidos por vendedores.
- **Segmentación de inventario:** La segmentación con K-Means permite identificar grupos de productos con características similares para campañas de marketing, recomendaciones cruzadas y optimización de inventario.
- **Análisis a escala:** El uso de Spark SQL y Parquet permite que analistas de negocio ejecuten consultas ad hoc sobre datasets masivos sin necesidad de infraestructura de data warehouse tradicional.
- **Pipelines reproducibles:** La estructura modular del proyecto (lecciones separadas, formatos estándar, esquemas tipados) facilita la reproducción y extensión del análisis.

### Limitaciones del enfoque actual

Es importante reconocer las limitaciones del proyecto en su estado actual:

1. **Entorno local vs. clúster real:** Todo el procesamiento se ejecuta en modo `local[*]` en una sola máquina. En producción, Spark se ejecuta en clústeres distribuidos (YARN, Kubernetes, Databricks) con decenas o cientos de nodos.

2. **Features de píxeles crudos:** Los modelos de ML utilizan los 784 valores de píxeles directamente como features. En un escenario real se utilizarían técnicas de extracción de features más sofisticadas (CNN embeddings, transfer learning) para obtener representaciones más informativas.

3. **Clasificación binaria simplificada:** El modelo de clasificación agrupa 10 clases en solo 2 categorías (ropa vs. accesorios). Un sistema de producción requeriría clasificación multi-clase con mayor granularidad.

4. **Tamaño del dataset:** Aunque Fashion-MNIST es adecuado para aprendizaje, 70,000 registros no representan un desafío real de Big Data. Los beneficios de Spark se manifiestan con datasets de millones o miles de millones de registros.

5. **Ausencia de datos transaccionales reales:** El proyecto utiliza datos de imágenes como proxy de transacciones de e-commerce. Un pipeline real integraría datos transaccionales, de comportamiento de usuarios, inventario y más.

### Próximos pasos sugeridos

Para evolucionar este proyecto hacia un nivel más avanzado, se sugieren los siguientes pasos:

1. **Ingeniería de features avanzada:** Extraer features más representativas utilizando embeddings de redes neuronales convolucionales (CNN) pre-entrenadas, en lugar de usar píxeles crudos.

2. **Clasificación multi-clase:** Extender el modelo de Regresión Logística a las 10 categorías completas, e implementar modelos alternativos como Random Forest o Gradient Boosted Trees disponibles en MLlib.

3. **Cross-validation y tuning de hiperparámetros:** Utilizar `CrossValidator` y `ParamGridBuilder` de Spark MLlib para optimizar los hiperparámetros de los modelos de forma distribuida.

4. **Despliegue en la nube:** Migrar el pipeline a un entorno cloud como **Databricks**, **AWS EMR** o **Google Dataproc** para experimentar con procesamiento distribuido real.

5. **Integración con datos reales:** Incorporar datasets de e-commerce reales (transacciones, clickstream, reviews) para construir un pipeline más representativo del caso de uso de RetailMax.

6. **Orquestación del pipeline:** Implementar herramientas de orquestación como **Apache Airflow** o **Prefect** para automatizar la ejecución secuencial de las etapas del pipeline.

7. **Monitoreo y logging:** Agregar métricas de monitoreo del pipeline (tiempos de ejecución, uso de recursos, calidad de datos) para garantizar la fiabilidad en producción.

---

## 📚 Referencias

- **Apache Spark Official Documentation:** [https://spark.apache.org/docs/latest/](https://spark.apache.org/docs/latest/)
- **Fashion-MNIST — Zalando Research (GitHub):** [https://github.com/zalandoresearch/fashion-mnist](https://github.com/zalandoresearch/fashion-mnist)
- **Spark MLlib Guide:** [https://spark.apache.org/docs/latest/ml-guide.html](https://spark.apache.org/docs/latest/ml-guide.html)
- **Databricks Learning Resources:** [https://www.databricks.com/learn](https://www.databricks.com/learn)
- **PySpark API Reference:** [https://spark.apache.org/docs/latest/api/python/](https://spark.apache.org/docs/latest/api/python/)
- **Apache Parquet Documentation:** [https://parquet.apache.org/documentation/latest/](https://parquet.apache.org/documentation/latest/)

---

## 👤 Autor y Licencia

### Autor

Desarrollado por un estudiante del bootcamp de **Data Science** de **Talento Digital / Alkemy**.

| Campo | Detalle |
|---|---|
| **Programa** | Bootcamp Data Science — Talento Digital / Alkemy |
| **Módulo** | 9 — Fundamentos de Big Data |
| **Proyecto** | Retail Analytics Pipeline |
| **Fecha** | Marzo 2026 |

### Licencia

Este proyecto está licenciado bajo la **Licencia MIT**. Puedes usar, copiar, modificar y distribuir este software libremente, sujeto a las condiciones establecidas en el archivo `LICENSE`.

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  <strong>Retail Analytics Pipeline</strong> · Módulo 9 · Talento Digital / Alkemy
  <br>
  Construido con Apache Spark y Python
</p>

