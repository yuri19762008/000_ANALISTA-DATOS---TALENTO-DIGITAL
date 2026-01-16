# 1. Crear una lista de diccionarios (Alumnos)
alumnos = [
    {"nombre": "Ana", "curso": "Python", "nota": 95},
    {"nombre": "Carlos", "curso": "Java", "nota": 80},
    {"nombre": "Elena", "curso": "Python", "nota": 88}
]

# 2. Agregar un nuevo alumno con append()
alumnos.append({"nombre": "Luis", "curso": "C++", "nota": 75})

# 3. Modificar una nota accediendo a un diccionario por índice
# Cambiaremos la nota del segundo alumno (Carlos, índice 1)
alumnos[1]["nota"] = 85

# 5. Obtener estadísticas del grupo (Promedio)
# Sumamos todas las notas y dividimos por el total de alumnos
total_notas = 0
cantidad_alumnos = len(alumnos)

for alumno in alumnos:
    nota = alumno["nota"]
    total_notas += nota

promedio = total_notas / cantidad_alumnos
print(f"Promedio del grupo: {promedio}")

# Alternativa usando un bucle 'for' directamente
total_notas = 0

for alumno in alumnos:
    total_notas = total_notas + alumno["nota"]

promedio = total_notas / len(alumnos)
print("Promedio del grupo:", promedio)

"""total_notas = sum(alumno["nota"] for alumno in alumnos)
promedio = total_notas / len(alumnos)
print(f"Promedio del grupo: {promedio}")"""

# 6. Mostrar todos los nombres usando 'for' y acceso por clave
print("Lista de alumnos:")
for alumno in alumnos:
    print(f"- {alumno['nombre']}")

# 7. Ordenar los alumnos por nota con sort() y una función lambda
# Usamos reverse=True para que el mayor puntaje aparezca primero

def obtener_nota(alumno):
    return alumno["nota"]

alumnos.sort(key=obtener_nota, reverse=True)


alumnos.sort(key=lambda x: x["nota"], reverse=True)

print("\nAlumnos ordenados por nota (Mayor a Menor):")
print(alumnos)