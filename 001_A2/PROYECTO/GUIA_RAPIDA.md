# GUÍA RÁPIDA DE INICIO

## 🚀 Inicio Rápido (3 pasos)

### Paso 1: Descargar el Proyecto
```bash
# Si está en GitHub
git clone https://github.com/tu-usuario/Sistema-Gestion-Contactos.git
cd Sistema-Gestion-Contactos
```

### Paso 2: Ejecutar las Pruebas
```bash
# Verificar que todo funciona correctamente
python test_contact_system.py
```

**Resultado esperado:**
```
test_actualizar_direccion ... ok
test_actualizar_email ... ok
test_actualizar_nombre ... ok
...
Ran 22 tests in 0.02s
OK ✅
```

### Paso 3: Ejecutar la Aplicación
```bash
# Iniciar el sistema interactivo
python main.py
```

---

## 📂 Estructura de Archivos

```
Sistema-Gestion-Contactos/
│
├── 📄 main.py
│   └─ Interfaz interactiva (menú principal)
│
├── 📄 contact.py
│   └─ Clase Contact (modelo de datos)
│
├── 📄 contact_manager.py
│   └─ Gestor de contactos (lógica de negocio)
│
├── 📄 test_contact_system.py
│   └─ Pruebas unitarias (22 tests)
│
├── 📄 ejemplos_uso.py
│   └─ Ejemplos de cómo usar el sistema
│
├── 📄 README.md
│   └─ Documentación completa
│
├── 📄 INFORME_PRUEBAS.md
│   └─ Informe detallado de pruebas
│
├── 📄 GUIA_RAPIDA.md
│   └─ Este archivo
│
├── 📄 requirements.txt
│   └─ Dependencias (ninguna para este proyecto)
│
└── 📄 contactos.json
    └─ Base de datos (se genera automáticamente)
```

---

## 🎮 Cómo Usar la Aplicación

### Menú Principal

```
==================================================
SISTEMA DE GESTIÓN DE CONTACTOS
==================================================
1. Agregar nuevo contacto
2. Ver todos los contactos
3. Buscar contacto por nombre
4. Buscar contacto por teléfono
5. Editar contacto
6. Eliminar contacto
7. Salir
==================================================
```

### Ejemplo de Sesión

**Opción 1: Agregar Contacto**
```
Seleccione una opción: 1

--- AGREGAR NUEVO CONTACTO ---
Nombre: Juan García
Teléfono: +56912345678
Correo: juan@example.com
Dirección: Calle Principal 123

✅ Contacto agregado correctamente
```

**Opción 2: Ver Todos**
```
Seleccione una opción: 2

================================================================================
LISTA DE CONTACTOS
================================================================================

1. Nombre: Juan García
   Teléfono: +56912345678
   Email: juan@example.com
   Dirección: Calle Principal 123

================================================================================
```

**Opción 3: Buscar por Nombre**
```
Seleccione una opción: 3

Ingrese el nombre a buscar: Juan

✅ Se encontraron 1 resultado(s):

Nombre: Juan García
Teléfono: +56912345678
Email: juan@example.com
Dirección: Calle Principal 123
```

---

## 🧪 Ejecutar Pruebas

### Opción 1: Ejecución Simple
```bash
python test_contact_system.py
```

### Opción 2: Ejecución Detallada
```bash
python -m unittest test_contact_system -v
```

### Opción 3: Ejecutar una Prueba Específica
```bash
python -m unittest test_contact_system.TestContact.test_crear_contacto -v
```

---

## 💻 Programar con el Sistema

### Importar el Módulo

```python
from contact_manager import ContactManager
from contact import Contact

# Crear gestor
gestor = ContactManager("contactos.json")

# Agregar contacto
gestor.agregar_contacto(
    "Juan García",
    "+56912345678",
    "juan@example.com",
    "Calle Principal 123"
)

# Buscar por teléfono
contacto = gestor.buscar_por_telefono("+56912345678")
print(contacto)

# Editar
gestor.editar_contacto("+56912345678", nombre="Juan García Pérez")

# Eliminar
gestor.eliminar_contacto("+56912345678")
```

---

## 📝 Requisitos Técnicos

- **Python**: 3.7 o superior
- **Sistema Operativo**: Windows, macOS, Linux
- **Dependencias**: Ninguna (solo librerías estándar)
- **Espacio en disco**: ~100 KB

---

## 🔧 Configuración

### Cambiar Archivo de Almacenamiento

```python
# Por defecto: "contactos.json"
gestor = ContactManager("contactos.json")

# Personalizado
gestor = ContactManager("mis_contactos.json")
gestor = ContactManager("/ruta/completa/contactos.json")
```

---

## ⚠️ Solución de Problemas

### Problema: "ModuleNotFoundError: No module named 'contact'"

**Solución**: Asegúrate de estar en el directorio correcto y que todos los archivos están presentes.

```bash
# Verificar archivos
ls -la *.py

# Verás:
# contact.py
# contact_manager.py
# main.py
# test_contact_system.py
```

### Problema: "FileNotFoundError" al ejecutar

**Solución**: Verifica que tienes permisos de escritura en el directorio.

```bash
# En Linux/macOS
chmod +x main.py

# En Windows, ejecuta el símbolo del sistema como administrador
```

### Problema: Las pruebas fallan

**Solución**: Asegúrate de que tienes Python 3.7+

```bash
python --version
# Debe mostrar: Python 3.7.x o superior
```

---

## 📚 Recursos Adicionales

### Documentación Detallada
- 📖 [README.md](README.md) - Documentación completa
- 📋 [INFORME_PRUEBAS.md](INFORME_PRUEBAS.md) - Detalle de pruebas
- 💡 [ejemplos_uso.py](ejemplos_uso.py) - Ejemplos de código

### Temas Clave de POO

1. **Encapsulación**: Atributos privados con `_`
2. **Propiedades**: Uso de `@property` y `@setter`
3. **Métodos Estáticos**: `from_dict()` y `to_dict()`
4. **Gestión de Excepciones**: Try/except en operaciones

---

## 🎯 Próximos Pasos

### Para Aprender Más
1. Estudia el código en `contact.py` (encapsulación)
2. Revisa `contact_manager.py` (gestión de datos)
3. Explora `test_contact_system.py` (pruebas)

### Para Mejorar el Proyecto
1. Agregar GUI con tkinter
2. Integrar base de datos SQLite
3. Crear API REST con Flask
4. Implementar búsqueda avanzada
5. Agregar importación/exportación CSV

---

## 📞 Contacto y Soporte

Para problemas o preguntas:
1. Revisa la documentación (README.md)
2. Ejecuta las pruebas para validar instalación
3. Consulta ejemplos_uso.py para casos de uso

---

## ✅ Checklist de Verificación

Antes de presentar el proyecto:

- [ ] Todos los archivos están presentes
- [ ] Las pruebas pasan correctamente (22/22)
- [ ] La aplicación interactiva funciona
- [ ] Se pueden agregar, buscar, editar y eliminar contactos
- [ ] Los datos se guardan en JSON
- [ ] El README está completo
- [ ] El código está documentado
- [ ] No hay errores en la consola
- [ ] El proyecto está en GitHub
- [ ] Se incluye el enlace en Moodle

---

## 🎉 ¡Listo para Usar!

Tu Sistema de Gestión de Contactos está completamente funcional.

**¡Felicidades!** 🥳

Ahora puedes:
- ✅ Usar la aplicación para gestionar contactos
- ✅ Estudiar el código para aprender POO
- ✅ Extender con nuevas funcionalidades
- ✅ Compartir en tu portafolio

---

**Creado con ❤️ para el Módulo 2 de Evaluación**

*Última actualización: [Fecha]*
