# 1. Crear un set con los nombres únicos (eliminar duplicados)
nombres_con_duplicados = ["Ana", "Carlos", "Elena", "Ana", "Luis", "Elena"]
nombres_unicos = set(nombres_con_duplicados)
print(f"Nombres únicos registrados: {nombres_unicos}")

# 2. Crear una estructura anidada (lista de diccionarios)
# Incluye nombre, edad, cursos (lista) y calificaciones (diccionario)
alumnos = [
    {
        "nombre": "Ana", 
        "edad": 25, 
        "cursos": ["Python", "SQL"], 
        "calificaciones": {"Python": 95, "SQL": 88}
    },
    {
        "nombre": "Carlos", 
        "edad": 19, 
        "cursos": ["Java"], 
        "calificaciones": {"Java": 80}
    },
    {
        "nombre": "Elena", 
        "edad": 30, 
        "cursos": ["Python", "C++"], 
        "calificaciones": {"Python": 92, "C++": 90}
    }
]

# 3. Utilizar comprensión de listas para obtener alumnos mayores a 22 años
mayores_de_22 = [a["nombre"] for a in alumnos if a["edad"] > 22]
print(f"\nAlumnos mayores de 22 años: {mayores_de_22}")

# 4. Utilizar comprensión de diccionarios para filtrar calificaciones > 90
# Lo haremos para un alumno específico (ej. Ana)
notas_excelentes_ana = {curso: nota for curso, nota in alumnos[0]["calificaciones"].items() if nota > 90}
print(f"Calificaciones excelentes de Ana (>90): {notas_excelentes_ana}")

# 5. Función con retorno múltiple (tupla) para promedio y cantidad de cursos
def analizar_alumno(alumno):
    notas = alumno["calificaciones"].values()
    promedio = sum(notas) / len(notas)
    cantidad_cursos = len(alumno["cursos"])
    return (promedio, cantidad_cursos)  # Retorno de tupla

# 6. Mostrar resultados con formato limpio
print("\n--- Reporte Académico ---")
for a in alumnos:
    # Desempaquetado de la tupla retornada por la función
    prom, cant = analizar_alumno(a)
    print(f"Alumno: {a['nombre']} | Cursos: {cant} | Promedio: {prom:.2f}")