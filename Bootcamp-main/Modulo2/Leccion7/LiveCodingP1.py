#Paso 1 y 2) Crear la clase Empleado con __init__
class Empleado:
    def __init__(self, nombre, rol, salario):
        self.nombre = nombre
        self.rol = rol
        self.salario = salario

# prueba
e1 = Empleado("Ana", "Analista", 1200)
print(e1.nombre, e1.rol, e1.salario)


# Paso 3) Agregar método mostrar_info() que imprima los datos
class Empleado:
    def __init__(self, nombre, rol, salario):
        self.nombre = nombre
        self.rol = rol
        self.salario = salario

    def mostrar_info(self):
        print(f"Nombre: {self.nombre} | Rol: {self.rol} | Salario: ${self.salario}")

#prueba
e1 = Empleado("Ana", "Analista", 1200)
e1.mostrar_info()

# Paso 4) Agregar método actualizar_salario(nuevo_monto)
class Empleado:
    def __init__(self, nombre, rol, salario):
        self.nombre = nombre
        self.rol = rol
        self.salario = salario

    def mostrar_info(self):
        print(f"Nombre: {self.nombre} | Rol: {self.rol} | Salario: ${self.salario}")

    def actualizar_salario(self, nuevo_monto):
        self.salario = nuevo_monto

# prueba
e1 = Empleado("Ana", "Analista", 1200)
e1.mostrar_info()
e1.actualizar_salario(1400)
e1.mostrar_info()


# Paso 5) Agregar __str__() para representación legible
class Empleado:
    def __init__(self, nombre, rol, salario):
        self.nombre = nombre
        self.rol = rol
        self.salario = salario

    def mostrar_info(self):
        print(f"Nombre: {self.nombre} | Rol: {self.rol} | Salario: ${self.salario}")

    def actualizar_salario(self, nuevo_monto):
        self.salario = nuevo_monto

    def __str__(self):
        return f"Empleado({self.nombre}, {self.rol}, ${self.salario})"

#prueba
e1 = Empleado("Ana", "Analista", 1200)
print(e1)


# Paso 6) Instanciar varios empleados y mostrar su información
e1 = Empleado("Ana", "Analista", 1200)
e2 = Empleado("Juan", "Desarrollador", 1500)
e3 = Empleado("María", "Jefa de Proyecto", 2000)

e1.mostrar_info()
e2.mostrar_info()
e3.mostrar_info()

# Paso 7) Acceder a atributos y modificarlos desde fuera y desde métodos
# Desde fuera:
e1.salario = 1300
e1.mostrar_info()


# Desde un método:
e1.actualizar_salario(1600)
e1.mostrar_info()

# Paso 8) Usar una lista de objetos y recorrerla
empleados = [e1, e2, e3]

for emp in empleados:
    emp.mostrar_info()
