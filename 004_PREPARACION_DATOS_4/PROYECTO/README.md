# Análisis Exploratorio de Datos para ComercioYA

Proyecto del módulo "Análisis Exploratorio de Datos para decisiones comerciales". Se analiza un dataset de ventas históricas de ComercioYA para apoyar decisiones de negocio.

## Contenido del repositorio

- `main.py`: script principal de EDA (carga de datos, análisis estadístico y gráficos).
- `app.py`: aplicación Streamlit con tablas y visualizaciones interactivas.
- `comercio_ya.ipynb`: notebook con el desarrollo paso a paso del análisis.
- `ecommerce_sales_data-2.csv`: dataset de ventas utilizado.
- `figures/`: gráficos exportados desde el EDA.
- `figures_notebook/`: gráficos generados desde el notebook.
- `informes/`: informe final del proyecto.
- `requirements.txt`: dependencias necesarias para ejecutar el proyecto.

## Instalación

```
pip install -r requirements.txt

```

## Uso

1. Ejecutar el análisis EDA

    python PROYECTO/main.py

2. Ejecutar el dashboard (Streamlit)

    cd PROYECTO/ streamlit run app.py