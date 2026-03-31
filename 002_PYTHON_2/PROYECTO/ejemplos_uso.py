"""
Ejemplos de Uso - Sistema de Gestión de Contactos
Demostraciones de cómo utilizar el sistema
"""

# EJEMPLO 1: Uso Básico del Sistema
# ======================================

from contact import Contact
from contact_manager import ContactManager

# Crear un gestor de contactos
gestor = ContactManager("mi_contactos.json")

# Agregar algunos contactos
gestor.agregar_contacto(
    "Juan García",
    "+56912345678",
    "juan@example.com",
    "Calle Principal 123, Santiago"
)

gestor.agregar_contacto(
    "Ana Silva",
    "+56987654321",
    "ana@example.com",
    "Avenida Central 456, Valparaíso"
)

gestor.agregar_contacto(
    "Pedro López",
    "+56911111111",
    "pedro@example.com",
    "Pasaje del Bosque 789, Concepción"
)

print("✅ Contactos agregados correctamente")
print(f"Total de contactos: {gestor.obtener_cantidad_contactos()}")


# EJEMPLO 2: Buscar Contactos
# ======================================

# Buscar por nombre (búsqueda parcial)
resultados = gestor.buscar_por_nombre("García")
print(f"\n🔍 Búsqueda por 'García': {len(resultados)} resultado(s)")
for contacto in resultados:
    print(f"  - {contacto.nombre} ({contacto.telefono})")

# Buscar por teléfono (búsqueda exacta)
contacto = gestor.buscar_por_telefono("+56987654321")
if contacto:
    print(f"\n🔍 Contacto encontrado:")
    print(contacto)


# EJEMPLO 3: Ver Todos los Contactos
# ======================================

todos = gestor.obtener_todos_contactos()
print(f"\n📋 Lista de Todos los Contactos ({len(todos)} total):")
for i, contacto in enumerate(todos, 1):
    print(f"\n{i}. {contacto.nombre}")
    print(f"   Teléfono: {contacto.telefono}")
    print(f"   Email: {contacto.email}")
    print(f"   Dirección: {contacto.direccion}")


# EJEMPLO 4: Editar Contacto
# ======================================

print("\n✏️ Editando contacto...")
gestor.editar_contacto(
    "+56912345678",
    nombre="Juan García Rodríguez",
    email="juan.garcia@newmail.com"
)

contacto_editado = gestor.buscar_