# 1. Usar un while para repetir hasta que se ingrese una opción válida
while True:
    acceso = input("¿Desea iniciar el sistema de control académico? (si/no): ").lower()
    if acceso == "si":
        print("Iniciando sistema...")
        break
    elif acceso == "no":
        print("Saliendo del programa.")
        exit()
    else:
        print("Opción no válida. Por favor, escriba 'si' o 'no'.")

# 2. Crear una lista de productos/materias y recorrerla con for
materias = ["Matemáticas", "Programación", "Base de Datos", "Sistemas"]
print("\nMaterias a procesar:")
for materia in materias:
    print(f"- {materia}")

# 3. Generar una secuencia numérica con range()
print("\nGenerando registros de asistencia para los primeros 3 días:")
for dia in range(1, 4):
    print(f"Día {dia}: Registro completado.")

# 4. Usar for con items() para mostrar contenido de un diccionario

edades = {"Ana": 25, "Juan": 30, "Maria": 22}
for nombre, edad in edades.items():
    print(f"{nombre} tiene {edad} años")

# 5. Construir una nueva lista con list comprehension
nombres = ["Ana", "Juan", "Maria", "Pedro"]
notas = [8.5, 4.0, 10.0, 5.5]

aprobados = [nombres[i] for i in range(len(nombres)) if notas[i] >= 6]

print(aprobados) 


# 6. Filtrar elementos de un diccionario con comprensión de diccionario
# Diccionario original
estudiantes_notas = {
    "Ana": 8.5, 
    "Juan": 4.0, 
    "Maria": 10.0, 
    "Pedro": 5.5,
    "Luis": 7.0
}

# Filtrar con comprensión de diccionario (Punto 7 de tu guía)
destacados = {nombre: nota for nombre, nota in estudiantes_notas.items() if nota > 8}

print(destacados)
# Resultado: {'Ana': 8.5, 'Maria': 10.0}
