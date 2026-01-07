# Sistema de Clasificación por Edad y Rol

print("=== Sistema de Clasificación por Edad y Rol ===\n")

# Paso 1: Solicitar edad al usuario
edad_input = input("Ingrese su edad: ")

if edad_input.isdigit():
    edad = int(edad_input)
    if edad < 0:
        print("Edad no válida. Terminando programa.")
    else:
        # Paso 2: Solicitar rol o categoría
        print("\nSeleccione su rol o categoría:")
        print("1. Estudiante")
        print("2. Docente")
        print("3. Visitante")
        
        opcion_input = input("\nIngrese el número de su rol (1-3): ")
        
        if opcion_input.isdigit():
            opcion_rol = int(opcion_input)
            if opcion_rol == 1:
                rol = "estudiante"
            elif opcion_rol == 2:
                rol = "docente"
            elif opcion_rol == 3:
                rol = "visitante"
            else:
                print("Opción no válida. Terminando programa.")
                rol = None
            
            if opcion_rol >= 1 and opcion_rol <= 3:
                # Paso 3: Clasificar edad
                if edad < 13:
                    categoria_edad = "Infancia"
                elif edad >= 13 and edad <= 17:
                    categoria_edad = "Adolescencia"
                elif edad >= 18 and edad <= 64:
                    categoria_edad = "Adultez"
                else:
                    categoria_edad = "Persona mayor"
                
                # Paso 4 y 5: Evaluar combinación de rol y edad para habilitar acceso o no a un beneficio
                if rol == "estudiante":
                    if edad < 25:
                        acceso = "SÍ"
                        motivo = "Estudiante menor de 25 años"
                    else:
                        acceso = "NO"
                        motivo = "Estudiante mayor de 25 años no califica"
                elif rol == "docente":
                    acceso = "SÍ"
                    motivo = "Docente tiene acceso completo"
                elif rol == "visitante":
                    acceso = "NO"
                    motivo = "Visitantes no tienen acceso al beneficio"
                else:
                    acceso = "NO"
                    motivo = "Rol no reconocido"
                
                # Paso 6: Imprimir resumen final de edad, rol y acceso
                print("\n" + "="*50)
                print("RESUMEN FINAL")
                print("="*50)
                print(f"Edad: {edad} años")
                print(f"Categoría de edad: {categoria_edad}")
                print(f"Rol: {rol.capitalize()}")
                print(f"Acceso al beneficio: {acceso}")
                print(f"Motivo: {motivo}")
                print("="*50)
                
                # Validar entradas con if-else y operadores de comparación
                if acceso == "SÍ":
                    print("\n✓ ¡Felicitaciones! Usted tiene acceso al sistema de beneficios.")
                    
                    # Recomendaciones personalizadas según categoría
                    if categoria_edad == "Infancia":
                        print("\nRecomendaciones para Infancia:")
                        print("  • Contenido educativo adaptado a su edad")
                        print("  • Actividades lúdicas y recreativas")
                        print("  • Supervisión de un adulto recomendada")
                    elif categoria_edad == "Adolescencia":
                        print("\nRecomendaciones para Adolescencia:")
                        print("  • Programas de orientación vocacional")
                        print("  • Talleres de desarrollo personal")
                        print("  • Acceso a recursos digitales educativos")
                    elif categoria_edad == "Adultez":
                        print("\nRecomendaciones para Adultez:")
                        print("  • Cursos de formación continua")
                        print("  • Oportunidades de networking profesional")
                        print("  • Recursos de desarrollo profesional")
                    else:
                        print("\nRecomendaciones para Persona Mayor:")
                        print("  • Programas de actualización tecnológica")
                        print("  • Actividades de bienestar y salud")
                        print("  • Comunidad de apoyo intergeneracional")
                else:
                    print("\n✗ Lo sentimos, actualmente no tiene acceso al sistema de beneficios.")
                    print("  Contacte al administrador para más información.")
        else:
            print("Error: Debe ingresar un número válido. Terminando programa.")
else:
    print("Error: Debe ingresar un número válido. Terminando programa.")