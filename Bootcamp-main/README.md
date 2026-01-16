# Bootcamp Fundamentos de Ciencia de datos 🐍

Bienvenido/a — este repositorio contiene los ejercicios y material práctico del
curso "Bootcamp Fundamentos de Ciencia de datos".

**Entorno:** Bootcamp

---

**Descripción**

Este repositorio agrupa las lecciones, demos y ejercicios por módulos y lecciones.
El objetivo es practicar el flujo real de trabajo: escribir código, ejecutarlo,
versionarlo y compartirlo.

**Estructura principal**

- `Modulo1/` — material y ejercicios introductorios.
- `Modulo2/` — Introducción a Python con demos y ejercicios 
- `Modulo3/` — Libreria NumPy

Dentro de cada `LeccionX/` hay ejemplos `demo.py`, ejercicios y archivos de apoyo.

---

**Requisitos**

- Python 3.8 o superior
- Entorno virtual (se recomienda crear uno llamado `Bootcamp`)

**Instalación rápida (venv)**

```bash
python -m venv Bootcamp
source Bootcamp/bin/activate
pip install --upgrade pip
```

Si usas Anaconda, puedes crear un entorno con `conda create -n Bootcamp python=3.10`.

---

**Ejecutar ejemplos**

- Ejecutar el script de prueba:

```bash
python Modulo2/Leccion2/ejemplo.py
```

- Ejecutar un demo concreto:

```bash
python Modulo2/Leccion2/demo.py
```

---

**Cómo contribuir**

1. Crea una rama nueva, p. ej. `feature/mi-ejercicio`.
2. Añade tus archivos en la carpeta correspondiente (mantén la estructura por módulo/ lección).
3. Abre un Pull Request con una descripción y cómo ejecutar los ejemplos añadidos.

**Buenas prácticas**

- Usa el entorno `Bootcamp` para instalar dependencias.
- Añade docstrings y comentarios mínimos en funciones.
- Usa nombres de fichero descriptivos (p. ej. `Ejercicio1.py`, `MiRutinaSaludable.py`).

---

**Esquema del directorio**

A continuación se muestra un esquema simplificado de cómo está organizado el
repositorio (rutas relativas):

```text
.
├─ Modulo1/
│  ├─ demo.py
│  └─ ...
├─ Modulo2/
│  ├─ Leccion2/
│  │  ├─ CalculadoraExpress.py
│  │  ├─ Clase M2 AE2.py
│  │  ├─ demo.py
│  │  ├─ demo2.py
│  │  ├─ ejemplo.py
│  │  └─ Live Coding P1.py
│  ├─ Leccion3/
│  │  ├─ AccesoPermitido.py
│  │  ├─ Clase M2 AE3.py
│  │  └─ LiveCodingP1.py
│  ├─ Leccion4/
│  │  ├─ demo.py
│  │  ├─ operaciones.py
│  │  └─ MiRutinaSaludable.py
│  ├─ Leccion5/
│  ├─ Leccion6/
│  └─ Leccion7/
├─ Modulo3/
│  └─ Leccion1/
│     ├─ NumPy.py
│     └─ demo.py
└─ README.md
```

