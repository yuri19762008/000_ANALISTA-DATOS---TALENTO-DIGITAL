# 1. Crear listas
nombres = ["Ana", "Luis", "María", "Pedro", "Sofía"]
notas = [7.5, 5.8, 10, 4.9, 6.3]

# 2. zip() para mostrar cada nombre con su nota
print("Listado de estudiantes:")
for nombre, nota in zip(nombres, notas):
    print(f"{nombre}: {nota}")

# 3. enumerate() para la posición de la nota más baja
pos_min = 0
nota_min = notas[0]
for i, nota in enumerate(notas):
    if nota < nota_min:
        nota_min = nota
        pos_min = i
print(f"\nNota más baja: {nota_min} (posición {pos_min}, estudiante {nombres[pos_min]})")

# 4. Comprensión con aprobados (nota >= 6)
aprobados = [nombre for nombre, nota in zip(nombres, notas) if nota >= 6]
print(f"\nEstudiantes aprobados: {aprobados}")

# 5. for + break para detectar nota perfecta (10)
hay_perfecta = False
for nota in notas:
    if nota == 10:
        hay_perfecta = True
        print("\nHay al menos una nota perfecta (10).")
        break
if not hay_perfecta:
    print("\nNo hay notas perfectas.")

# 6. Resumen
cantidad_aprobados = len(aprobados)
promedio_notas = sum(notas) / len(notas)
necesitan_rendir = [nombre.upper() for nombre, nota in zip(nombres, notas) if nota < 6]

print("\nResumen:")
print(f"- Cantidad de aprobados: {cantidad_aprobados}")
print(f"- Promedio de notas: {promedio_notas:.2f}")
print(f"- Estudiantes que necesitan rendir: {necesitan_rendir}")
