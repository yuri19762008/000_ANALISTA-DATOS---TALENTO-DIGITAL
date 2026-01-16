# --- DATOS INICIALES ---
nombres = ["Ana", "Juan", "Maria", "Pedro", "Luis"]
notas = [85, 42, 90, 55, 70]

# 4. Usar enumerate() para recorrer con índice
print("\n--- 4. Listado Numerado de Estudiantes ---")
for idx, nombre in enumerate(nombres, start=1):
    print(f"{idx}. Estudiante: {nombre}")