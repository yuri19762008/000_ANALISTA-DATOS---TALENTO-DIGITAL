# Paso 1) Clase base Empleado con atributos y mostrar_info()
class Empleado:
    def __init__(self, nombre: str, rol: str, salario: float):
        self.nombre = nombre
        self.rol = rol
        self.salario = float(salario)

    def mostrar_info(self):
        return f"Empleado: {self.nombre} | Rol: {self.rol} | Salario: ${self.salario:.0f}"


# prueba
e = Empleado("Ana", "Analista", 1200)
print(e.mostrar_info())

# Paso 2) Herencia: clase Gerente que hereda y sobrescribe métodos
class Gerente(Empleado):
    def __init__(self, nombre: str, salario: float, equipo_size: int):
        super().__init__(nombre, "Gerente", salario)
        self.equipo_size = equipo_size

    def mostrar_info(self):
        return f"Gerente: {self.nombre} | Equipo: {self.equipo_size} | Salario: ${self.salario:.0f}"

# prueba
g = Gerente("Juan", 2500, 8)
print(g.mostrar_info())

# Paso 3) Método obtener_bono() + encapsulación con _atributo
# Primero, en Empleado agregamos un atributo encapsulado y el bono base:
class Empleado:
    def __init__(self, nombre: str, rol: str, salario: float):
        self._nombre = nombre      # convención: “interno”
        self.rol = rol
        self.salario = float(salario)

    def mostrar_info(self):
        return f"Empleado: {self._nombre} | Rol: {self.rol} | Salario: ${self.salario:.0f}"

    def obtener_bono(self):
        return self.salario * 0.10

# Ahora en Gerente sobrescribimos el bono:
class Gerente(Empleado):
    def __init__(self, nombre: str, salario: float, equipo_size: int):
        super().__init__(nombre, "Gerente", salario)
        self.equipo_size = equipo_size

    def mostrar_info(self):
        return f"Gerente: {self._nombre} | Equipo: {self.equipo_size} | Salario: ${self.salario:.0f}"

    def obtener_bono(self):
        return self.salario * 0.20

# Prueba
e = Empleado("Ana", "Analista", 1200)
g = Gerente("Juan", 2500, 8)

print(e.obtener_bono())
print(g.obtener_bono())

# Paso 4) @property y @setter para controlar el nombre
# En Empleado, agregamos propiedad nombre para acceder/validar _nombre:
class Empleado:
    def __init__(self, nombre: str, rol: str, salario: float):
        self._nombre = nombre
        self.rol = rol
        self.salario = float(salario)

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if not isinstance(nuevo_nombre, str) or not nuevo_nombre.strip():
            raise ValueError("El nombre debe ser un string no vacío.")
        self._nombre = nuevo_nombre.strip()

    def mostrar_info(self):
        return f"Empleado: {self.nombre} | Rol: {self.rol} | Salario: ${self.salario:.0f}"

    def obtener_bono(self):
        return self.salario * 0.10

# prueba
e = Empleado(" Ana  ", "Analista", 1200)
e.nombre = "  Ana María  "
print(e.nombre)          # Ana María
# e.nombre = ""          # descomentar para ver el error


# Paso 5) __str__() para impresión amigable
# En Empleado:
def __str__(self):
    return self.mostrar_info()

# prueba
print(e)   # llama automáticamente a __str__

# Paso 6) Clase Desarrollador con método exclusivo
class Desarrollador(Empleado):
    def __init__(self, nombre: str, salario: float, stack: str):
        super().__init__(nombre, "Desarrollador", salario)
        self.stack = stack

    def mostrar_info(self):
        return f"Desarrollador: {self.nombre} | Stack: {self.stack} | Salario: ${self.salario:.0f}"

    def escribir_codigo(self):
        return f"{self.nombre} está programando en {self.stack}."

# prueba
d = Desarrollador("Malva", 1800, "Python")
print(d.mostrar_info())
print(d.escribir_codigo())

# Paso 7) Función mostrar_datos(objeto) para demostrar polimorfismo
def mostrar_datos(objeto):
    print(objeto.mostrar_info())
    print(f"Bono: ${objeto.obtener_bono():.0f}")
    print("-" * 40)

# prueba
empleados = [
    Empleado("Ana", "Analista", 1200),
    Gerente("Juan", 2500, 8),
    Desarrollador("Malva", 1800, "Python")
]

for obj in empleados:
    mostrar_datos(obj)

# Paso 8) Clase abstracta con métodos obligatorios (ABC)
# Acá lo más limpio es crear una base abstracta y hacer que Empleado herede de ella.
from abc import ABC, abstractmethod

class EmpleadoBase(ABC):
    @abstractmethod
    def mostrar_info(self):
        pass

    @abstractmethod
    def obtener_bono(self):
        pass

# Y al inicio de Empleado:
class Empleado(EmpleadoBase):
    ...

"""Con eso ya se obliga a que cualquier clase hija tenga esos métodos (o herede una implementación válida)."""
