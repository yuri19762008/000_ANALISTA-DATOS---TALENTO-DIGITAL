# Definición de clases en Python

class Perro: 
    def __init__(self, nombre, edad): 
        self.nombre = nombre 
        self.edad = edad  
    def ladrar(self): 
        print("¡Guau!")
            
mi_perro = Perro("Rex", 3)
mi_perro.ladrar()

# Métodos especiales adicionales
class Perro: 
    def __init__(self, nombre, edad): 
        self.nombre = nombre 
        self.edad = edad  
    def __str__(self): 
        return f"Perro: {self.nombre}, {self.edad} años"
    
""" Tipos de atributos en Python """
# Ejemplo completo: tipos de atributos en Python
class Perro:
    # ATRIBUTO DE CLASE
    especie = "Canino"

    def __init__(self, nombre, edad):
        # ATRIBUTOS PÚBLICOS
        self.nombre = nombre
        self.edad = edad

        # ATRIBUTO "PRIVADO" (por convención)
        self._energia = 100

    def jugar(self):
        self._energia -= 10
        print(f"{self.nombre} tiene {self._energia} de energía")

# 1. Atributos públicos
# Se pueden acceder y modificar directamente desde fuera:
p = Perro("Rex", 3)

print(p.nombre)   # Rex
p.edad = 4
print(p.edad)     # 4

# 2. Atributos “privados” (por convención)
# Se escriben con un guion bajo y no deberían modificarse directamente:
print(p._energia)   # 100 

# 3. Atributos de clase
# Son compartidos por todas las instancias:
p1 = Perro("Rex", 3)
p2 = Perro("Malva", 5)

print(p1.especie)
print(p2.especie)

# Ejemplo completo: tipos de métodos en Python
class Empleado:
    empresa = "Tech Chile"   # atributo de clase

    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

    # 1️⃣ MÉTODO PÚBLICO
    def mostrar_info(self):
        return f"{self.nombre} gana ${self.salario}"

    # 2️⃣ MÉTODO "PRIVADO" (por convención)
    def _calcular_bono(self):
        return self.salario * 0.10

    # Método público que usa uno privado
    def obtener_bono(self):
        return self._calcular_bono()

    # 3️⃣ MÉTODO DE CLASE
    @classmethod
    def cambiar_empresa(cls, nuevo_nombre):
        cls.empresa = nuevo_nombre

    # 4️⃣ MÉTODO ESTÁTICO
    @staticmethod
    def es_salario_valido(salario):
        return salario > 0
    
# Método público: Se puede llamar desde fuera del objeto:
e = Empleado("Ana", 1200)
print(e.mostrar_info())

# Método “privado” (_): Está pensado para uso interno de la clase:
print(e.obtener_bono())

# Método de clase (@classmethod): Trabaja con la clase, no con una instancia:
Empleado.cambiar_empresa("Data Chile")
print(Empleado.empresa)

# Método estático (@staticmethod): No depende ni del objeto ni de la clase:
print(Empleado.es_salario_valido(1500))  # True
print(Empleado.es_salario_valido(-500))  # False



#### Parte 2 #####
# Métodos comunes de strings
# upper(): Convierte todos los caracteres a mayúsculas.
texto = "Hola Python"
print(texto.upper())

# lower(): Convierte todos los caracteres a minúsculas.
texto = "Hola PYTHON"
print(texto.lower())

# strip(): Elimina espacios en blanco al inicio y al final de la cadena.
texto = "   Hola Python   "
print(texto.strip())

# replace(): Reemplaza una subcadena por otra.
texto = "Hola Python"
nuevo_texto = texto.replace("Python", "Mundo")
print(nuevo_texto)

# split():Divide una cadena en una lista de subcadenas según un separador.
texto = "Ana,Juan,María"
lista = texto.split(",")
print(lista)

# Métodos de búsqueda en strings
# find() y index()
texto = "Python es divertido"

# find(): devuelve: la posición si encuentra la subcadena -1 si no la encuentra
print(texto.find("es"))
print(texto.find("Java"))

# index(): devuelve la posición si existe lanza una excepción si no la encuentra
print(texto.index("es"))
print(texto.index("Java"))  # genera error

# startswith() y endswith()
archivo = "reporte_final.pdf"

print(archivo.startswith("reporte"))
print(archivo.endswith(".pdf"))

# count()
mensaje = "hola hola hola"
print(mensaje.count("hola"))

# Métodos de validación de strings
# isalpha(): Verifica si todos los caracteres son letras (no permite espacios ni números).
texto1 = "Python"
texto2 = "Python3"
texto3 = "Hola Mundo"

print(texto1.isalpha())  # True
print(texto2.isalpha())  # False (tiene número)
print(texto3.isalpha())  # False (tiene espacio)


# isdigit(): Verifica si todos los caracteres son dígitos.
valor1 = "12345"
valor2 = "12a45"
valor3 = "12.5"

print(valor1.isdigit())  # True
print(valor2.isdigit())  # False
print(valor3.isdigit())  # False (el punto no es un dígito)

# isalnum(): Verifica si solo tiene letras o números (sin espacios ni símbolos).
dato1 = "Python3"
dato2 = "Python 3"
dato3 = "Python_3"

print(dato1.isalnum())  # True
print(dato2.isalnum())  # False (espacio)
print(dato3.isalnum())  # False (_ no es alfanumérico)

# islower() y isupper(): Verifican si todos los caracteres alfabéticos están en minúscula o mayúscula.
texto1 = "hola"
texto2 = "HOLA"
texto3 = "Hola"

print(texto1.islower())  # True
print(texto2.isupper())  # True
print(texto3.islower())  # False
print(texto3.isupper())  # False

# Mini ejemplo práctico
nombre = input("Ingrese su nombre: ")

if nombre.isalpha():
    print("Nombre válido")
else:
    print("El nombre solo debe contener letras")




# Interpolación de strings
# Definir variables
nombre = "Ana"
edad = 25

# Usar una f-string para construir un mensaje
mensaje = f"Hola, me llamo {nombre} y tengo {edad} años."

# Imprimir el mensaje
print(mensaje)  # Imprime: Hola, me llamo Ana y tengo 25 años.

# Inmutabilidad de strings
s = "hello"
s = s.upper()  # Crea un nuevo string
print(s)  # Imprime: HELLO

# Ejemplo completo de clase en Python.
class Empleado:
    # Atributo de clase
    empresa = "TechCorp"

    # Constructor
    def __init__(self, nombre, salario):
        # Atributos de instancia
        self.nombre = nombre
        self._salario = salario  # Atributo privado

    # Método público
    def mostrar_info(self):
        return f"Empleado: {self.nombre}, Empresa: {self.empresa}"

    # Método privado
    def _calcular_bono(self):
        return self._salario * 0.1

    # Método público que usa el método privado
    def obtener_bono(self):
        return f"Bono anual: {self._calcular_bono()}"

# uso de la clase empleado
# Crear instancias de la clase Empleado
emp1 = Empleado("Ana López", 50000)
emp2 = Empleado("Carlos Ruiz", 60000)

# Acceder a atributos y métodos
print(emp1.nombre)             # Ana López
print(emp1.empresa)            # TechCorp
print(emp1.mostrar_info())     # Empleado: Ana López, Empresa: TechCorp
print(emp1.obtener_bono())     # Bono anual: 5000.0

# Modificar el atributo de clase
Empleado.empresa = "NewTech"

# Ver cómo afecta a todas las instancias
print(emp1.empresa)            # NewTech
print(emp2.empresa)            # NewTech

# Herencia en acción
# Definir una subclase llamada Gerente que hereda de Empleado
class Gerente(Empleado):
    def __init__(self, nombre, salario, departamento):
        # Llamar al constructor de la clase padre
        super().__init__(nombre, salario)
        self.departamento = departamento

    # Sobrescribir un método de la clase padre
    def mostrar_info(self):
        return f"Gerente: {self.nombre}, Dept: {self.departamento}"

    # Método específico de esta clase
    def asignar_tareas(self):
        return f"Asignando tareas en {self.departamento}"
# Crear instancia de la clase hija
gerente = Gerente("Laura Martínez", 80000, "Desarrollo")

# Usar métodos sobrescritos y heredados
print(gerente.mostrar_info())     # Gerente: Laura Martínez, Dept: Desarrollo
print(gerente.obtener_bono())     # Bono anual: 8000.0
print(gerente.asignar_tareas())   # Asignando tareas en Desarrollo

# Polimorfismo en acción
# Clase base
class Animal:
    def sonido(self):
        pass  # Método vacío (se espera que sea sobrescrito)

# Subclase Perro
class Perro(Animal):
    def sonido(self):
        return "¡Guau!"

# Subclase Gato
class Gato(Animal):
    def sonido(self):
        return "¡Miau!"

# Función que acepta cualquier objeto que implemente el método sonido
def hacer_sonido(animal):
    print(animal.sonido())
# Crear instancias de las subclases
perro = Perro()
gato = Gato()
# Llamar a la función con diferentes objetos
hacer_sonido(perro) # ¡Guau!
hacer_sonido(gato) # ¡Miau! 


# Ejemplo de métodos especiales
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Método que define la representación en texto
    def __str__(self):
        return f"({self.x}, {self.y})"

    # Método que define la suma con otro objeto Punto
    def __add__(self, other):
        return Punto(self.x + other.x, self.y + other.y)

    # Método que define la longitud (módulo del vector)
    def __len__(self):
        return int((self.x**2 + self.y**2)**0.5)

# Crear dos objetos Punto
p1 = Punto(3, 4)
p2 = Punto(2, 3)
# Pruebas
print(p1) # (3, 4)
print(p1 + p2) # (5, 7)
print(len(p1)) # 5 

# Propiedades en Python
class Persona:
    def __init__(self, nombre):
        self._nombre = nombre  # Atributo privado

    # Getter: permite acceder al atributo como si fuera público
    @property
    def nombre(self):
        return self._nombre

    # Setter: define cómo modificar el atributo, con validación
    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):
            raise TypeError("El nombre debe ser una cadena")
        self._nombre = valor

p = Persona("Juan")
print(p.nombre)       # Juan

p.nombre = "Ana"      # Usa el setter
print(p.nombre)       # Ana

p.nombre = 123        # Lanzaría TypeError

# Clases abstractas en Python
from abc import ABC, abstractmethod
# Clase abstracta
class FormaGeometrica(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimetro(self):
        pass

# Subclase que implementa todos los métodos abstractos
class Rectangulo(FormaGeometrica):
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto


def area(self):
    return self.ancho * self.alto

def perimetro(self):
    return 2 * (self.ancho + self.alto)
# No se puede instanciar una clase abstracta directamente
# forma = FormaGeometrica() # ❌ Esto lanzaría un error
# Crear una instancia válida de una subclase concreta
rect = Rectangulo(5, 3)
print(rect.area()) # 15
print(rect.perimetro()) # 16

# Ejemplo de clase bien documentada
class CuentaBancaria:
    def __init__(self, titular, saldo_inicial=0):
        """
        Inicializa una nueva cuenta bancaria.

        Args:
            titular (str): Nombre del titular de la cuenta.
            saldo_inicial (float, optional): Saldo inicial. Por defecto 0.
        """
        self.titular = titular
        self._saldo = saldo_inicial
        self._numero = self._generar_numero()


    def depositar(self, cantidad):
        """
        Añade dinero a la cuenta.

        Args:
            cantidad (float): Cantidad a depositar.

        Returns:
            float: Nuevo saldo de la cuenta.

        Raises:
            ValueError: Si la cantidad es negativa.
        """
        if cantidad < 0:
            raise ValueError("No se puede depositar una cantidad negativa")
        self._saldo += cantidad
        return self._saldo






