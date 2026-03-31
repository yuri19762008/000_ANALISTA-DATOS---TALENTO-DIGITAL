# Caso de uso Apache Spark – ShopNow (E‑commerce)

## 1. Contexto y problema

La empresa ficticia **ShopNow** es un e‑commerce regional que registra millones de eventos de navegación y compras al mes. Sus sistemas tradicionales de data warehouse no soportan analizar grandes volúmenes de datos de comportamiento en tiempo casi real: las consultas tardan horas o se caen cuando intentan procesar decenas de millones de filas.

Esto genera varios problemas:
- Recomendaciones genéricas, poco relevantes para cada cliente.
- Dificultad para detectar cambios rápidos en preferencias o productos en tendencia.
- Imposibilidad de reaccionar en minutos ante patrones de fraude o abandono.

Como respuesta, ShopNow decide implementar una solución basada en Apache Spark para construir un motor de recomendaciones escalable y casi en tiempo real.

---

## 2. Cómo se utilizó Apache Spark

### 2.1 Módulos de Spark utilizados

1. **Spark SQL / DataFrames**  
   - Para integrar y consultar datos de compras, catálogo de productos y eventos de navegación.  
   - Permite usar un lenguaje tipo SQL y aprovechar optimizaciones del planificador (Catalyst).

2. **Spark MLlib**  
   - Para entrenar un sistema de recomendación basado en *collaborative filtering* (ALS).  
   - Permite trabajar con grandes matrices usuario–producto de forma distribuida.

3. **Spark Streaming**  
   - Para procesar en micro-lotes los eventos de navegación que llegan en tiempo casi real desde Kafka.  
   - Actualiza métricas recientes (productos más vistos, últimas interacciones) que enriquecen las recomendaciones.

### 2.2 Tipos de datos procesados

- **Datos estructurados**: tabla de compras (id_cliente, id_producto, fecha, monto, canal).  
- **Datos semiestructurados**: eventos de navegación en formato JSON (vistas, clicks, add-to-cart).  
- **Datos de catálogo**: información de cada producto (categoría, marca, precio, disponibilidad).

Ejemplo simplificado de eventos de navegación (JSON):

```json
{
  "id_cliente": "C123",
  "id_producto": "P987",
  "evento": "view",
  "timestamp": "2026-03-12T15:45:00Z"
}
```

---

## 3. Arquitectura implementada (visión general)

### 3.1 Ingesta de datos

- **Streaming**:  
  - Eventos de navegación desde web y app móvil se envían a un *backend* que los publica en tópicos de **Apache Kafka**.  
  - Spark Streaming se suscribe a esos tópicos para procesar los eventos casi en tiempo real.

- **Batch**:  
  - Procesos ETL nocturnos exportan compras históricas desde el ERP/CRM hacia un *data lake* en la nube (por ejemplo, S3).  
  - También se cargan periódicamente tablas de catálogo de productos.

### 3.2 Almacenamiento (data lake en la nube)

El data lake se organiza en zonas:

- **raw**: datos crudos tal como llegan (eventos JSON, dumps de BD).  
- **clean/silver**: datos limpios y tipados (eventos parseados, compras sin duplicados).  
- **curated/gold**: datasets listos para analítica avanzada y modelos ML (tablas de features, segmentos, recomendaciones).

Ejemplo de rutas lógicas en S3:

- `s3://shopnow-datalake/raw/navegacion/`  
- `s3://shopnow-datalake/clean/compras/`  
- `s3://shopnow-datalake/curated/recomendaciones/`

### 3.3 Procesamiento con Spark

1. **Procesamiento batch (offline)**  
   - Spark SQL lee datos de compras y catálogo desde la zona *clean*.  
   - Se construye la matriz usuario–producto y se entrena un modelo ALS en MLlib.  
   - Las recomendaciones base (offline) se guardan en la zona *curated* y/o en una base NoSQL.

2. **Procesamiento streaming (casi en tiempo real)**  
   - Spark Streaming lee micro-lotes desde Kafka.  
   - Calcula métricas recientes (por ejemplo, productos más vistos en los últimos 15 minutos por categoría).  
   - Actualiza tablas/colecciones usadas por la API de recomendaciones.

### 3.4 Capa de consumo

- **API de recomendaciones**: servicio que consume resultados desde una base NoSQL (p. ej. Cassandra o MongoDB) y expone recomendaciones al sitio web y app.  
- **Dashboards de BI**: se conectan a la zona *curated* del data lake para analizar performance de recomendaciones, comportamiento de clientes, etc.

---

## 4. Ventajas obtenidas frente a otras tecnologías

1. **Menor latencia en el procesamiento**  
   - Al trabajar en memoria, Spark reduce significativamente los tiempos de entrenamiento de modelos y de generación de recomendaciones, comparado con soluciones basadas solo en MapReduce.

2. **Ecosistema unificado**  
   - Con Spark SQL, MLlib y Streaming en un solo framework, se evita integrar muchas herramientas distintas para ETL, ML y streaming.

3. **Escalabilidad horizontal**  
   - Al ejecutarse en un clúster en la nube, la empresa puede aumentar nodos según crece el volumen de datos, sin rediseñar toda la arquitectura.

4. **Integración con la nube**  
   - Usando servicios gestionados (EMR, Dataproc, HDInsight), se simplifica la administración de infraestructura y se paga solo por los recursos usados.

---

## 5. Componentes de Spark clave en la solución

1. **Spark SQL / DataFrames**  
   - Permite unificar datos de múltiples fuentes usando un modelo tabular y consultas tipo SQL.  
   - Facilita definiciones declarativas de transformaciones (qué quiero obtener) en lugar de imperativas (cómo hacerlo paso a paso).

2. **Spark MLlib (ALS)**  
   - Proporciona algoritmos de *collaborative filtering* eficientes para grandes datasets de e‑commerce.  
   - Soporta entrenamiento distribuido y evaluación de modelos.

3. **Spark Streaming**  
   - Permite procesar flujos de eventos desde Kafka en micro-lotes, con una API muy similar a la de batch.  
   - Facilita combinar señales offline (historial) con señales online (comportamiento reciente).

4. **Ejecución en clúster**  
   - La arquitectura Driver + Executors y un Cluster Manager (YARN, Standalone, Kubernetes o servicio gestionado) permiten repartir la carga de trabajo.

---

## 6. Desafíos al adoptar Spark

1. **Curva de aprendizaje y tuning**  
   - El equipo debe aprender conceptos como RDD, DataFrames, particiones, ancho de *shuffle*, configuración de memoria y núcleos.

2. **Calidad de datos**  
   - Integrar muchas fuentes genera problemas de datos faltantes, duplicados o inconsistentes, que afectan al rendimiento del modelo de recomendación.

3. **Operación en producción**  
   - Se requiere monitoreo continuo de jobs batch y de streaming, manejo de fallos en Kafka o en el clúster, y *alerting* ante retrasos en los micro-lotes.

4. **Costos en la nube**  
   - Es necesario optimizar el tamaño de los clústeres, programar apagado automático y aprovechar el auto-escalado para controlar gastos.

---

## 7. Reflexión final

Este caso muestra cómo Apache Spark puede ser el corazón de una solución de recomendaciones para e‑commerce, combinando procesamiento batch y streaming, modelos de ML escalables y una arquitectura apoyada en la nube.

A nivel de aprendizaje, te permite practicar:
- Identificación de módulos de Spark adecuados para cada tipo de tarea.
- Diseño de una arquitectura Big Data basada en clúster distribuido y data lake.
- Análisis de beneficios y desafíos reales al adoptar Spark en un contexto empresarial.
