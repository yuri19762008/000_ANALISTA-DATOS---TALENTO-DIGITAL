### Ejemplo de función en python

def saludo():    
    print("¡Hola, mundo!")
    
# Llamando a la función 
saludo()


### ejemplo de función con docstring
def saludo():
    """Esta función imprime un saludo de bienvenida."""
    print("¡Hola! Bienvenido al programa.")


#### función Len()
texto = "Hola, mundo"
longitud = len(texto)
print(longitud)  # Imprime: 11

lista = [1, 2, 3, 4, 5]
longitud = len(lista)
print(longitud)  # Imprime: 5
    
### Funciones print() e input()
nombre = input("¿Cuál es tu nombre? ")
print("Hola,", nombre)

### Función type()
x = 10
y = "Hola"
z = [1, 2, 3]
print(type(x))  
print(type(y))  
print(type(z))  

## Funciones de conversiones de tipo
# Conversión de string a entero
numero_texto = "123"
numero = int(numero_texto)
print(numero + 10)  # 133
# Conversión de entero a string
numero = 456
texto = str(numero)
print("El número es: " + texto)

####Ejemplo de función personalizada

def cuadrado(numero):    
    """    Calcula el cuadrado de un número.        
    Args:     
    numero:   El número a elevar al cuadrado            
    Returns:  El cuadrado del número    """ 
    return numero ** 2

# Uso de la función
resultado = cuadrado(5)
print(resultado)  # Imprime: 25

###Parámetros y retorno de funciones

def suma(a, b):
    return a + b

resultado = suma(5, 3)
print(resultado)  # Salida: 8

### Funciones con parámetros predeterminados
def saludo(nombre="Usuario"):
    print("Hola,", nombre)

saludo()           # Salida: Hola, Usuario
saludo("Ana")      # Salida: Hola, Ana


## Ejemplo de módulo
# Archivo: operaciones.py
def sumar(a, b):    
    """Suma dos números y devuelve el resultado."""
    return a + b

####Importación de un módulo
# Importar el módulo operaciones
import operaciones
# Usar la función sumar del módulo
resultado = operaciones.sumar(5, 3)
print(resultado)  # Imprime: 8


### Módulo os para archivos
import os

# Listar archivos en el directorio actual
archivos = os.listdir('.')
print(archivos)

# Verificar si un archivo existe
existe = os.path.exists('archivo.txt')
print(existe)

# Crear un directorio
os.mkdir('nuevo_directorio')


###### PARTE 2 ######

#Importación de módulos en Python
# Importación básica
import math# Usar una función del módulo
resultado = math.sqrt(16)
print(resultado) # Imprime: 4.0


#Importación con alias
# Importar con alias
import numpy as np
# Usar el alias para acceder a funciones
array = np.array([1, 2, 3, 4, 5])
print(array)

import math as m
# Usar el alias para acceder a funciones
print(m.sqrt(16))  # Salida: 4.0

# Importar funciones específicas
from math import sqrt, pi# Usar las funciones directamente
resultado = sqrt(16)
print(resultado)  # Imprime: 4.0
print(pi)  # Imprime: 3.141592653589793


#Ejemplo completo de importación
from datetime import datetime
import os as sistema
from random import randint, choice

# Uso de las importaciones
raiz = math.sqrt(25)            # Calcular la raíz cuadrada de 25
ahora = datetime.now()          # Obtener la fecha y hora actual
archivos = sistema.listdir('.') # Listar archivos en el directorio actual
numero = randint(1, 10)         # Generar un número aleatorio entre 1 y 10
fruta = choice(['manzana', 'pera', 'uva']) # Elegir una fruta al azar

print(raiz, "\n" , ahora, "\n", archivos, "\n", numero, "\n", fruta)

## Operaciones básicas con math
import math
# Raíz cuadrada
raiz = math.sqrt(16)
print(raiz)  # 4.0
# Potencia
potencia = math.pow(2, 3)
print(potencia)  # 8.0
# Logaritmo natural
logaritmo = math.log(10)
print(logaritmo)  # 2.302585092994046
# Logaritmo base 10
logaritmo10 = math.log10(100)
print(logaritmo10)  # 2.0

import math

# Redondeo hacia arriba
techo = math.ceil(4.2)
print(techo)  # Salida: 5

# Redondeo hacia abajo
piso = math.floor(4.8)
print(piso)  # Salida: 4

# Truncamiento (elimina la parte decimal)
truncado = math.trunc(4.9)
print(truncado)  # Salida: 4

##Funciones básicas de estadística
import statistics

# Lista de datos
datos = [2, 5, 7, 9, 12, 5, 8, 9]

# Media (promedio)
media = statistics.mean(datos)
print(f"Media: {media}")  # Salida: 7.125

# Mediana (valor central)
mediana = statistics.median(datos)
print(f"Mediana: {mediana}")  # Salida: 7.5

# Moda (valor más frecuente)
moda = statistics.mode(datos)
print(f"Moda: {moda}")  # Salida: 5
# Desviación estándar
desviacion = statistics.stdev(datos)
print(f"Desviación estándar: {desviacion}")  # Salida: 3.1622776601683795


## Cálculos avanzados con statistics
import statistics

# Lista de datos
datos = [2, 5, 7, 9, 12, 5, 8, 9]

# Desviación estándar
desviacion = statistics.stdev(datos)
print(f"Desviación estándar: {desviacion}")

# Varianza
varianza = statistics.variance(datos)
print(f"Varianza: {varianza}")

# Cuartiles
q1 = statistics.quantiles(datos, n=4)[0]  # Primer cuartil
q2 = statistics.quantiles(datos, n=4)[1]  # Segundo cuartil (mediana)
q3 = statistics.quantiles(datos, n=4)[2]  # Tercer cuartil
print(f"Cuartiles: {q1}, {q2}, {q3}")

##Funciones de orden superior
#Función map()
# Aplicar una función a cada elemento de una lista
numeros = [1, 2, 3, 4, 5] 
#Usando map con una función definida
def cuadrado(x): return x ** 2

resultado = map(cuadrado, numeros)
print(list(resultado)) # [1, 4, 9, 16, 25]

# Usando map con una función lambda
resultado = map(lambda x: x * 3, numeros)

print(list(resultado)) # [3, 6, 9, 12, 15]

#Función filter()
# Seleccionar elementos que cumplen una condición
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]# Filtrar números pares
pares = filter(lambda x: x % 2 == 0, numeros)
print(list(pares)) # [2, 4, 6, 8, 10]
# Filtrar números mayores que 5
mayores = filter(lambda x: x > 5, numeros)
print(list(mayores)) # [6, 7, 8, 9, 10]

# función reduce()
from functools import reduce

# Combinar elementos de una lista en un solo valor
numeros = [1, 2, 3, 4, 5]# Sumar todos los elementos
suma = reduce(lambda x, y: x + y, numeros)

print(suma) # 15

# Multiplicar todos los elementos
producto = reduce(lambda x, y: x * y, numeros)
print(producto) # 120

## Expresiones lambda
# Sintaxis básica de lambda
# lambda argumentos: expresión

# Ejemplos de expresiones lambda
sumar = lambda x, y: x + y
print(sumar(5, 3)) # Salida: 8

multiplicar = lambda x, y, z: x * y * z
print(multiplicar(2, 3, 4)) # Salida: 24

# Lambda con condicionales
# CAMBIO: Usamos 'es_par' como nombre de variable para que coincida con los print
es_par = lambda x: "Par" if x % 2 == 0 else "Impar"

print(es_par(4)) # Salida: Par
print(es_par(7)) # Salida: Impar

###Ejemplo completo de filter y reduce
from functools import reduce

# Lista de productos con precio y stock
productos = [
    {"nombre": "Laptop", "precio": 1200, "stock": 5},
    {"nombre": "Teléfono", "precio": 800, "stock": 10},
    {"nombre": "Tablet", "precio": 500, "stock": 0},
    {"nombre": "Monitor", "precio": 300, "stock": 8},
    {"nombre": "Teclado", "precio": 100, "stock": 15}
]
# Filtrar productos disponibles (stock > 0)
disponibles = filter(lambda p: p["stock"] > 0, productos)
# Calcular el valor total del inventario
valor_total = reduce(
    lambda acum, p: acum + (p["precio"] * p["stock"]),
    disponibles,
    0
)
print(f"Valor total del inventario: ${valor_total}")

##Combinación de funciones de orden superior

from functools import reduce

# Lista de números
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Filtrar números pares, elevarlos al cuadrado y sumarlos
resultado = reduce(
    lambda x, y: x + y,
    map(
        lambda x: x ** 2,
        filter(lambda x: x % 2 == 0, numeros)
    )
)

print(resultado)  # Salida: 220 (2² + 4² + 6² + 8² + 10² = 4 + 16 + 36 + 64 + 100)


## creación de módulos personalizados
## archivo mi_modulo.py

# Archivo main.py
import mi_modulo

print(mi_modulo.saludar("Ana"))
print(mi_modulo.PI)
