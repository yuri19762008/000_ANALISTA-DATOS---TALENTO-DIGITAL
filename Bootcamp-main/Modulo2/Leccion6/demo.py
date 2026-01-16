nombres = ["Ana", "Juan", "Maria", "Pedro", "Luis"]
notas_finales = [85, 62, 90, 55, 70]
registros = []
for nombre, nota_final in zip(nombres,notas_finales):
    registros.append({
        "nombre":nombre,
        "nota_final":nota_final
    })
#print(registros)

estudiantes_dict = {r["nombre"]:r["nota_final"] for r in registros}

#print(estudiantes_dict)

aprobados = [r["nombre"] for r in registros if r["nota_final"]>=60]
#print(aprobados)


"""for r in registros:
    nombre = r["nombre"]
    nota = r["nota_final"]
    print(f" {nombre} , {nota}")
    if nota < 60:
        print("Nota baja")
        break
    if nota >= 90:
        print("Nota alta")
        continue"""

def generador_aprobados(registros):
    for r in registros:
        print(r)
        if r["nota_final"] >= 60:
            yield r

for r in generador_aprobados(registros):
    nombre = r["nombre"]
    nota_final = r["nota_final"]

    if nota_final >= 90:
        print(f"Nota alta {nota_final} para {nombre}")

    if nota_final < 60:
        print(f"Nota baja {nota_final} para {nombre}")

