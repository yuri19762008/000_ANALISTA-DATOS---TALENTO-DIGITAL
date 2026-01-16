# --- DATOS INICIALES ---
nombres = ["Ana", "Juan", "Maria", "Pedro", "Luis"]
notas_finales = [85, 42, 90, 55, 70]  # 0-100
evaluaciones = [
    [80, 90, 85],   # Ana
    [40, 45, 41],   # Juan
    [95, 88, 92],   # Maria
    [50, 60, 55],   # Pedro
    [70, 72, 68],   # Luis
]

# Variables globales
APROBACION = 60
NOTA_CRITICA = 30
DEBUG = True

# 1) range(start, stop, step) para generar secuencias
for paso in range(0, 10, 2):  # 0,2,4,6,8
    print(f"Paso de auditoría: {paso}")

# 2) Combinar listas con zip()
registros = []
for nombre, nota_final, notas_eval in zip(nombres, notas_finales, evaluaciones):
    registros.append({
        "nombre": nombre,
        "nota_final": nota_final,
        "evaluaciones": notas_eval
    })

if DEBUG:
    print("Registros:", registros)

# 3) Comprensiones: crear listas y diccionarios
# Diccionario nombre -> nota_final
estudiantes_dict = {r["nombre"]: r["nota_final"] for r in registros}
print("Diccionario nombre->nota_final:", estudiantes_dict)

# Lista de aprobados (por nota final)
aprobados_lista = [r["nombre"] for r in registros if r["nota_final"] >= APROBACION]
print("Aprobados (lista):", aprobados_lista)

# 4) enumerate() para recorrer con índice
for idx, r in enumerate(registros, start=1):
    print(f"{idx}. {r['nombre']} (nota final: {r['nota_final']})")


# 5) break y continue dentro de un análisis de notas + Bucles anidados (evaluaciones por estudiante)
for r in registros:
    nombre = r["nombre"]
    notas_eval = r["evaluaciones"]

    # continue: si faltan evaluaciones, se omite (caso realista)
    if not notas_eval:
        if DEBUG:
            print(f"[DEBUG] {nombre} no tiene evaluaciones -> se omite.")
        continue

    # bucle anidado: revisar cada evaluación
    tiene_critica = False
    for nota in notas_eval:
        # break: si aparece una nota crítica, detenemos revisión de ese estudiante
        if nota < NOTA_CRITICA:
            print(f"ALERTA: {nombre} tiene nota crítica ({nota}). Se corta revisión de sus evaluaciones.")
            tiene_critica = True
            break

    if tiene_critica:
        continue  # pasamos al siguiente estudiante

    if DEBUG and (APROBACION - 5) <= r["nota_final"] <= (APROBACION + 5):
        print(f"[DEBUG] {nombre} está cerca del corte: nota_final={r['nota_final']} evaluaciones={notas_eval}")

    print(f"{nombre}: revisión de evaluaciones OK.")

# 6) Generador con yield para listar alumnos aprobados
def generador_aprobados(registros, corte=60):
    for r in registros:
        if r["nota_final"] >= corte:
            yield r  # devuelve el registro completo

# 7) Depuración con impresión selectiva y condiciones
for r in generador_aprobados(registros, APROBACION):
    nombre = r["nombre"]
    nota_final = r["nota_final"]

    # depuración selectiva: destacados
    if nota_final >= 80:
        print(f"[DESTACADO] {nombre} tiene excelente nota final: {nota_final}")

    # continue: ejemplo “regla de negocio” / caso especial (privacidad)
    if nombre == "Maria":
        print("(Saltando detalle de Maria por privacidad)")
        continue

    print(f"Procesando informe para: {nombre} | nota final: {nota_final}")

    # break: ejemplo de límite de revisión (si quieres cortar al llegar a un nombre)
    if nombre == "Luis":
        print("Se alcanzó el límite de revisión. Finalizando.")
        break
