# Sistema de Gestión de Contactos en Python

Aplicación de consola que permite **registrar, buscar, editar y eliminar contactos**, utilizando **programación orientada a objetos**, estructuras de datos en Python y **persistencia en JSON**.

---

## 📚 Tabla de contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Estructura del proyecto](#-estructura-del-proyecto)

---

## 📋 Descripción

Este proyecto implementa un **Sistema de Gestión de Contactos** en Python que funciona como una agenda de clientes en la línea de comandos.  
Permite almacenar información personal (nombre, teléfono, correo y dirección) de forma organizada, segura y persistente mediante archivos JSON, aplicando buenas prácticas de código y pruebas unitarias.[web:44][web:50]

El sistema fue desarrollado como parte de una evaluación de módulo, pensado para ser incluido en un portafolio técnico.

---

## ✨ Características

- **Registro de contactos**: alta de nuevos contactos con validaciones básicas.
- **Búsqueda flexible**:
  - Por nombre (coincidencia parcial, sin importar mayúsculas/minúsculas).
  - Por teléfono (coincidencia exacta).
- **Edición de contactos**: actualización de nombre, correo y dirección.
- **Eliminación de contactos**: borrado seguro con confirmación.
- **Persistencia en JSON**: los contactos se guardan y cargan automáticamente.
- **Interfaz de consola**: menú simple e intuitivo.
- **Pruebas unitarias**: cobertura de las funcionalidades principales con `unittest`.[web:28][web:35]

---

## 🛠 Tecnologías

- **Lenguaje**: Python 3.7+
- **Librerías estándar**:
  - `json` para persistencia de datos.
  - `os` para manejo de archivos.
  - `unittest` para pruebas unitarias.[web:28][web:39]

No se utilizan dependencias externas, lo que facilita la ejecución en cualquier entorno con Python 3 instalado.

---

## 🗂 Estructura del proyecto

```bash
Sistema-Gestion-Contactos/
│
├── main.py                 # Punto de entrada - interfaz (menú CLI)
├── contact.py              # Clase Contact (modelo de datos)
├── contact_manager.py      # Clase ContactManager (lógica de negocio)
├── test_contact_system.py  # Pruebas unitarias (Contact y ContactManager)
│
├── README.md               # Este documento
│
├── INFORME_PRUEBAS.md      # Informe detallado de pruebas (opcional)
├── GUIA_RAPIDA.md          # Guía rápida de uso (opcional)
├── ENTREGA_PORTAFOLIO.md   # Guía de entrega/portafolio (opcional)
└── contactos.json          # Archivo JSON con contactos (se genera al usar el sistema)
