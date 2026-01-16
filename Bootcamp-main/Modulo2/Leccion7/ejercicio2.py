class Empleado:
    def __init__(self, nombre: str, salario: float):
        self._nombre = None
        self.nombre = nombre  # pasa por setter
        self.salario = float(salario)

    # 4) Propiedad nombre con getter/setter (valida que sea string)
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):
            raise TypeError("El nombre debe ser un string.")
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip().title()

    # 1) Método mostrar_info()
    def mostrar_info(self):
        print(f"Empleado: {self.nombre} | Salario: {self.salario:.2f}")

    # 1) Método obtener_bono() (10% del salario)
    def obtener_bono(self) -> float:
        return self.salario * 0.10


# 2) Clase hija Gerente: sobrescribe obtener_bono() con 20%
class Gerente(Empleado):
    def obtener_bono(self) -> float:
        return self.salario * 0.20

    def mostrar_info(self):
        print(f"Gerente: {self.nombre} | Salario: {self.salario:.2f}")


# 2) Clase hija Técnico: agrega especialidad y redefine mostrar_info()
class Tecnico(Empleado):
    def __init__(self, nombre: str, salario: float, especialidad: str):
        super().__init__(nombre, salario)
        self.especialidad = especialidad

    def mostrar_info(self):
        print(
            f"Técnico: {self.nombre} | Especialidad: {self.especialidad} | "
            f"Salario: {self.salario:.2f}"
        )


# 3) Polimorfismo: recibe cualquier objeto "empleado" y muestra info
def ver_info(empleado):
    empleado.mostrar_info()
    print(f"Bono: {empleado.obtener_bono():.2f}")
    print("-" * 35)


if __name__ == "__main__":
    # 5) Instanciar objetos de cada clase
    e1 = Empleado("ana", 1000)
    g1 = Gerente("carlos", 2500)
    t1 = Tecnico("maria", 1800, "Redes")

    # Guardarlos en lista y recorrer
    empleados = [e1, g1, t1]

    for emp in empleados:
        ver_info(emp)
