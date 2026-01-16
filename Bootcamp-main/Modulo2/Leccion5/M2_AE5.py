# Crear una lista

mi_lista = [10, 20, 30, "Hola", True]
print(mi_lista)  # Salida: [10, 20, 30, 'Hola', True]

# agregar y modificar elementos en una lista
mi_lista = [1, 2, 3]
mi_lista.append(4)          # Agregar elemento al final
mi_lista.insert(1, 1.5)     # Insertar elemento en posición específica
mi_lista[2] = 2.5           # Modificar elemento en posición específica
print(mi_lista)  # Salida: [1, 1.5, 2.5, 3, 4]

# Rescatar un elemento y rango de elementos
mi_lista = [ 1, 2, 3, 4, 5 ]
print(mi_lista[2])    # Salida: 3
print(mi_lista[1:4])  # Salida: [2, 3, 4]

# Listas Anidadas y Matrices
matriz = [[1,2], [3,4], [5,6]]
print(matriz[1][0])  # Salida: 3

# Operaciones comunes con Listas
mi_lista = [5, 2, 9, 1, 5,
            3, 8, 4, 7, 6]
print(mi_lista)  # Salida: [5, 2, 9, 1, 5, 3, 8, 4, 7, 6]
mi_lista.sort()  # Ordenar la lista
print(mi_lista)  # Salida: [1, 2, 3, 4, 5, 5, 6, 7, 8, 9]
mi_lista.reverse()  # Invertir el orden de la lista
print(mi_lista)  # Salida: [9, 8, 7, 6, 5, 5, 4, 3, 2, 1]
print(len(mi_lista))  # Salida: 10  

remove_element = mi_lista.pop()  # Eliminar y retornar el último elemento
print(remove_element)  # Salida: 1
print(mi_lista)  # Salida: [9, 8, 7, 6, 5, 5, 4, 3, 2]

# Encontrar el índice de un elemento
index_of_5 = mi_lista.index(5)
print(index_of_5)  # Salida: 4


#combinar listas
lista_a = [1, 2, 3]
lista_b = [4, 5, 6]
lista_combinada = lista_a + lista_b
print(lista_combinada)  # Salida: [1, 2, 3, 4, 5, 6]




# crear diccionario
mi_diccionario = {
    "nombre": "Ana", 
    "edad": 25, 
    "ciudad": "Lima"}

print(mi_diccionario)  # Salida: {'nombre': 'Ana', 'edad': 25, 'ciudad': 'Lima'}

# Agregar y Modificar elementos en un Diccionario
mi_diccionario["profesion"] = "Ingeniera"
mi_diccionario["edad"] = 26
print(mi_diccionario)  # Salida: {'nombre': 'Ana', 'edad': 26, 'ciudad': 'Lima', 'profesion': 'Ingeniera'}

# Rescatar Elementos en un Diccionario
print(mi_diccionario["nombre"])  # Salida: Ana
print(mi_diccionario.get("pais", "No especificado"))  # Salida: No especificado

## Diccionarios Anidados

empleado = {
    "nombre": "Carlos",
    "datos_personales": {
        "edad": 35,
        "ciudad": "Bogotá"
    },
    "salario": 5000
}

print(empleado["datos_personales"]["ciudad"])  # Salida: Bogotá

# Obtener todas las claves
print(mi_diccionario.keys())  # Salida: dict_keys(['nombre', 'edad', 'ciudad', 'profesion'])
# Obtener todos los valores
print(mi_diccionario.values())  # Salida: dict_values(['Ana', 26, 'Lima', 'Ingeniera'])
# Obtener pares clave-valor
print(mi_diccionario.items())  # Salida: dict_items([('nombre', 'Ana'), ('edad', 26), ('ciudad', 'Lima'), ('profesion', 'Ingeniera')])
# Eliminar un elemento
edad = mi_diccionario.pop("edad")
print(edad)  # Salida: 26
print(mi_diccionario)  # Salida: {'nombre': 'Ana', 'ciudad': 'Lima', 'profesion': 'Ingeniera'}
#popitems
clave, valor = mi_diccionario.popitem()
print(f"Clave: {clave}, Valor: {valor}")  # Salida: Clave: profesion, Valor: Ingeniera
print(mi_diccionario)  # Salida: {'nombre': 'Ana', 'ciudad': 'Lima'}





##### PARTE 2 ######
# Creación de una Tupla
mi_tupla = (10, 20, "Python")
mi_tupla_sin_parentesis = 1, 2, 3

print(mi_tupla)  # Salida: (10, 20, 'Python')
print(mi_tupla_sin_parentesis)  # Salida: (1, 2, 3)

# Acceso a Elementos en una Tupla
print(mi_tupla[0])  # Salida: 10
print(mi_tupla_sin_parentesis[2])  # Salida: 3

# Empaquetado y Desempaquetado de Tuplas
coordenadas = (4,5)
x, y = coordenadas
print(f"x: {x}, y: {y}")  # Salida: x: 4, y: 5

# operaciones con Tuplas
tupla_a = (1, 2, 3)
tupla_b = (4, 5, 6)
tupla_concatenada = tupla_a + tupla_b
print(tupla_concatenada)  # Salida: (1, 2, 3, 4, 5, 6)

# repeticion de tuplas
tupla_repetida = tupla_a * 2
print(tupla_repetida)  # Salida: (1, 2, 3, 1, 2, 3)

# slicing en tuplas
print(tupla_concatenada[2:5])  # Salida: (3, 4, 5)

# conversión entre tuplas y listas  
tupla_a = (1, 2, 3)
lista_desde_tupla = list(tupla_a)
print(lista_desde_tupla)  # Salida: [1, 2, 3]

tupla_desde_lista = tuple(lista_desde_tupla)
print(tupla_desde_lista)  # Salida: (1, 2, 3)




# Creación de un set (Conjunto)
mi_set = {1, 2, 3, 4, 4, 5}
print(mi_set)  # Salida: {1, 2, 3, 4, 5}

# Agregar y Eliminar Elementos en un Set
mi_set.add(6)
mi_set.discard(3)
mi_set.remove(2)
print(mi_set)  # Salida: {1, 3, 4, 5, 6}

# Operaciones de Conjunto con Sets
set_a = {1, 2, 3}
set_b = {3, 4, 5}

print(set_a.union(set_b))        # Salida: {1, 2, 3, 4, 5}
print(set_a.intersection(set_b)) # Salida: {3}
print(set_a.difference(set_b))   # Salida: {1, 2}


# Eliminación de Elementos Duplicados
lista = [1, 2, 2, 3, 4, 4, 5]
mi_set = set(lista)
lista_sin_duplicados = list(mi_set)
print(lista_sin_duplicados)  # Salida: [1, 2, 3, 4, 5]

# Operaciones adicionales con Sets
# diferencia simétrica
set_c = {1, 2, 3, 4}
set_d = {3, 4, 5, 6}
diferencia_simetrica = set_c.symmetric_difference(set_d)
print(diferencia_simetrica)  # Salida: {1, 2, 5, 6}

# subconjuntos y superconjuntos
set_e = {1, 2}
set_f = {1, 2, 3, 4}
print(set_e.issubset(set_f))  # Salida: True
print(set_f.issuperset(set_e))  # Salida: True  

# conjuntos disjuntos
set_g = {1, 2}
set_h = {3, 4}  
print(set_g.isdisjoint(set_h))  # Salida: True


# Compresión de Listas
numeros = [1, 2, 2, 3, 4, 4, 5]
cuadrados = [x**2 for x in numeros]
print(cuadrados)  # Salida: {1, 4, 9, 16, 25}

# Compresión de Diccionarios
diccionario = {x: x**2 for x in range(5)}
print(diccionario)  # Salida: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Ejemplos de compresión de diccionarios
# 1. Crear un diccionario de cuadrados
cuadrados = {x: x**2 for x in range(10)}
print("Diccionario de cuadrados:", cuadrados)

# 2. Filtrar solo los valores pares de un diccionario original
original = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
pares = {k: v for k, v in original.items() if v % 2 == 0}
print("Diccionario con valores pares:", pares)

# 3. Convertir los valores de un diccionario a mayúsculas
nombres = {'id1': 'ana', 'id2': 'luis', 'id3': 'maría'}
mayusculas = {k: v.upper() for k, v in nombres.items()}
print("Diccionario con valores en mayúsculas:", mayusculas)



# comprensión de Sets
set_comp = {x for x in range(10) if x % 2 == 0}
print("Set de cuadrados:", set_comp)

# Ejemplos de compresión de sets
# 1. Crear un set de cuadrados del 0 al 9
cuadrados = {x**2 for x in range(10)}
print("Set de cuadrados:", cuadrados)

# 2. Filtrar valores pares de una colección
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
pares = {x for x in numeros if x % 2 == 0}
print("Set de números pares:", pares)

# 3. Extraer primeras letras de una lista de palabras
palabras = ["Hola", "Python", "Set", "Compresión"]
primeras_letras = {palabra[0] for palabra in palabras}
print("Primeras letras:", primeras_letras)

# Ejemplo de estructura mixta
# Estructura de datos para un sistema de gestión de estudiantes

estudiantes = [
    {
        "nombre": "Ana",
        "edad": 22,
        "cursos": ["Python", "Estadística", "Machine Learning"],
        "calificaciones": {
            "Python": 95,
            "Estadística": 88,
            "Machine Learning": 92
        }
    },
    {
        "nombre": "Carlos",
        "edad": 24,
        "cursos": ["Python", "Bases de Datos", "Web"],
        "calificaciones": {
            "Python": 85,
            "Bases de Datos": 90,
            "Web": 78
        }
    }
]

# Ejemplo de acceso a datos
print("Nombre del primer estudiante:", estudiantes[0]["nombre"])
print("Nota de Carlos en Web:", estudiantes[1]["calificaciones"]["Web"])
print("Cursos de Ana:", estudiantes[0]["cursos"])
print("Edad de Carlos:", estudiantes[1]["edad"])
print("Calificaciones de Ana:", estudiantes[0]["calificaciones"])
print("Estudiantes:", estudiantes)




