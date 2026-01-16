# Ejemplo con FOR:
# Iterar sobre una lista de números e imprimir solo los pares
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print("Números pares en la lista:")
for numero in numeros:
    if numero % 2 == 0:
        print(numero)


# Sintaxis de While
# Inicialización de la variable de control
contador = 1

# Mientras la condición sea True, se ejecuta el bloque
while contador <= 5:
    print("Contador:", contador)  # Bloque de código a ejecutar
    contador += 1                 # Actualización de la variable de control

# Ejemplo de While: Contar hasta 5

contador = 1
while contador <= 5:    
    print("Número:", contador)    
    contador += 1        

# Sintaxis de For

coleccion = [1,2,3,4,5]

for elemento in coleccion:    
    # Bloque de código a ejecutar    
    # para cada elemento
    print(elemento)

# For con Range

for i in range(5):    
    print(i)  
    # Imprime 0, 1, 2, 3, 4

# Iterando Listas de Elementos
frutas = ["manzana", "banana", "cereza"]
for fruta in frutas:    
    print(fruta)

# Operaciones con Listas
frutas = ["manzana", "banana", "cereza"]
frutas_mayusculas = [fruta.upper() for fruta in frutas]
print(frutas_mayusculas)  # ["MANZANA", "BANANA", "CEREZA"]

# Sintaxis general
nueva_lista = [expresión for elemento in iterable if condición]

# Iterando con ítems()
edades = {"Ana": 25, "Carlos": 30, "María": 22}
for nombre, edad in edades.items(): 
    print(f"{nombre} tiene {edad} años")

# Iterando Claves y Valores
# Diccionario de ejemplo para que el código funcione
edades = {
    "Ana": 25,
    "Juan": 30,
    "Maria": 22
}

# Solo claves
for nombre in edades.keys():
    print("Nombre:", nombre)

# Solo valores
for edad in edades.values():
    print("Edad:", edad)    

# Modificando Diccionarios
# Método seguro usando comprensión de diccionario
edades = {"Ana": 25, "Carlos": 30, "María": 22}
edades_en_meses = {nombre: edad * 12 for nombre, edad in edades.items()}

######### PARTE 2 ###########
# Uso Básico de Range
for i in range(5):    
    print(i)# Imprime: 0, 1, 2, 3, 4


# range(stop) → [0, 1, 2, ..., stop-1]
# range(start, stop) → [start, start+1, ..., stop-1]
# range(start, stop, step) → [start, start+step, ..., stop-1]


# Range con punto de inicio y fin
for i in range(2,6):
    print("Número:",i)


# Range con incremento personalizado
for i in range(1, 10, 2):
    print("Número:",i)

for i in range(1, 10, 2):    
    print(i)# Imprime: 1, 3, 5, 7, 9


# Iterando por índice
numeros = [10, 20, 30, 40, 50]
for i in range(len(numeros)):    
    numeros[i] += 5
    print(numeros)# [15, 25, 35, 45, 55]

# Repetición controlada
for _ in range(3):
    print("esta es una repetición controlada")

for _ in range(3):
     print("Esta acción se repite tres veces")

# Ejemplos avanzados con Range
# Iteración inversa
for i in range(10, 0, -1):    
    print(i)  # Cuenta regresiva: 10, 9, 8, ..., 1
    # Acceso a elementos alternos

numeros = [10, 20, 30, 40, 50, 60]
for i in range(0, len(numeros), 2):    
    print(numeros[i])  # Imprime: 10, 30, 50     

# Combinando While y For
# Buscar un elemento en una lista con límite de intentos
numeros = [10, 20, 30, 40, 50]
buscar = 30
intentos = 0
encontrado = False
while intentos < 3 and not encontrado: 
    for num in numeros: 
        if num == buscar: 
            encontrado = True 
            print(f"¡Encontrado {buscar}!") 
            break 
    intentos += 1

# Sentencias de control en bucles
for i in range(10):    
    if i == 5:        
        break    
    print(i)  # Imprime: 0, 1, 2, 3, 4
   

for i in range(10): 
    if i % 2 == 0: 
        continue 
    print(i) # Imprime: 1, 3, 5, 7, 9


# Bucles anidados
# Imprimir una tabla de multiplicación
for i in range(1, 5):    
    for j in range(1, 5):        
        print(f"{i} x {j} = {i*j}")   
        print("-----")



# Comprensiones avanzadas
# Comprensión de lista
cuadrados = [x**2 for x in range(10)]
# Comprensión de diccionario
cuadrados_dict = {x: x**2 for x in range(10)}
# Comprensión de conjunto
cuadrados_set = {x**2 for x in range(10)}

# Iteración con enumerate
frutas = ["manzana", "banana", "cereza"]
for indice, fruta in enumerate(frutas):    
    print(f"Índice {indice}: {fruta}")# Índice 0: manzana# Índice 1: banana# Índice 2: cereza


# Iteración con Zip
nombres = ["Ana", "Carlos", "María"]
edades = [25, 30, 22]
for nombre, edad in zip(nombres, edades):    
    print(f"{nombre} tiene {edad} años")# Ana tiene 25 años# Carlos tiene 30 años# María tiene 22 años  


# Iteradores y generadores
# Generador simple
def contar_hasta(n): 
    i = 1 
    while i <= n: 
        yield i 
        i += 1
# Uso del generador
for num in contar_hasta(5): 
    print(num)
   
###
def contar_hasta(n):
    resultado = [] # Creamos una lista para guardar los números
    i = 1
    while i <= n:
        resultado.append(i) # En lugar de yield, guardamos el número en la lista
        i += 1
    return resultado # Entregamos la lista completa al final

for num in contar_hasta(6): 
    print(num)



# Patrones comunos con Bucles
# Acumulación
numeros = [1,2,3]
suma = 0
for num in numeros:    
    suma += num


# filtrado
numeros = [1,2,3]
pares = []
for num in numeros:    
    if num % 2 == 0:   
     pares.append(num)

print(pares)

# Busqueda
lista = [1,2,3]
objetivo = 2
for elemento in lista: 
    if elemento == objetivo: 
        print("¡Encontrado!") 
        break

# Bucles en programación funcional
# Enfoque imperativo con bucle
cuadrados = []
for x in range(10): 
    cuadrados.append(x**2) 
    
# Enfoque funcional
cuadrados = list(map(lambda x: x**2, range(10)))

# Filtrado imperativo
pares = []
for x in range(10): 
    if x % 2 == 0: 
        pares.append(x)
        
# Filtrado funcional
pares = list(filter(lambda x: x % 2 == 0, range(10)))

# Iteración asíncrona
import asyncio

# Definimos una función asíncrona 
async def procesar_elemento(elemento):
    # 'await' pausa esta función sin bloquear al resto del programa
    await asyncio.sleep(1)  # Simula una operación que tarda (como una descarga)
    return elemento * 2

async def main():
    # Creamos una lista de tareas 
    tareas = [procesar_elemento(i) for i in range(5)]
    
    # 'gather' ejecuta todas las tareas en paralelo y espera a que terminen
    resultados = await asyncio.gather(*tareas)
    
    print(resultados)

# Punto de entrada para ejecutar la corrutina principal
asyncio.run(main())

