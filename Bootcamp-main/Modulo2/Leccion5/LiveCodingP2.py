# 1. Crear tuplas para coordenadas y retorno múltiple
# Tuplas: coordenadas (inmutables)
santiago = (-33.4489, -70.6693)   # (lat, lon)
valparaiso = (-33.0472, -71.6127)

print("Coordenadas Santiago:", santiago)
print("Latitud de Santiago:", santiago[0])  # acceso por índice


# Tuplas: retorno múltiple
def resumen_notas(notas):
    promedio = sum(notas) / len(notas)
    maximo = max(notas)
    minimo = min(notas)
    return promedio, maximo, minimo   # retorna una tupla

prom, maxi, mini = resumen_notas([60, 70, 90, 80])
print("Promedio:", prom, "| Máxima:", maxi, "| Mínima:", mini)

# =========================================
# 2) Sets: únicos y diferencias
# =========================================
lista_a = ["Ana", "Luis", "Ana", "Sofía", "Pedro"]
lista_b = ["Luis", "Camila", "Pedro", "Pedro"]

unicos_a = set(lista_a)
unicos_b = set(lista_b)

print("\nNombres únicos en A:", unicos_a)
print("Nombres únicos en B:", unicos_b)

# Diferencias entre listas (quién está en A pero no en B)
solo_en_a = unicos_a - unicos_b
solo_en_b = unicos_b - unicos_a
comunes = unicos_a & unicos_b

print("Solo en A:", solo_en_a)
print("Solo en B:", solo_en_b)
print("Comunes:", comunes)


# =========================================
# 3) Comprensión de lista: filtrar datos
# =========================================
datos = [1, 3, 6, 2, 9, 10, 4]
mayores_a_5 = [x for x in datos if x > 5]

print("\nDatos:", datos)
print("Mayores a 5:", mayores_a_5)


# =========================================
# 4) Comprensión de diccionario: filtrar por valor
# =========================================
notas_por_alumno = {
    "Ana": 92,
    "Luis": 75,
    "Sofía": 88,
    "Pedro": 95,
    "Camila": 60
}

solo_sobre_90 = {nombre: nota for nombre, nota in notas_por_alumno.items() if nota > 90}

print("\nNotas:", notas_por_alumno)
print("Solo notas > 90:", solo_sobre_90)

# =========================================
# 5) Estructura anidada: alumnos con cursos y calificaciones
# =========================================
alumnos = [
    {
        "nombre": "Ana",
        "edad": 23,
        "cursos": ["Python", "SQL", "Power BI"],
        "calificaciones": {"Python": 92, "SQL": 85, "Power BI": 90}
    },
    {
        "nombre": "Luis",
        "edad": 21,
        "cursos": ["Python", "Excel"],
        "calificaciones": {"Python": 75, "Excel": 88}
    },
    {
        "nombre": "Sofía",
        "edad": 25,
        "cursos": ["Python", "Estadística"],
        "calificaciones": {"Python": 88, "Estadística": 91}
    }
]

# Mostrar nombres
print("\nNombres de alumnos:")
for alumno in alumnos:
    print("-", alumno["nombre"])

# Filtrar alumnos mayores a 22 (comprensión)
mayores_22 = [a["nombre"] for a in alumnos if a["edad"] > 22]
print("Mayores de 22:", mayores_22)

# Filtrar calificaciones > 90 de un alumno (comprensión de diccionario)
calif_ana = alumnos[0]["calificaciones"]
altas_ana = {curso: nota for curso, nota in calif_ana.items() if nota > 90}
print("Calificaciones > 90 de Ana:", altas_ana)

