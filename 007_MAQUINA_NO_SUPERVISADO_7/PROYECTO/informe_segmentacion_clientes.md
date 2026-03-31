# Informe Final – Segmentador Inteligente de Clientes Minoristas

## 1. Contexto y objetivo

El departamento de Inteligencia de Negocios de **Retail Insights S.A.** busca entender mejor el comportamiento de sus clientes minoristas para diseñar campañas de marketing más personalizadas y efectivas.

Actualmente se utilizan variables básicas (como edad o gasto total histórico), lo que no permite diseñar estrategias diferenciadas ni identificar segmentos ocultos con patrones de compra específicos.

El objetivo de este proyecto es desarrollar un **modelo de segmentación de clientes** utilizando técnicas de **aprendizaje no supervisado**, de modo que se puedan identificar grupos de clientes con comportamientos similares, visualizarlos de forma clara y utilizar estos segmentos para apoyar decisiones de negocio en campañas de retención, fidelización y ventas cruzadas.

Para ello se emplean técnicas de **reducción de dimensionalidad** (PCA y t-SNE) y **clusterización** (K-Means, DBSCAN y agrupamiento jerárquico) a partir de los datos contenidos en los archivos `Train.csv` y `Test.csv`.

## 2. Datos y preprocesamiento

### 2.1 Descripción general de los datos

Los archivos `Train.csv` y `Test.csv` contienen información de clientes, incluyendo características demográficas y de comportamiento.

Entre ellas se observan variables como:

- Identificador del cliente.
- Género.
- Estado civil o situación familiar.
- Edad.
- Profesión u ocupación (por ejemplo, Artist, Executive, Healthcare, Engineer, Lawyer, etc.).
- Alguna medida de antigüedad o interacción (variables numéricas con valores como 0, 1, 3, 8, etc.).
- Nivel de ingresos o categoría socioeconómica (valores como Low, Average, High).
- Una o más variables categóricas adicionales (por ejemplo, Cat_1, Cat_2, Cat_6, etc.).

El dataset presenta tanto variables **numéricas** como **categóricas**, y se observan valores faltantes en varias columnas, lo que hace necesario un preprocesamiento cuidadoso.

### 2.2 Tratamiento de valores nulos

Para asegurar que los algoritmos de aprendizaje no supervisado funcionen de forma adecuada, se aplicó la siguiente estrategia de imputación:

- **Variables numéricas**  
  - Imputación con la **mediana** de cada columna, lo que reduce la sensibilidad a valores extremos.

- **Variables categóricas**  
  - Imputación con la **categoría más frecuente** de cada columna, preservando la consistencia semántica de los datos.

### 2.3 Escalado y codificación

Luego de la imputación, se aplicaron transformaciones específicas:

- **Escalado de variables numéricas**  
  - Se utilizó **StandardScaler** para centrar las variables en media 0 y desviación estándar 1.

- **Codificación de variables categóricas**  
  - Se utilizó **OneHotEncoder** con manejo de categorías desconocidas, generando columnas binarias (dummy) para cada categoría de las variables cualitativas.

## 3. Metodología

### 3.1 Reducción de dimensionalidad: PCA

Se aplicó **PCA (Principal Component Analysis)** sobre la matriz de datos ya preprocesada para:

- Analizar cuánta varianza explican las distintas componentes principales.
- Obtener una representación en **2 dimensiones (PC1 y PC2)** que permita visualizar los clientes en un plano.

### 3.2 Reducción de dimensionalidad: t-SNE

Se aplicó **t-SNE (t-distributed Stochastic Neighbor Embedding)** para obtener una representación en 2D que preserve bien las relaciones locales entre clientes (vecindarios).

### 3.3 Clusterización: K-Means

Se aplicó **K-Means** sobre los datos preprocesados siguiendo estos pasos:

1. Evaluación de distintos valores de `k` usando el **método del codo**.
2. Cálculo del **coeficiente de silueta** para varios valores de `k`.
3. Selección de un valor de `k` razonable (por ejemplo, `k = 4`).
4. Ajuste final del modelo K-Means y obtención de las etiquetas de clúster.

### 3.4 Clusterización: DBSCAN

Se aplicó **DBSCAN** sobre la misma matriz de datos preprocesados:

1. Definición de parámetros `eps` y `min_samples`.
2. Identificación de clústeres densos y puntos de ruido (`-1`).
3. Cálculo de silueta cuando hay al menos dos clústeres válidos.

### 3.5 Clusterización: agrupamiento jerárquico

Se utilizó **agrupamiento jerárquico aglomerativo**:

1. Fijando un número de clústeres (por ejemplo, 4).
2. Calculando la silueta para evaluar la separación de los grupos.

## 4. Resultados de los clústeres e interpretación de negocio

### 4.1 Comparación cuantitativa de algoritmos

| Algoritmo   | N_clústeres_efectivos | Silueta | N_ruido |
|------------|------------------------|---------|---------|
| K-Means    | 4                      | (valor) | 0       |
| DBSCAN     | variable               | (valor) | > 0     |
| Jerárquico | 4                      | (valor) | 0       |

En general:

- **K-Means** produce clústeres compactos y fáciles de interpretar.
- **DBSCAN** detecta clústeres de forma irregular y clientes atípicos.
- **Jerárquico** ofrece una estructura en niveles comparable a K-Means.

### 4.2 Interpretación cualitativa de los segmentos

Ejemplos de posibles segmentos (según promedio de variables por clúster):

- **Segmento 1**: clientes de edad media, ocupaciones como Artist o Healthcare, con nivel de ingreso principalmente “Low”.
- **Segmento 2**: clientes con ocupaciones de alto poder adquisitivo (Executive, Lawyer) y niveles de ingreso “High”.
- **Segmento 3**: clientes más jóvenes, con menor antigüedad.
- **Segmento 4**: clientes con patrones menos frecuentes o mixtos.

## 5. Recomendaciones comerciales por segmento

- **Segmentos de alto ingreso**: productos premium, planes exclusivos, programas VIP.
- **Segmentos de ingreso bajo**: promociones y bundles económicos, programas de fidelización simples.
- **Segmentos jóvenes/nuevos**: estrategias de onboarding, campañas de activación, recomendaciones personalizadas.
- **Outliers detectados por DBSCAN**: análisis individual para detectar oportunidades o riesgos.



## 6. Conclusiones y trabajo futuro

### 6.1 Conclusiones

- Se construyó un sistema de segmentación de clientes basado en aprendizaje no supervisado.
- K-Means y jerárquico proporcionan segmentaciones estables y fáciles de interpretar.
- DBSCAN complementa al identificar clústeres densos y clientes atípicos.

### 6.2 Trabajo futuro

- Afinar hiperparámetros de K-Means y DBSCAN.
- Incorporar nuevas variables transaccionales.
- Evaluar otros algoritmos de clusterización.
- Conectar con modelos supervisados para predecir el segmento de nuevos clientes.
