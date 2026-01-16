# 1. Crear una lista llamada alumnos con diccionarios iniciales
# Cada diccionario tiene las claves: "nombre", "curso", "nota"
alumnos = [
    {"nombre": "Ana", "curso": "Python", "nota": 95},
    {"nombre": "Carlos", "curso": "Java", "nota": 80},
    {"nombre": "Elena", "curso": "Python", "nota": 88}
]

# 2. Usar un bucle for para mostrar todos los nombres de los alumnos registrados
print("Alumnos registrados inicialmente:")
for alumno in alumnos:
    print(f"- {alumno['nombre']}")

# 3. Agregar un nuevo alumno al final de la lista utilizando el método append()
nuevo_alumno = {"nombre": "Luis", "curso": "C++", "nota": 75}
alumnos.append(nuevo_alumno)

# 4. Modificar la nota del segundo alumno de la lista, accediendo por índice
# El segundo alumno está en el índice 1
alumnos[1]["nota"] = 85

# 5. Calcular y mostrar el promedio general de las notas
total_notas = 0
for alumno in alumnos:
    total_notas += alumno["nota"]

promedio = total_notas / len(alumnos)
print(f"\nEl promedio general de las notas es: {promedio}")

# 6. Ordenar la lista por nota de forma descendente (sort + lambda)
# Usamos reverse=True para que sea de mayor a menor
alumnos.sort(key=lambda alumno: alumno["nota"], reverse=True)

# Mostrar resultado final ordenado
print("\nLista de alumnos ordenada por nota (descendente):")
for alumno in alumnos:
    print(f"Nombre: {alumno['nombre']}, Nota: {alumno['nota']}")