"""
Sistema de Gestión de Contactos - Módulo 2 Alkemy ABP
Desarrollado con POO, listas/diccionarios y pruebas unitarias
"""

class Contacto:
    """Clase que representa un contacto con encapsulación"""
    
    def __init__(self, nombre, telefono, correo, direccion):
        self._nombre = nombre
        self._telefono = telefono
        self._correo = correo
        self._direccion = direccion
    
    def __str__(self):
        return f"{self._nombre} - {self._telefono} - {self._correo}"
    
    def to_dict(self):
        """Convierte contacto a diccionario para almacenamiento"""
        return {
            'nombre': self._nombre,
            'telefono': self._telefono,
            'correo': self._correo,
            'direccion': self._direccion
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea contacto desde diccionario"""
        return cls(data['nombre'], data['telefono'], data['correo'], data['direccion'])
    
    # Getters
    def get_nombre(self): return self._nombre
    def get_telefono(self): return self._telefono
    def get_correo(self): return self._correo
    def get_direccion(self): return self._direccion
    
    # Setters
    def set_nombre(self, nombre): self._nombre = nombre
    def set_telefono(self, telefono): self._telefono = telefono
    def set_correo(self, correo): self._correo = correo
    def set_direccion(self, direccion): self._direccion = direccion

class GestorContactos:
    """Clase principal que gestiona la lista de contactos"""
    
    def __init__(self):
        self.contactos = []  # Lista de diccionarios para persistencia
    
    def agregar_contacto(self, contacto):
        """Agrega nuevo contacto a la lista"""
        self.contactos.append(contacto.to_dict())
        print(f"✓ Contacto '{contacto.get_nombre()}' agregado correctamente")
    
    def eliminar_contacto(self, nombre):
        """Elimina contacto por nombre"""
        for i, contacto in enumerate(self.contactos):
            if contacto['nombre'].lower() == nombre.lower():
                eliminado = self.contactos.pop(i)
                print(f"✓ Contacto '{eliminado['nombre']}' eliminado")
                return True
        print("✗ Contacto no encontrado")
        return False
    
    def editar_contacto(self, nombre, **kwargs):
        """Edita campos específicos de un contacto"""
        for contacto in self.contactos:
            if contacto['nombre'].lower() == nombre.lower():
                for clave, valor in kwargs.items():
                    if clave in contacto:
                        contacto[clave] = valor
                print(f"✓ Contacto '{nombre}' actualizado")
                return True
        print("✗ Contacto no encontrado")
        return False
    
    def buscar_contacto(self, criterio, valor):
        """Busca contactos por nombre o teléfono"""
        resultados = []
        for contacto in self.contactos:
            if (criterio == 'nombre' and valor.lower() in contacto['nombre'].lower()) or \
               (criterio == 'telefono' and valor in contacto['telefono']):
                resultados.append(contacto)
        return resultados
    
    def listar_todos(self):
        """Muestra todos los contactos"""
        if not self.contactos:
            print("No hay contactos registrados")
            return
        print("\n=== LISTA DE CONTACTOS ===")
        for i, contacto in enumerate(self.contactos, 1):
            print(f"{i}. {contacto['nombre']} | {contacto['telefono']} | {contacto['correo']}")

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*50)
    print("         SISTEMA DE GESTIÓN DE CONTACTOS")
    print("="*50)
    print("1. Agregar contacto")
    print("2. Listar todos los contactos")
    print("3. Buscar contacto")
    print("4. Editar contacto")
    print("5. Eliminar contacto")
    print("6. Salir")
    print("-"*50)

def main():
    """Función principal de la aplicación"""
    gestor = GestorContactos()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ").strip()
        
        if opcion == '1':
            nombre = input("Nombre: ").strip()
            telefono = input("Teléfono: ").strip()
            correo = input("Correo: ").strip()
            direccion = input("Dirección: ").strip()
            
            contacto = Contacto(nombre, telefono, correo, direccion)
            gestor.agregar_contacto(contacto)
        
        elif opcion == '2':
            gestor.listar_todos()
        
        elif opcion == '3':
            print("\n🔍 Búsqueda por nombre completo (ej: 'Juan Pérez')")
            nombre_completo = input("Ingrese nombre y apellido: ").strip()
    
            if not nombre_completo:
                print("✗ Debe ingresar un nombre")
                input("Presione Enter para continuar...")
                continue
    
            resultados = gestor.buscar_contacto('nombre', nombre_completo)
    
            if resultados:
                print(f"\n✓ {len(resultados)} contacto(s) encontrado(s):")
                for contacto in resultados:
                    print(f"  • {contacto['nombre']} | {contacto['telefono']} | {contacto['correo']} | {contacto['direccion']}")
            else:
                print("✗ No se encontraron contactos con ese nombre")
    
            input("Presione Enter para continuar...")

        
        elif opcion == '4':
            nombre = input("Nombre del contacto a editar: ").strip()
            print("Deje en blanco los campos que no quiere cambiar")
            nuevos_datos = {
                'nombre': input("Nuevo nombre: ").strip() or None,
                'telefono': input("Nuevo teléfono: ").strip() or None,
                'correo': input("Nuevo correo: ").strip() or None,
                'direccion': input("Nueva dirección: ").strip() or None
            }
            # Filtrar None values
            datos_validos = {k: v for k, v in nuevos_datos.items() if v}
            if datos_validos:
                gestor.editar_contacto(nombre, **datos_validos)
            else:
                print("✗ No se especificaron cambios")
        
        elif opcion == '5':
            nombre = input("Nombre del contacto a eliminar: ").strip()
            gestor.eliminar_contacto(nombre)
        
        elif opcion == '6':
            print("¡Gracias por usar el Sistema de Gestión de Contactos!")
            break
        
        else:
            print("✗ Opción inválida")

# Pruebas unitarias incluidas
def ejecutar_pruebas():
    """Ejecuta pruebas unitarias del sistema"""
    print("Ejecutando pruebas unitarias...")
    
    # Prueba 1: Crear contacto
    contacto_test = Contacto("Juan Pérez", "123456789", "juan@email.com", "Calle 123")
    assert contacto_test.get_nombre() == "Juan Pérez"
    print("✓ Prueba 1: Creación de contacto OK")
    
    # Prueba 2: Gestor básico
    gestor_test = GestorContactos()
    gestor_test.agregar_contacto(contacto_test)
    assert len(gestor_test.contactos) == 1
    print("✓ Prueba 2: Agregar contacto OK")
    
    # Prueba 3: Búsqueda
    resultados = gestor_test.buscar_contacto('nombre', 'juan')
    assert len(resultados) == 1
    print("✓ Prueba 3: Búsqueda OK")
    
    print("🎉 ¡Todas las pruebas pasaron correctamente!")

if __name__ == "__main__":
    # Descomenta para ejecutar pruebas primero
    # ejecutar_pruebas()
    
    main()
