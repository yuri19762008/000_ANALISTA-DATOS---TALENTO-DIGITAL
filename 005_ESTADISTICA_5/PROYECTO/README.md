# Desarrollo del notebook: hábitos saludables en jóvenes universitarios

## Descripción del notebook

Este notebook implementa paso a paso un proyecto de inferencia estadística sobre hábitos de sueño, alimentación y actividad física en estudiantes universitarios, y su relación con el estrés percibido y el rendimiento académico. Cada sección del notebook corresponde a una lección del módulo, desde la formulación del problema hasta las pruebas de hipótesis, utilizando un dataset simulado de al menos 150 estudiantes.

## Estructura del notebook

### 1. Lección 1 – Planteo del problema y diseño del estudio

En la primera parte se documenta el contexto del problema, las preguntas de investigación y las hipótesis estadísticas sobre la relación entre hábitos saludables (sueño, alimentación, actividad física) y bienestar académico (estrés, notas).  
Se construye un diccionario de variables (tipo, escala de medición y rol en el análisis) y se describe el diseño del estudio como observacional, transversal y cuantitativo, con muestreo aleatorio simple simulado sobre estudiantes universitarios.

### 2. Lección 2 – Simulación del dataset y probabilidades

En esta sección se generan los datos con Python (NumPy y pandas), simulando variables como edad, horas de sueño, calidad del sueño, nivel de actividad física, puntaje de alimentación, estrés y promedio de notas.  
A partir de este dataset se definen eventos aleatorios (por ejemplo, dormir ≥7h, actividad alta, alimentación saludable, nota ≥8) y se calculan probabilidades básicas de intersección, unión y complementarios, interpretadas como proporciones de estudiantes que cumplen distintas combinaciones de hábitos.

### 3. Lección 3 – Distribuciones de probabilidad y gráficos

El notebook explora las distribuciones empíricas de las variables mediante histogramas y gráficos de barras, e identifica qué variables pueden modelarse de manera razonable con distribuciones normales o discretas (binomial/Poisson).  
Se calculan probabilidades teóricas usando la distribución normal (por ejemplo, probabilidad de dormir al menos cierta cantidad de horas) y un ejemplo binomial para el puntaje de alimentación, ilustrando cómo conectar parámetros teóricos con datos simulados.

### 4. Lección 4 – Distribución muestral y Teorema del Límite Central

Aquí se generan distribuciones muestrales de la media de horas de sueño, tomando muchas muestras repetidas con distintos tamaños (n=10, 30, 50) a partir del dataset simulado.  
Se grafican los histogramas de esas medias muestrales y se compara su forma y dispersión, verificando empíricamente el Teorema del Límite Central: las distribuciones de las medias se aproximan a una normal y su variabilidad disminuye a medida que crece el tamaño muestral.

### 5. Lección 5 – Intervalos de confianza para la media

Esta parte implementa funciones para calcular intervalos de confianza para la media de variables continuas (por ejemplo, horas de sueño y estrés), utilizando la distribución t de Student.  
Se obtienen intervalos al 90 %, 95 % y 99 %, y se analiza cómo cambia su ancho con el nivel de confianza y con el tamaño de la muestra, mostrando que más confianza y menos datos implican intervalos más amplios y, por tanto, estimaciones menos precisas.

### 6. Lección 6 – Pruebas de hipótesis y valor p

En la última sección se realizan pruebas de hipótesis de ejemplo:

- Test de una media para evaluar si los estudiantes duermen, en promedio, menos de 7 horas.  
- Test de proporción para evaluar si menos de la mitad de los estudiantes tiene buena calidad de sueño.  
- Test de comparación de medias para analizar si el estrés es menor en estudiantes con actividad física alta que en estudiantes con actividad baja.

Se calculan estadísticos de prueba, valores p y se toman decisiones respecto a las hipótesis nula y alternativa, discutiendo el significado de errores tipo I y tipo II en el contexto de la salud y el bienestar estudiantil.

## Flujo de trabajo en el notebook

1. Definir el contexto, las preguntas y las hipótesis.  
2. Simular el dataset con las variables necesarias y revisar las primeras filas para validar la estructura.  
3. Calcular probabilidades de eventos simples y combinados a partir de frecuencias relativas.  
4. Explorar las distribuciones de las variables con gráficos y vincularlas a modelos de probabilidad teóricos.  
5. Generar distribuciones muestrales de la media para ilustrar el Teorema del Límite Central.  
6. Construir e interpretar intervalos de confianza para parámetros poblacionales.  
7. Ejecutar pruebas de hipótesis, interpretar valores p y discutir las conclusiones y riesgos de error.  

Este desarrollo convierte el proyecto teórico del módulo en un flujo práctico reproducible, que puede usarse como base para proyectos posteriores con datos reales o nuevas preguntas de investigación.
