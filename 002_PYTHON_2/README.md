\# Infografía: Sentencias iterativas en Python

\## 1. ¿Qué son las sentencias iterativas?

Las \*\*sentencias iterativas\*\* permiten repetir un bloque de código varias veces, de forma automática, sin escribir las mismas instrucciones una y otra vez. \

Se usan especialmente cuando:

\- Trabajas con \*\*grandes cantidades de datos\*\*.

\- Necesitas aplicar la misma operación a una \*\*colección\*\* (lista, diccionario, etc.).

\- Quieres \*\*automatizar tareas repetitivas\*\* y evitar errores humanos. \

\*\*Ventajas principales:\*\*

\- Eficiencia: menos líneas, más trabajo automatizado. \

\- Mantenimiento: el código es más claro y fácil de modificar. \

\- Flexibilidad: se adapta a muchos escenarios distintos. \

\- Optimización: permite construir algoritmos más complejos de forma simple. \

\## 2. Herramientas de iteración en Python

Python ofrece tres pilares básicos para iterar: `while`, `for` y `range`. \

\- \*\*`while`\*\*: repite mientras una condición sea verdadera.

\- \*\*`for`\*\*: recorre elementos de una colección o secuencia.

\- \*\*`range`\*\*: genera secuencias numéricas para controlar iteraciones. \

Idea clave:

\- Usa `while` cuando depende de una \*\*condición lógica\*\*.

\- Usa `for` cuando repites sobre una \*\*colección\*\* o un \*\*rango conocido\*\* de valores. \

\## 3. Bucle `while`

\### 3.1. Concepto

`while` ejecuta un bloque de código \*\*mientras se cumpla una condición\*\*. \

\- Es útil cuando \*\*no sabes\*\* cuántas veces vas a repetir.

\- La repetición termina cuando la condición deja de ser verdadera. \

\### 3.2. Sintaxis básica

```python

while condicion:

&#x20;   # bloque de código

&#x20;   # actualizar variables de control

```

Ejemplo: contar hasta 5. \

```python

contador = 1

while contador <= 5:

&#x20;   print(contador)

&#x20;   contador += 1

```

Interpretación:

\- Partes en 1.

\- Mientras `contador <= 5`, imprimes y sumas 1.

\- Cuando llega a 6, la condición ya no se cumple y el bucle termina. \

\### 3.3. Bucles infinitos

Si \*\*no actualizas\*\* la variable de control, el bucle puede ser \*\*infinito\*\*. \

Ejemplo de error típico:

```python

contador = 1

while contador <= 5:

&#x20;   print(contador)

&#x20;   # falta contador += 1

```

\- La condición nunca cambia, el bucle nunca termina.

\- Por eso, siempre hay que revisar la \*\*condición de salida\*\*. \

\### 3.4. Usos típicos de `while`

\- Validar entrada de usuario hasta que sea correcta.

\- Monitorear un proceso hasta que cambie de estado.

\- Repetir una acción “hasta que pase algo”. \

Mini–ejemplo: pedir un número positivo.

```python

numero = int(input("Ingresa un número positivo: "))

while numero <= 0:

&#x20;   print("Debe ser positivo.")

&#x20;   numero = int(input("Ingresa un número positivo: "))

```

\## 4. Bucle `for`

\### 4.1. Concepto

`for` recorre los elementos de una \*\*colección\*\* (lista, tupla, diccionario, etc.) o una \*\*secuencia\*\*, uno por uno. \

\- Es ideal cuando conoces la \*\*cantidad de iteraciones\*\* o depende del tamaño de la colección. \

\### 4.2. Sintaxis básica

```python

for elemento in coleccion:

&#x20;   # usar elemento

```

Ejemplo con lista: \

```python

numeros =

for n in numeros:

&#x20;   print(n)

```

\### 4.3. Ventajas de `for` frente a `while`

\- No necesitas manejar manualmente la variable de control.

\- Es más legible.

\- Evita muchos bucles infinitos. \

\### 4.4. `for` con `range`

Permite crear una secuencia de enteros y recorrerlos con `for`. \

Formas típicas:

```python

\# solo fin (0 hasta fin-1)

for i in range(5):      # 0,1,2,3,4

&#x20;   print(i)



\# inicio, fin

for i in range(2, 6):   # 2,3,4,5

&#x20;   print(i)



\# inicio, fin, paso

for i in range(1, 10, 2):   # 1,3,5,7,9

&#x20;   print(i)

```

Usos:

\- Repetir una acción un número exacto de veces.

\- Trabajar por \*\*índice\*\* en listas. \

\## 5. Iterar listas

\### 5.1. Recorrer elementos

```python

frutas = \["manzana", "pera", "uva"]

for fruta in frutas:

&#x20;   print(fruta)

```

Interpretación:

\- En cada vuelta, `fruta` toma un valor de la lista.

\- Se usa para aplicar la misma operación a cada elemento. \

\### 5.2. Modificar con comprensión de listas

```python

frutas = \["manzana", "pera", "uva"]

frutas\_mayus = \[f.upper() for f in frutas]

```

Sintaxis general: \

```python

nueva\_lista = \[expresion for elemento in iterable if condicion\_opcional]

```

Ideas:

\- Menos código que un `for` clásico.

\- Muy útil para \*\*transformar\*\* datos. \

\## 6. Iterar diccionarios

Los diccionarios guardan \*\*pares clave–valor\*\*. \

```python

edades = {"Ana": 25, "Carlos": 30, "María": 22}

```

\### 6.1. Recorrer claves y valores con `items()`

```python

for nombre, edad in edades.items():

&#x20;   print(nombre, edad)

```

\### 6.2. Otros métodos

\- `keys()`: solo claves.

\- `values()`: solo valores. \

```python

for nombre in edades.keys():

&#x20;   print(nombre)



for edad in edades.values():

&#x20;   print(edad)

```

\### 6.3. Precaución al modificar

Modificar el diccionario \*\*mientras lo recorres\*\* puede dar errores. \

Patrón más seguro:

\- Crear un \*\*nuevo diccionario\*\* con comprensión de diccionario. \

```python

edades\_mayores = {nombre: edad for nombre, edad in edades.items() if edad >= 25}

```

\## 7. Control avanzado de bucles

\### 7.1. `break` y `continue`

\- `break`: rompe el bucle completamente. \

\- `continue`: salta al \*\*siguiente ciclo\*\*, sin ejecutar el resto del bloque. \

Ejemplo con `break`:

```python

for n in range(10):

&#x20;   if n == 5:

&#x20;       break

&#x20;   print(n)

```

Ejemplo con `continue`:

```python

for n in range(5):

&#x20;   if n == 2:

&#x20;       continue

&#x20;   print(n)

```

\### 7.2. Bucles anidados

Un bucle dentro de otro. \

```python

for i in range(3):

&#x20;   for j in range(2):

&#x20;       print(i, j)

```

\- Útiles para trabajar con estructuras 2D.

\- Cuidado con el rendimiento: crece muy rápido el número de iteraciones. \

\### 7.3. `enumerate` y `zip`

\- `enumerate(iterable)`: da \*\*índice\*\* y valor. \

```python

frutas = \["manzana", "pera", "uva"]

for indice, fruta in enumerate(frutas):

&#x20;   print(indice, fruta)

```

\- `zip(lista1, lista2, ...)`: recorre varias colecciones al mismo tiempo. \

```python

nombres = \["Ana", "Carlos", "María"]

notas =



for nombre, nota in zip(nombres, notas):

&#x20;   print(nombre, nota)

```

\## 8. Iteradores, generadores y comprensiones avanzadas

\### 8.1. Iteradores y generadores

\- Un \*\*iterador\*\* es un objeto que sabe devolver elementos uno a uno. \

\- Un \*\*generador\*\* es una función especial que usa `yield` y produce valores bajo demanda, sin guardar toda la secuencia en memoria. \

Mini–ejemplo:

```python

def generador\_pares(limite):

&#x20;   n = 0

&#x20;   while n <= limite:

&#x20;       yield n

&#x20;       n += 2



for numero in generador\_pares(10):

&#x20;   print(numero)

```

\### 8.2. Comprensiones avanzadas

No solo existen listas, también comprensiones de diccionarios y conjuntos. \

```python

\# diccionario: nombre -> nota aprobada

nombres = \["Ana", "Carlos", "María"]

notas =

aprobados = {n: nota for n, nota in zip(nombres, notas) if nota >= 6}

```

\## 9. Optimización y depuración de bucles

\### 9.1. Optimización de bucles

Buenas prácticas: \

\- Minimizar operaciones costosas dentro del bucle.

\- Usar funciones incorporadas (`map`, `filter`, `sum`, etc.) cuando tenga sentido.

\- Evitar bucles anidados innecesarios.

\- Preferir comprensiones cuando mejoran legibilidad. \

\### 9.2. Depuración de bucles

Técnicas útiles: \

\- Imprimir variables clave en algunas iteraciones.

\- Limitar el número de repeticiones durante las pruebas.

\- Revisar cuidadosamente la \*\*condición de salida\*\* (sobre todo en `while`). \

\## 10. Patrones comunes con bucles

Patrones que aparecen todo el tiempo: \

\- \*\*Acumulación\*\*: sumar o acumular resultados.

```python

total = 0

for n in numeros:

&#x20;   total += n

```

\- \*\*Filtrado\*\*: dejar solo los elementos que cumplen una condición.

```python

mayores = \[n for n in numeros if n > 10]

```

\- \*\*Búsqueda\*\*: encontrar un elemento que cumpla cierta condición (a menudo con `break`). \

\## 11. Ejercicio aplicado 1: recorriendo el inventario

\### 11.1. Contexto

Un almacén necesita revisar su inventario, detectar productos con \*\*stock bajo\*\* y generar una lista para reposición. \

\### 11.2. Consigna (resumida)

1\. Crear una lista de diccionarios con `nombre`, `stock`, `precio`.

2\. Usar `for` para recorrer los productos e imprimir los que tienen stock bajo.

3\. Construir con comprensión de lista la lista `reposicion`.

4\. Calcular total de productos en bajo stock y valor total.

5\. Usar un `while` para simular ingreso de productos hasta que el usuario escriba `"salir"`. \

\### 11.3. Idea algorítmica

\- Combina `for`, `while`, comprensiones, acumulación y validación de entrada.

\- Es un ejemplo típico de uso real de bucles en un sistema sencillo. \

\## 12. Ejercicio aplicado 2: análisis académico con bucles inteligentes

\### 12.1. Contexto

Una escuela quiere procesar datos de estudiantes: nombres, notas, aprobados, reprobados, promedios, etc. \

\### 12.2. Consigna (resumida)

1\. Crear listas `nombres` y `notas` con la misma cantidad de elementos.

2\. Usar `zip` para mostrar nombre y nota.

3\. Usar `enumerate` para encontrar la posición con nota más baja.

4\. Crear comprensión de lista con nombres de aprobados (nota ≥ 6).

5\. Con `for` y `break`, detectar si hay nota perfecta 10.

6\. Mostrar resumen:

&#x20; - cantidad de aprobados

&#x20; - promedio de notas

&#x20; - nombres en mayúsculas de estudiantes que deben rendir (nota < 6). \

\### 12.3. Herramientas que integra

\- `for`, `range`, `zip`, `enumerate`, `break`, comprensiones de listas. \

\- Patrón ideal para practicar lógica de negocio con bucles. \

\## 13. Conclusiones clave

\- `while` es ideal cuando la \*\*repetición depende de una condición\*\* que puede cambiar (usuario, sensores, estados). \

\- `for` es mejor cuando recorres \*\*colecciones o rangos controlados\*\*. \

\- Herramientas como `range`, comprensiones, `enumerate`, `zip`, `break`, `continue` permiten escribir bucles más claros, cortos y eficientes. \

\- Dominar estos patrones es fundamental para resolver problemas reales y escribir código limpio y mantenible en Python. \
