class Empleado:
    def __init__(self, nombre: str, rol: str, salario: float):
        self.nombre = nombre
        self.rol = rol
        self.salario = float(salario)

    def mostrar(self):
        print(f"Nombre: {self.nombre} | Rol: {self.rol} | Salario: {self.salario:.2f}")

    def actualizar_salario(self, nuevo_monto: float):
        nuevo_monto = float(nuevo_monto)
        if nuevo_monto <= 0:
            print(f"⚠️ No se actualizó el salario de {self.nombre}: monto inválido.")
            return
        self.salario = nuevo_monto

    def gana_mas_que(self, promedio: float) -> bool:
        return self.salario > promedio

    def __str__(self):
        return f"Empleado(nombre='{self.nombre}', rol='{self.rol}', salario={self.salario:.2f})"


# 3) Instanciar 3 empleados y guardarlos en una lista
empleados = [
    Empleado("Ana", "Analista", 1200),
    Empleado("Juan", "Desarrollador", 1500),
    Empleado("María", "Jefa de Proyecto", 2000),
]

# (Opcional) actualizar salario de alguien para mostrar que el método funciona
empleados[0].actualizar_salario(1300)

# 4) Recorrer lista y mostrar info
print("=== Lista de empleados ===")
for emp in empleados:
    emp.mostrar()

# Calcular el promedio de salario
promedio_salario = sum(emp.salario for emp in empleados) / len(empleados)
print(f"\nPromedio general de salario: {promedio_salario:.2f}")

# Usar gana_mas_que() para informar quién está por encima del promedio
print("\n=== Empleados por encima del promedio ===")
for emp in empleados:
    if emp.gana_mas_que(promedio_salario):
        print(f"- {emp.nombre} ({emp.rol}) está por encima del promedio.")
