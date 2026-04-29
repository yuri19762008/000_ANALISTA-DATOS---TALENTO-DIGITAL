# Bootcamp Fundamentos de Ciencia de Datos 🐍

Bienvenido/a — este repositorio contiene los ejercicios y material práctico del curso **"Bootcamp Fundamentos de Ciencia de Datos"**.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Estructura de Módulos](#estructura-de-módulos)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Cómo Usar](#cómo-usar)
- [Contribuir](#cómo-contribuir)
- [Estructura del Repositorio](#esquema-del-directorio)

---

## Descripción

Este repositorio agrupa las lecciones, demos y ejercicios por módulos y lecciones (9 módulos en total). El objetivo es practicar el flujo real de trabajo: escribir código, ejecutarlo, versionarlo y compartirlo.

Cada módulo suma progresivamente conceptos fundamentales, desde lo básico hasta análisis de datos avanzado.

## Estructura de Módulos

- **Módulo 1** — Introducción y fundamentos
- **Módulo 2** — Introducción a Python (control de flujo, funciones, módulos)
- **Módulo 3** — Librerías de análisis: NumPy y Pandas
- **Módulo 4** — Manipulación y análisis de datos
- **Módulo 5** — Visualización de datos
- **Módulo 6** — Machine Learning básico
- **Módulo 7** — Modelos supervisados avanzados
- **Módulo 8** — Modelos no supervisados
- **Módulo 9** — Big Data

En cada `Leccion/` encontrarás:
- Archivos `demo.py` — ejemplos didácticos
- Archivos `ejercicio.py` o `Ejercicio1.py`, `Ejercicio2.py` — problemas para practicar
- Archivos `LiveCoding.py` — soluciones del coding en vivo
- Notebooks `.ipynb` — para exploración interactiva
- Conjuntos de datos `.csv` o archivos de soporte

---

## Requisitos

- **Python 3.8 o superior** (recomendado 3.10+)
- **pip** (gestor de paquetes de Python)
- Entorno virtual (venv, conda, poetry, etc.)

### Dependencias Principales

- `numpy` — computación numérica
- `pandas` — manipulación de datos
- `matplotlib` / `seaborn` — visualización
- `scikit-learn` — machine learning
- `jupyter` / `jupyter notebook` — notebooks interactivos

## Instalación

### Opción 1: Entorno virtual con venv (Recomendado)

```bash
# Crear el entorno virtual
python -m venv Bootcamp

# Activar el entorno
# En macOS/Linux:
source Bootcamp/bin/activate
# En Windows:
# Bootcamp\Scripts\activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias desde requirements.txt
pip install -r requirements.txt
```

### Opción 2: Anaconda/Miniconda

```bash
# Crear entorno con conda
conda create -n Bootcamp python=3.10

# Activar entorno
conda activate Bootcamp

# Instalar dependencias
conda install numpy pandas matplotlib seaborn scikit-learn jupyter scipy -y
```

## Cómo Usar

### Ejecutar un script de Python

```bash
python Modulo2/Leccion2/ejemplo.py
```

### Ejecutar un demo específico

```bash
python Modulo2/Leccion2/demo.py
```

### Abrir un Jupyter Notebook

```bash
jupyter notebook Modulo3/Leccion2/demo_notebook.ipynb
# O simplemente:
jupyter notebook
# Y navega en el navegador
```

---

## Cómo Contribuir

Si deseas agregar ejemplos, ejercicios o mejoras:

1. **Crea una rama nueva:**
   ```bash
   git checkout -b feature/mi-ejercicio
   ```

2. **Organiza tus archivos:**
   - Respeta la estructura `ModuloX/LeccionY/`
   - Usa nombres de archivo descriptivos (ej: `Ejercicio1.py`, `MiRutinaSaludable.py`)
   - Si creas archivos de datos, guárdalos junto al código que los usa

3. **Asegúrate de:**
   - Incluir docstrings en funciones principales
   - Agregar comentarios para lógica compleja
   - Usar nombres de variables claros y descriptivos

4. **Abre un Pull Request** con:
   - Descripción clara de qué agregaste/modificaste
   - Instrucciones sobre cómo ejecutar tu código
   - Referencias a módulos o lecciones relacionadas

### Buenas Prácticas

- Activa el entorno `Bootcamp` antes de trabajar
- Instala nuevas dependencias con `pip install paquete` y documéntalo
- Evita agregar archivos grandes (>10MB) al repositorio
- Usa nombres de archivo consistentes con el resto del bootcamp
- Mantén la estructura de directorios consistente

---

## Esquema del Directorio

Estructura simplificada del repositorio:

```
Bootcamp/
├── README.md
├── dbscan.ipynb
├── Modulo1/
│   ├── [Ejercicios introductorios]
├── Modulo2/
│   ├── Leccion2/
│   │   ├── demo.py
│   │   ├── ejemplo.py
│   │   ├── CalculadoraExpress.py
│   │   ├── MiRutinaSaludable.py
│   │   └── Live Coding P1.py
│   ├── Leccion3/
│   │   ├── demo.py
│   │   ├── AccesoPermitido.py
│   │   └── LiveCodingP1.py
│   ├── Leccion4/
│   │   ├── demo.py
│   │   ├── operaciones.py
│   │   └── mi_modulo.py
│   ├── Leccion5/
│   ├── Leccion6/
│   └── Leccion7/
├── Modulo3/
│   ├── ExamenM3.ipynb
│   ├── Leccion1/
│   │   ├── demo.py
│   │   ├── NumPy.py
│   │   └── ejercicio1.py
│   ├── Leccion2/
│   │   ├── demo_notebook.ipynb
│   │   ├── Demo.ipynb
│   │   ├── Titanic-Dataset.csv
│   │   └── Libreria_pandas.py
│   ├── Leccion3/
│   │   ├── AAPL_historico.csv
│   │   ├── yf.ipynb
│   │   └── [Datasets varios]
│   ├── Leccion4/
│   ├── Leccion5/
│   └── Leccion6/
├── Modulo4/ a Modulo9/
│   ├── Leccion1/ a Leccion8/
│   └── [Ejercicios y material de cada lección]
└── [Otros archivos de configuración]
```

### Tipos de Archivos

- `demo.py` — Ejemplos didácticos básicos
- `demo*.py` — Variantes de demostraciones
- `Ejercicio*.py` — Ejercicios numerados para resolver
- `LiveCoding*.py` — Soluciones del coding en vivo
- `*.ipynb` — Notebooks Jupyter para exploración interactiva
- `*.csv` / `*.json` — Conjunto de datos para análisis
- `__pycache__/` — Archivos compilados (ignorar)

---

## Consejos Útiles

### Primeros Pasos

1. **Clona o descarga** el repositorio
2. **Activa el entorno virtual:**
   ```bash
   source Bootcamp/bin/activate  # macOS/Linux
   # o: Bootcamp\Scripts\activate  # Windows
   ```
3. **Explora los módulos** comenzando por Modulo2 (Introducción a Python)
4. **Usa Jupyter** para explorar de forma interactiva:
   ```bash
   jupyter notebook
   ```

### Debugging

- Si tienes errores de importación, asegúrate de tener el entorno activado
- Verifica que todas las dependencias estén instaladas: `pip list`
- Para instalar librerías faltantes: `pip install nombre_paquete`

### Recursos Recomendados

- [Documentación oficial de Python](https://docs.python.org/3/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/)

---

**Última actualización:** 30 de marzo de 2026
│  └─ Leccion7/
├─ Modulo3/
│  └─ Leccion1/
│     ├─ NumPy.py
│     └─ demo.py
└─ README.md
```

