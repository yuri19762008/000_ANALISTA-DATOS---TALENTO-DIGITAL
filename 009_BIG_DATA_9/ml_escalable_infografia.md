# Introducción a Machine Learning Escalable con Spark MLlib

## Resumen ejecutivo

### Propósito del tema
Este material introduce **Spark MLlib** como la biblioteca de *machine learning* de Apache Spark orientada al trabajo con **grandes volúmenes de datos**. Su idea central es que el aprendizaje automático tradicional puede quedarse corto cuando los datos ya no caben en una sola máquina, por lo que se necesita procesamiento distribuido y escalable. 

### Qué aporta MLlib
MLlib permite construir modelos de **clasificación, regresión, clustering, reducción de dimensionalidad y recomendación** dentro del ecosistema Spark. Su valor está en combinar escalabilidad horizontal, ejecución en clústeres e integración con componentes como Spark SQL y Spark Streaming. 

### Estructuras de datos clave
La estructura principal es el **DataFrame**, que organiza datos en columnas distribuidas. Para representar variables numéricas se usan **vectores densos y dispersos**, y para operaciones más avanzadas también se emplean **matrices**. 

### Flujo de trabajo en MLlib
El enfoque de MLlib sigue una secuencia clara: **preparar datos, definir algoritmo, dividir entrenamiento/prueba, entrenar, predecir y evaluar**. Este flujo puede integrarse en un **Pipeline**, lo que mejora la automatización, la reproducibilidad y el mantenimiento del proceso. 

### Algoritmos destacados
En aprendizaje supervisado aparecen modelos como **Regresión Logística, Regresión Lineal, Árboles de Decisión, Random Forest y Gradient-Boosted Trees**. En aprendizaje no supervisado destacan **K-Means, Gaussian Mixture Model (GMM), PCA y SVD**, además de **ALS** para recomendación. 

### Evaluación y optimización
MLlib incluye métricas para clasificación y regresión, como **AUC, F1, RMSE y MAE**, junto con herramientas de optimización como **validación cruzada** y **Grid Search**. Esto permite comparar modelos y ajustar hiperparámetros de forma objetiva. 

## Infografías

### Infografía 1: panorama general de MLlib

```text
MACHINE LEARNING ESCALABLE
│
├── Problema
│   ├── Mucho volumen de datos
│   ├── Una sola máquina no basta
│   └── Se requiere procesamiento distribuido
│
├── Solución
│   └── Apache Spark MLlib
│
├── Ventajas
│   ├── Escalabilidad horizontal
│   ├── Procesamiento en clúster
│   ├── Integración con Spark
│   └── Pipelines reproducibles
│
└── Usos
    ├── Clasificación
    ├── Regresión
    ├── Clustering
    ├── PCA / reducción de dimensión
    └── Recomendación
```

### Infografía 2: flujo de trabajo supervisado

```text
Datos crudos
   ↓
Preparación de datos
(StringIndexer / OneHotEncoder / VectorAssembler / Scaler)
   ↓
DataFrame con label + features
   ↓
División train / test
   ↓
Entrenamiento del modelo
   ↓
Predicción
   ↓
Evaluación
(AUC / RMSE / otras métricas)
   ↓
Mejora con Pipeline + ajuste de hiperparámetros
```

### Infografía 3: estructuras de datos en MLlib

| Estructura | Función | Cuándo se usa |
|---|---|---|
| DataFrame | Base para entrada, transformación y salida | Casi todo el flujo de MLlib |
| DenseVector | Guarda todos los valores | Cuando la mayoría no son cero |
| SparseVector | Guarda solo índices y valores no nulos | Cuando hay muchos ceros |
| Matrix | Representación bidimensional | SVD, factorización y operaciones avanzadas |
| Pipeline | Encadena etapas del flujo | Cuando se quiere automatizar y reutilizar |
| Model / Transformer | Aplican conocimiento aprendido o transformaciones | Predicción y despliegue |

### Infografía 4: supervisado vs no supervisado

| Tipo | Objetivo | Algoritmos ejemplo | Salida típica |
|---|---|---|---|
| Supervisado | Predecir usando etiquetas | Logistic Regression, Linear Regression, Random Forest | Clase o valor numérico |
| No supervisado | Descubrir patrones sin etiquetas | K-Means, GMM, PCA | Clústeres o nuevas dimensiones |

### Infografía 5: idea clave de escalabilidad

```text
Machine Learning tradicional
→ limitado por memoria local
→ tiempos mayores con datasets grandes
→ menor capacidad de crecimiento

Spark MLlib
→ procesamiento distribuido
→ paralelismo en clústeres
→ trabajo con millones de registros
→ mejor adaptación a Big Data
```

## Markdown completo listo para copiar

```markdown
# Introducción a Machine Learning Escalable con Spark MLlib

## Resumen ejecutivo

### Propósito del tema
Este tema presenta Spark MLlib como la biblioteca de machine learning de Apache Spark para trabajar con grandes volúmenes de datos. Su foco está en resolver problemas donde el aprendizaje automático tradicional ya no escala bien en una sola máquina. 

### Qué ofrece MLlib
MLlib permite desarrollar soluciones de clasificación, regresión, clustering, reducción de dimensionalidad y recomendación. Su fortaleza está en el procesamiento distribuido, la integración con Spark y la ejecución eficiente en clústeres. 

### Estructuras de datos principales
La estructura base es el DataFrame, usada para cargar, transformar y almacenar resultados. También se utilizan vectores densos y dispersos para representar características, y matrices para operaciones más avanzadas.

### Flujo general de trabajo
El proceso estándar consiste en preparar datos, definir el algoritmo, dividir en entrenamiento y prueba, entrenar, predecir y evaluar. Este flujo se puede encapsular en un Pipeline para automatizar y hacer reproducible el modelado. 

### Algoritmos más importantes
En supervisado destacan Regresión Logística, Regresión Lineal, Árboles, Random Forest y Gradient-Boosted Trees. En no supervisado resaltan K-Means, GMM, PCA y SVD, además de ALS para recomendación.

### Evaluación y mejora
MLlib incorpora métricas como AUC, F1, RMSE y MAE, además de herramientas de validación cruzada y Grid Search. Esto ayuda a medir rendimiento y optimizar hiperparámetros con criterio técnico.

## Infografías

### Panorama general

```text
MACHINE LEARNING ESCALABLE
│
├── Problema: grandes volúmenes de datos
├── Solución: Spark MLlib
├── Ventajas: escalabilidad + integración + paralelismo
└── Usos: clasificación, regresión, clustering, PCA, recomendación
```

### Flujo supervisado

```text
Preparación → Features/Label → Train/Test → Entrenamiento → Predicción → Evaluación
```

### Estructuras clave

| Estructura | Rol principal | Ejemplo de uso |
|---|---|---|
| DataFrame | Gestionar datos distribuidos | Entradas, transformaciones, predicciones |
| DenseVector | Representar features con pocos ceros | Variables numéricas completas |
| SparseVector | Ahorrar memoria cuando hay muchos ceros | Datos de alta dimensionalidad |
| Pipeline | Encadenar etapas | Preprocesamiento + modelo + evaluación |

### Supervisado vs no supervisado

| Enfoque | Requiere etiquetas | Ejemplos |
|---|---|---|
| Supervisado | Sí | Logistic Regression, Linear Regression |
| No supervisado | No | K-Means, GMM, PCA |

## Puntos de estudio rápido

- MLlib pertenece al ecosistema Apache Spark.
- Está pensado para datos masivos y procesamiento distribuido.
- Trabaja principalmente con DataFrames y vectores.
- Usa pipelines para automatizar el flujo de ML. 
- Incluye algoritmos supervisados y no supervisados.
- Permite evaluar y optimizar modelos a escala. 
```

## Estructura de PowerPoint

### Diapositiva 1: Portada
- Introducción a Machine Learning Escalable
- Spark MLlib como herramienta central
- Enfoque en Big Data y procesamiento distribuido

### Diapositiva 2: Índice
- Qué es MLlib
- Estructuras de datos principales
- Algoritmos soportados
- Flujo de trabajo con MLlib
- Evaluación y escalabilidad

### Diapositiva 3: ¿Por qué ML escalable?
- Los datos crecieron más allá de una sola máquina
- El ML tradicional enfrenta límites de memoria y tiempo
- Spark MLlib responde con procesamiento distribuido
- Permite entrenar y evaluar a gran escala

### Diapositiva 4: ¿Qué es MLlib?
- Biblioteca de machine learning de Apache Spark
- Diseñada para entornos distribuidos
- Integrada con Spark SQL y otros módulos
- Soporta clasificación, regresión y clustering

### Diapositiva 5: Ventajas principales
- Escalabilidad horizontal en clústeres
- Ejecución paralela de algoritmos
- Compatibilidad con varios lenguajes
- Integración en flujos end-to-end

### Diapositiva 6: Estructuras de datos
- DataFrame como estructura principal
- DenseVector para datos densos
- SparseVector para datos con muchos ceros
- Matrix para operaciones avanzadas
- Pipeline para automatizar etapas

### Diapositiva 7: Supervisado en MLlib
- Usa datos con etiqueta
- Ejemplos: Logistic Regression y Linear Regression
- También incluye árboles y ensambles
- Flujo: preparar, entrenar, predecir, evaluar

### Diapositiva 8: No supervisado en MLlib
- Busca patrones sin etiquetas
- K-Means agrupa por similitud
- GMM modela clústeres probabilísticos
- PCA reduce dimensión conservando información

### Diapositiva 9: Flujo de implementación
- Preparación con transformadores
- División en train y test
- Entrenamiento del modelo
- Predicción sobre nuevos datos
- Evaluación con métricas adecuadas

### Diapositiva 10: Pipelines
- Encadenan transformadores y estimadores
- Mejoran automatización y reproducibilidad
- Facilitan mantenimiento del flujo
- Son recomendados para producción

### Diapositiva 11: Evaluación del modelo
- Clasificación: AUC, Precision, Recall, F1
- Regresión: RMSE, MAE, R²
- Clustering: Silhouette Score
- Base para comparar y optimizar modelos

### Diapositiva 12: Optimización
- Grid Search para probar combinaciones
- Validación cruzada para medir robustez
- Selección del mejor modelo según métricas
- Mejora controlada del rendimiento

### Diapositiva 13: Conclusión
- MLlib permite llevar machine learning a escala real
- Spark aporta paralelismo e integración
- DataFrames, vectores y pipelines son piezas centrales
- Es una herramienta clave en proyectos Big Data

## Recomendaciones visuales para la PPT

### Estilo sugerido
- Diseño profesional y minimalista
- Fondo claro o azul oscuro suave
- Tipografía limpia como Inter, Calibri o Aptos
- Íconos simples y consistentes por sección

### Paleta de colores
- Azul principal: `#1D4ED8`
- Celeste de apoyo: `#38BDF8`
- Gris oscuro: `#1F2937`
- Gris claro: `#E5E7EB`
- Verde de acento: `#10B981`

### Íconos sugeridos
- MLlib / Spark: servidor, rayo, nube
- DataFrames: tabla o base de datos
- Vectores: puntos o barras
- Supervisado: etiqueta / check
- No supervisado: grupos / nodos
- Evaluación: gráfico o velocímetro

### Gráficos recomendados
   - Barras: comparar tipos de algoritmos o etapas del flujo
   - Diagrama de flujo: pipeline supervisado
   - Tabla comparativa: supervisado vs no supervisado
   - Esquema jerárquico: estructuras de datos de MLlib
