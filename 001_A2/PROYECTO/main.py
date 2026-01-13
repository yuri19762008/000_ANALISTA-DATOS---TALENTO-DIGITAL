"""Sistema de Gestión de Contactos - Módulo principal"""

from contact_manager import ContactManager


def mostrar_menu():
    """Muestra el menú principal de la aplicación"""
    print("\n" + "=" * 50)
    print("SISTEMA DE GESTIÓN DE CONTACTOS")
    print("=" * 50)
    print("1. Agregar nuevo contacto")
    print("2. Ver todos los contactos")
    print("3. Buscar contacto por nombre")
    print("4. Buscar contacto por teléfono")
    print("5. Editar contacto")
    print("6. Eliminar contacto")
    print("7. Salir")
    print("=" * 50)


def agregar_contacto(gestor: ContactManager):
    """Permite agregar un nuevo contacto"""
    try:
        print("\n--- AGREGAR NUEVO CONTACTO ---")
        nombre = input("Nombre: ").strip()
        if not nombre:
            print("❌ El nombre no puede estar vacío")
            return

        telefono = input("Teléfono: ").strip()
        if not telefono:
            print("❌ El teléfono no puede estar vacío")
            return

        email = input("Correo: ").strip()
        if not email:
            print("❌ El correo no puede estar vacío")
            return

        direccion = input("Dirección: ").strip()
        if not direccion:
            print("❌ La dirección no puede estar vacía")
            return

        gestor.agregar_contacto(nombre, telefono, email, direccion)
        print("✅ Contacto agregado correctamente")
    except Exception as e:
        print(f"❌ Error al agregar contacto: {e}")


def ver_todos_contactos(gestor: ContactManager):
    """Muestra todos los contactos registrados"""
    contactos = gestor.obtener_todos_contactos()

    if not contactos:
        print("\n❌ No hay contactos registrados")
        return

    print("\n" + "=" * 80)
    print("LISTA DE CONTACTOS")
    print("=" * 80)
    for i, contacto in enumerate(contactos, 1):
        print(f"\n{i}. {contacto}")
    print("=" * 80)


def buscar_por_nombre(gestor: ContactManager):
    """Busca un contacto por nombre"""
    nombre = input("\nIngrese el nombre a buscar: ").strip()
    resultados = gestor.buscar_por_nombre(nombre)

    if not resultados:
        print(f"❌ No se encontraron contactos con el nombre '{nombre}'")
        return

    print(f"\n✅ Se encontraron {len(resultados)} resultado(s):")
    for contacto in resultados:
        print(f"\n{contacto}")


def buscar_por_telefono(gestor: ContactManager):
    """Busca un contacto por teléfono"""
    telefono = input("\nIngrese el teléfono a buscar: ").strip()
    contacto = gestor.buscar_por_telefono(telefono)

    if not contacto:
        print(f"❌ No se encontró contacto con el teléfono '{telefono}'")
        return

    print("\n✅ Contacto encontrado:")
    print(f"\n{contacto}")


def editar_contacto(gestor: ContactManager):
    """Edita un contacto existente"""
    try:
        telefono = input("\nIngrese el teléfono del contacto a editar: ").strip()
        contacto = gestor.buscar_por_telefono(telefono)

        if not contacto:
            print(f"❌ No se encontró contacto con el teléfono '{telefono}'")
            return

        print(f"\nContacto actual:\n{contacto}")
        print("\nDejar en blanco para mantener el valor actual")

        nombre = input("Nuevo nombre (o Enter para mantener): ").strip() or contacto.nombre
        nuevo_email = input("Nuevo correo (o Enter para mantener): ").strip() or contacto.email
        nueva_direccion = input("Nueva dirección (o Enter para mantener): ").strip() or contacto.direccion

        gestor.editar_contacto(telefono, nombre, nuevo_email, nueva_direccion)
        print("✅ Contacto editado correctamente")
    except Exception as e:
        print(f"❌ Error al editar contacto: {e}")


def eliminar_contacto(gestor: ContactManager):
    """Elimina un contacto"""
    try:
        telefono = input("\nIngrese el teléfono del contacto a eliminar: ").strip()
        contacto = gestor.buscar_por_telefono(telefono)

        if not contacto:
            print(f"❌ No se encontró contacto con el teléfono '{telefono}'")
            return

        print(f"\nContacto a eliminar:\n{contacto}")
        confirmacion = input("\n¿Está seguro de que desea eliminar este contacto? (S/N): ").strip().upper()

        if confirmacion == "S":
            gestor.eliminar_contacto(telefono)
            print("✅ Contacto eliminado correctamente")
        else:
            print("❌ Operación cancelada")
    except Exception as e:
        print(f"❌ Error al eliminar contacto: {e}")


def main():
    """Función principal de la aplicación"""
    gestor = ContactManager("contactos.json")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_contacto(gestor)
        elif opcion == "2":
            ver_todos_contactos(gestor)
        elif opcion == "3":
            buscar_por_nombre(gestor)
        elif opcion == "4":
            buscar_por_telefono(gestor)
        elif opcion == "5":
            editar_contacto(gestor)
        elif opcion == "6":
            eliminar_contacto(gestor)
        elif opcion == "7":
            print("\n✅ ¡Gracias por usar el Sistema de Gestión de Contactos!")
            break
        else:
            print("❌ Opción no válida. Intente de nuevo")


if __name__ == "__main__":
    main()
