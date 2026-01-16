# 1) Solicitar edad y categoría
edad_txt = input("Ingrese su edad: ")
categoria = input("Ingrese su categoría (estudiante/docente/visitante): ")

print("\n--- Resultado ---")
print(f"Edad ingresada: {edad_txt}")
print(f"Categoría ingresada: {categoria}")

# 4) Validaciones adicionales (entrada inválida)
if not edad_txt.isdigit():
    print("❌ Edad inválida. Debes ingresar un número entero (ej: 20).")
    raise SystemExit

edad = int(edad_txt) if edad_txt.isdigit() else 0

# 2) Evaluar múltiples condiciones usando if-elif-else (clasificación por edad)
if edad <= 12:
    grupo = "niño/a"
elif edad <= 17:
    grupo = "adolescente"
elif edad <= 59:
    grupo = "adulto/a"
else:
    grupo = "adulto/a mayor"

# Reglas del beneficio (puedes ajustarlas si tu profe definió otras)
if categoria == "estudiante":
    acceso_beneficio = edad >= 18
elif categoria == "docente":
    acceso_beneficio = edad >= 21
else:  # visitante
    acceso_beneficio = False

# 3) Expresión ternaria para mensaje resumen
#resumen = "✅ Accede al beneficio" if acceso_beneficio else "⛔ No accede al beneficio"

if acceso_beneficio:
    resumen = "✅ Accede al beneficio"
else:
    resumen = "⛔ No accede al beneficio"

print("\n--- Resultado ---")
print(f"Edad: {edad}")
print(f"Categoría: {categoria}")
print(f"Clasificación: {grupo}")
print(resumen)