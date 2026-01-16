class Empleado:
    def __init__(self, nombre, rol, salario):
        self.nombre = nombre
        self.rol = rol
        self.salario = salario

    def mostrar_info(self):
        print(f" Nombre: {self.nombre}, Rol: {self.rol}, Salario: {self.salario}")

    def actualizar_salario(self,nuevo_monto):
        self.salario = nuevo_monto

    def __str__(self):
        return f"Empleado({self.nombre},{self.rol},${self.salario})"
    

e1 = Empleado("Ana", "Analista", 1200)
e2 = Empleado("Juan", "Desarrollador", 1500)
e3 = Empleado("María", "Jefa de Proyecto", 2000)

e1.actualizar_salario(1600)
#print(e1)

empleados = [e1,e2,e3]
for e in empleados:
    e.mostrar_info()






