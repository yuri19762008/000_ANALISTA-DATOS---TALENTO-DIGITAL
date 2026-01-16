# 1. Crear dos listas: nombres y notas
nombres = ["Ana", "Juan", "Maria", "Pedro", "Luis", "Elena"]
notas = [8.5, 4.0, 10.0, 5.5, 7.0, 3.5]

# 2. Usar zip() para recorrer ambas listas y mostrar nombre con nota
print("--- Listado de Estudiantes y Calificaciones ---")
for nombre, nota in zip(nombres, notas):
    print(f"Estudiante: {nombre} | Nota: {nota}")

# 3. Usar enumerate() para identificar la posición de la nota más baja
nota_minima = notas[0]
posicion_minima = 0

for i, nota in enumerate(notas):
    if nota < nota_minima:
        nota_minima = nota
        posicion_minima = i

print(f"\nLa nota más baja es {nota_minima} (estudiante en posición {posicion_minima}: {nombres[posicion_minima]})")

# 4. Crear una comprensión de lista con nombres de aprobados (nota >= 6)
aprobados = [nombre for nombre, nota in zip(nombres, notas) if nota >= 6]

# 5. Usar for + break para detectar si hay una nota perfecta (10)
print("\nBuscando excelencia académica...")
for nombre, nota in zip(nombres, notas):
    if nota == 10:
        print(f"¡Se ha detectado una nota perfecta! Felicitaciones a {nombre}.")
        break  # Cortamos el bucle al encontrar la primera nota 10

# 6. Mostrar resumen final
print("\n--- RESUMEN DEL CURSO ---")

# Cantidad de aprobados
print(f"Cantidad de aprobados: {len(aprobados)}")

# Promedio de notas
promedio = sum(notas) / len(notas)
print(f"Promedio general del grupo: {promedio:.2f}")

# Nombres en mayúsculas de los que necesitan rendir (nota < 6) usando comprensión
necesitan_rendir = [n.upper() for n, nota in zip(nombres, notas) if nota < 6]
print(f"Estudiantes que deben rendir examen (en mayúsculas): {necesitan_rendir}")