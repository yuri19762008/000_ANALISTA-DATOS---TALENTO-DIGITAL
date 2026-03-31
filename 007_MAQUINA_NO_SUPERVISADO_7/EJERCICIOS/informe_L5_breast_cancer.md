# Informe técnico – Análisis de caso L5
## Técnicas de reducción dimensional en datos clínicos (Breast Cancer Wisconsin)

### 1. Introducción

En este análisis se utilizó el dataset **Breast Cancer Wisconsin (Diagnostic)** como análogo de un conjunto de datos clínicos de alta dimensionalidad para diagnóstico de enfermedades. El objetivo fue aplicar técnicas de reducción dimensional para mejorar la comprensión de la estructura de los datos y evaluar su utilidad dentro de un pipeline de modelado predictivo.

Se trabajó con 30 variables numéricas que describen características de núcleos celulares obtenidos de imágenes de biopsias, y una variable objetivo binaria que indica si el tumor es maligno o benigno. [web:35]

### 2. Metodología

1. **Carga y exploración de datos**.
   - Se cargó el dataset desde `sklearn.datasets.load_breast_cancer` y se construyó un DataFrame con las 30 características numéricas.
   - Se verificó que no hubiera valores nulos y se revisaron estadísticos descriptivos básicos y distribuciones de algunas variables mediante histogramas.

2. **Preprocesamiento – StandardScaler**.
   - Se aplicó `StandardScaler` para estandarizar todas las variables numéricas, de modo que cada una tuviera media 0 y desviación estándar 1.
   - Este paso es clave para que tanto PCA como t-SNE no se vean dominados por variables con escalas mayores. [web:6]

3. **PCA (Análisis de Componentes Principales)**.
   - Se ajustó un PCA inicial con tantas componentes como variables (30) y se analizó la **varianza explicada acumulada**.
   - La curva de varianza mostró que con un número relativamente pequeño de componentes (por ejemplo, entre 7 y 10) se puede explicar alrededor del 90–95 % de la varianza total.
   - Para visualización se ajustó un PCA a 2 componentes, obteniendo una proyección 2D (PC1, PC2) y coloreando los puntos según la clase (maligno/benigno). [web:5][web:2]

4. **t-SNE (t-Distributed Stochastic Neighbor Embedding)**.
   - Se aplicó t-SNE sobre los datos estandarizados para obtener una proyección 2D no lineal.
   - Se usó una configuración base con `n_components=2`, `perplexity=30`, `learning_rate=200`, `init='pca'` y una semilla fija para reproducibilidad.
   - Además, se probaron distintas combinaciones de `perplexity` y `learning_rate` (por ejemplo, 5/50, 30/200, 50/500) para observar su impacto en la forma y separación de los clústers. [web:47]

### 3. Resultados

#### 3.1 PCA

- La curva de varianza explicada acumulada evidenció que unas pocas componentes concentran la mayor parte de la información. Esto indica que el espacio original de 30 dimensiones tiene redundancia y que es razonable reducirlo sin perder demasiada información relevante. [web:6]
- En la proyección 2D (PC1 vs PC2), las clases maligno y benigno aparecen parcialmente separadas: se forman dos regiones principales, aunque con cierto solapamiento en la zona central.
- Cada componente principal es una combinación lineal de las variables originales, lo que permite analizar las cargas (loadings) para entender qué características celulares contribuyen más a la variabilidad entre tumores. [web:5]

#### 3.2 t-SNE

- La proyección t-SNE 2D muestra grupos de puntos más compactos y mejor separados visualmente que PCA, especialmente para distinguir observaciones malignas de benignas.
- Con `perplexity=30` y `learning_rate=200`, los dos grupos principales se observan como “islas” bien diferenciadas, lo que facilita la comunicación visual de la existencia de dos patrones claros en los datos. [web:47]
- Al variar `perplexity` y `learning_rate` se aprecia que t-SNE es sensible a estos hiperparámetros: valores demasiado bajos o altos pueden fragmentar o mezclar los clústers, o cambiar la forma global del mapa.

### 4. Comparativa PCA vs t-SNE

**Visualización de clústers**

- t-SNE ofrece, en este caso, una separación visual más clara entre tumores malignos y benignos. Los clústers aparecen más compactos y bien definidos, por lo que resulta muy útil para exploración y presentación gráfica a equipos no técnicos. [web:40][web:47]
- PCA también logra una separación razonable, pero con más solapamiento. Aun así, la proyección es suficiente para apreciar que existen dos grupos principales en el espacio de características. [web:6]

**Uso en un pipeline de modelado predictivo**

- **PCA** es más adecuado como parte estable del pipeline, porque:
  - Proporciona una transformación lineal fija (definida por las componentes principales) que puede aplicarse de forma consistente a nuevos pacientes.
  - Reduce dimensionalidad y ruido, mejora tiempos de entrenamiento y puede ayudar a mitigar sobreajuste, manteniendo una buena parte de la información. [web:6][web:45]
  - Las componentes permiten cierto grado de interpretación clínica a través de las cargas asociadas a cada variable original. [web:5]

- **t-SNE** es más apropiado como herramienta de **visualización exploratoria**, pero menos recomendable como etapa fija del pipeline supervisado, porque:
  - Es más costoso computacionalmente y menos escalable a grandes volúmenes de datos.
  - No preserva bien las distancias globales; la forma del mapa puede cambiar con distintos parámetros o nuevas muestras.
  - Sus ejes no son interpretables y la transformación no está pensada para aplicarse de forma estable a nuevos datos. [web:47][web:50]

En resumen, para este caso clínico t-SNE resulta excelente para ilustrar la separación entre tumores malignos y benignos en presentaciones al equipo médico, mientras que PCA es la elección preferente para reducir dimensionalidad dentro del flujo de entrenamiento de modelos de diagnóstico.

### 5. Conclusiones

- El dataset de Breast Cancer Wisconsin presenta alta dimensionalidad pero con fuerte estructura interna, lo que permite explicar la mayor parte de la varianza con un número reducido de componentes principales.
- PCA proporciona una representación compacta y relativamente interpretable del espacio de características, resultando adecuado para mejorar eficiencia, reducir ruido y apoyar la interpretación global del modelo.
- t-SNE proporciona visualizaciones 2D muy expresivas y útiles para explorar clústers y comunicar hallazgos a audiencias no técnicas, pero su sensibilidad a los hiperparámetros y su naturaleza no lineal lo hacen menos indicado como transformación estándar en el pipeline predictivo.

### 6. Reflexión personal

El uso conjunto de PCA y t-SNE en un contexto clínico permite equilibrar **eficiencia de modelado** e **interpretabilidad visual**. PCA ayuda a condensar la información en pocas dimensiones manejables, mientras que t-SNE revela patrones y clústers que serían difíciles de ver en el espacio original. [web:45]

Las principales dificultades encontradas están relacionadas con:

- La elección del número de componentes óptimo en PCA (decidir entre explicar más varianza o mantener el modelo más simple).
- La selección de hiperparámetros en t-SNE (perplexity, learning_rate), que requieren experimentación cuidadosa para evitar interpretaciones engañosas.

Este ejercicio refuerza la importancia de combinar técnicas de reducción dimensional con análisis crítico y validación cuidadosa, especialmente cuando los resultados influyen en decisiones clínicas sensibles.
