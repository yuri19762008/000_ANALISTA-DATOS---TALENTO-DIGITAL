# Proyecto: Preparación de Datos con Python (Módulo 3)

## Descripción general

Este proyecto implementa un flujo completo de **preparación de datos** para un caso de e‑commerce utilizando Python, NumPy y Pandas.  
El objetivo es partir de datos provenientes de distintas fuentes (datos ficticios generados, archivos CSV/Excel y una tabla web), limpiarlos, transformarlos y dejarlos listos para análisis y modelos futuros.

El resultado final incluye:

- Un script Python con todo el flujo (`datos.py`).
- Un notebook (`datos.ipynb`) con las mismas etapas explicadas paso a paso.
- Un dataset final estructurado (`dataset_final.csv` y `dataset_final.xlsx`).
- Opcionalmente, un dashboard en Streamlit (`dashboard.py`) para explorar los datos.

---
### VERIFICAR RUTAS DE LECTURA Y GUARDADO
## Estructura sugerida del proyecto

```text
proyecto_modulo/
│
├─ datos.py
├─ datos.ipynb
├─ dashboard.py                  # opcional (Streamlit)
├─ requirements.txt
│
├─ clientes_ecommerce.csv
├─ clientes_ecommerce.xlsx
│
├─ clientes_numpy.npy
├─ clientes_desde_numpy.csv
├─ dataset_consolidado.csv
├─ dataset_limpio.csv
├─ dataset_wrangle.csv
├─ dataset_final.csv
└─ dataset_final.xlsx
```

---
## Instrucciones de instalación y ejecución
---

## 1. Requisitos previos

- Python 3.x instalado.
- Acceso a una terminal (CMD, PowerShell, Terminal en Linux/macOS).
- Git (opcional, solo si vas a clonar desde un repositorio).


## 2. Clonar o copiar el proyecto

Coloca todos los archivos del proyecto en una carpeta, por ejemplo:

```
proyecto/
    datos.py
    datos.ipynb
    dashboard.py                # si usas Streamlit
    requirements.txt
    clientes_ecommerce.csv
    clientes_ecommerce.xlsx
```
## Si usas Git:


        git clone <https://github.com/yuri19762008/000_ANALISTA-DATOS---TALENTO-DIGITAL/tree/master/002_A3/PROYECTO>
        
        cd proyecto


## 3. Crear y activar un entorno virtual
    - Windows (PowerShell o CMD)

        python -m venv .venv
        .venv\Scripts\activate

    - Linux / macOS

        python -m venv .venv
        source .venv/bin/activate


## 4. Instalar dependencias
    - Con el entorno virtual activo, en la carpeta del proyecto:


        pip install -r requirements.txt
        Esto instalará, entre otros:

            numpy
            pandas
            lxml
            requests
            streamlit (si está incluido para el dashboard)

    - Si quieres verificar versiones:


            pip list


## 5. Ejecutar el flujo principal (datos.py)

    - Asegúrate de que clientes_ecommerce.csv y clientes_ecommerce.xlsx estén en la misma carpeta que proyecto.

        En la terminal:

            python datos.py

    - Al finalizar, se habrán generado varios archivos intermedios y el dataset final:

            dataset_final.csv
            dataset_final.xlsx

## 6. Ejecutar el notebook (datos.ipynb) [opcional]

    - Instala Jupyter si aún no lo tienes:

            pip install jupyter

    - Lanza Jupyter:

            jupyter notebook


    - Abre datos.ipynb desde el navegador y ejecuta las celdas en orden.

## 7. Ejecutar el dashboard con Streamlit [opcional]

    - Si tu proyecto incluye dashboard.py y ya generaste dataset_final.csv:

            streamlit run dashboard.py

    - Esto abrirá (o mostrará) una URL del tipo:

            http://localhost:8501

    - Ábrela en el navegador para interactuar con el dashboard.


---

