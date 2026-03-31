# Informe – Reducción dimensional en encuestas de clientes

## Técnica recomendada

En este caso, se recomienda utilizar una combinación de PCA y t-SNE para presentar insights al equipo de marketing:

1. t-SNE para la visualización principal de los clústers de clientes, ya que genera un mapa 2D donde los grupos aparecen bien separados y son fáciles de identificar a simple vista.
2. PCA como apoyo para la interpretación de los factores subyacentes, analizando qué variables contribuyen más a los componentes principales que separan esos grupos.

## Principales hallazgos

- El dataset presenta una estructura segmentada: en ambas proyecciones 2D (PCA y t-SNE) se observan grupos de clientes con patrones similares de respuesta.
- La proyección con t-SNE muestra clústers más compactos y claramente diferenciados, lo que facilita la comunicación visual de los segmentos.
- La proyección con PCA conserva bien la estructura global de los datos y permite interpretar los ejes en términos de combinaciones de variables originales.

## Reflexión crítica

La reducción dimensional es una herramienta muy útil para trabajar con encuestas de alta dimensionalidad, ya que permite acelerar el entrenamiento de modelos y facilitar la visualización de patrones y agrupamientos que serían imposibles de ver en el espacio original.

Sin embargo, es importante tener en cuenta que:

- PCA es lineal y puede no capturar relaciones complejas entre variables; además, los componentes pueden ser difíciles de explicar si intervienen muchas variables.
- t-SNE produce visualizaciones muy expresivas, pero sus ejes no tienen una interpretación directa, no preserva distancias globales y es sensible a los hiperparámetros y al tamaño del dataset.

En contextos con volúmenes de datos aún mayores, una buena práctica es combinar PCA (para reducir ruido y dimensionalidad) con técnicas no lineales como t-SNE o UMAP, y trabajar con muestras representativas para visualización.
