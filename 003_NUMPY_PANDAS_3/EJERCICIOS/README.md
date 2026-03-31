# Análisis de Caso – NumPy en Análisis de Datos

## 2. Análisis y transformación de datos

En esta sección se describen las operaciones realizadas sobre los datos financieros utilizando NumPy para obtener métricas y aplicar transformaciones numéricas eficientes.

### 2.1 Métricas por acción

- Se calcula el promedio de precio por acción a lo largo de los días usando operaciones agregadas sobre las filas de la matriz de precios.
- Se obtienen también el valor máximo y mínimo de cada acción, lo que permite evaluar el rango de variación de cada activo en el periodo analizado.
- Estas métricas se realizan de forma vectorizada, sin bucles explícitos, aprovechando las funciones estadísticas de NumPy para trabajar sobre arrays multidimensionales.

### 2.2 Variación porcentual diaria

- La variación porcentual diaria de cada acción se obtiene aplicando la fórmula \((p_t - p_{t-1}) / p_{t-1} * 100\) entre columnas consecutivas de la matriz de precios.
- Mediante slicing se toman todas las filas y las columnas desplazadas (precios del día actual y del día anterior), calculando en una sola operación una matriz con las variaciones de todos los días y acciones.
- Este enfoque permite analizar rápidamente la volatilidad y el comportamiento diario de los activos, lo que es clave en análisis financiero.

### 2.3 Transformaciones matemáticas

- Se aplica el logaritmo natural a los precios para obtener una escala más adecuada para algunos modelos y análisis estadísticos, utilizando funciones matemáticas vectorizadas.
- Se muestra también el uso de la función exponencial sobre una versión escalada de los datos, como ejemplo de transformación no lineal.
- Para la normalización min-max por acción, se resta el mínimo y se divide por el rango de cada fila, generando valores entre 0 y 1 que facilitan comparaciones entre activos con escalas de precios diferentes.

## 3. Optimización e indexación de datos

En esta sección se detalla cómo se extrae información específica y se optimizan operaciones usando indexación avanzada y broadcasting en NumPy.

### 3.1 Indexación puntual y por subconjuntos

- El precio de una acción en un día concreto se recupera mediante indexación 2D estándar, usando el índice de fila para la acción y de columna para el día.
- Para obtener subconjuntos no contiguos (por ejemplo, un conjunto de acciones y días específicos), se emplea indexación avanzada con listas de índices y combinaciones que permiten generar submatrices de forma directa.
- Estas técnicas reducen la necesidad de escribir bucles y hacen más expresivas las consultas sobre el conjunto de datos.

### 3.2 Broadcasting en operaciones

- El centrado de los precios por acción se realiza restando el vector de promedios de cada fila a la matriz completa, aprovechando que NumPy expande automáticamente las dimensiones necesarias.
- Se aplica también un incremento porcentual uniforme (por ejemplo, un 5 %) multiplicando la matriz de precios por un escalar, lo que es útil para simulaciones o ajustes globales.
- El broadcasting permite aplicar operaciones entre arrays de dimensiones compatibles sin necesidad de replicar datos, mejorando tanto la claridad del código como el rendimiento.

## 4. Comparación con métodos sin NumPy

Esta sección analiza las diferencias entre usar NumPy y utilizar estructuras básicas de Python (listas y bucles) para las mismas tareas.

### 4.1 Implementación sin NumPy

- Con listas de listas, el cálculo de promedios, máximos y mínimos requeriría recorrer cada acción con bucles, utilizando funciones como `sum`, `len`, `max` y `min` manualmente.
- La variación porcentual diaria se implementaría con bucles anidados sobre acciones y días, generando estructuras nuevas paso a paso.
- La normalización y otras transformaciones matemáticas implicarían repetir patrones de iteración, lo que incrementa la cantidad de código y la probabilidad de errores.

### 4.2 Rendimiento y legibilidad

- NumPy ejecuta operaciones vectorizadas sobre arrays en código compilado (C), logrando una mejora notable en tiempos de ejecución frente a bucles interpretados en Python puro, especialmente con grandes volúmenes de datos.
- El código con NumPy es más conciso y declarativo: las operaciones sobre filas y columnas se expresan con funciones agregadas e indexación clara en lugar de múltiples bucles.
- En contextos de análisis financiero y de datos en tiempo (casi) real, la combinación de rendimiento y claridad hace que NumPy sea una herramienta especialmente adecuada.

### 4.3 Conclusiones sobre el uso de NumPy

- NumPy aporta una infraestructura optimizada para manipular matrices y realizar cálculos matemáticos y estadísticos de forma eficiente.
- Frente a métodos tradicionales, reduce la complejidad del código, mejora el rendimiento y proporciona abstracciones como broadcasting e indexación avanzada, que son difíciles de replicar manualmente con la misma eficiencia.
- En un entorno de análisis de datos financieros, estas ventajas se traducen en procesos más rápidos, mantenibles y escalables.
