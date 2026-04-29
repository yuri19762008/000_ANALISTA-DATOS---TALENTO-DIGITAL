# Herramientas de IA para la programación

Resumen de estudio basado en el material de clase **"Herramientas de IA para la programación"**. Este documento está pensado para repasar los conceptos con orden lógico, conectando desde los fundamentos de algoritmos hasta el uso estratégico y responsable de herramientas de inteligencia artificial en programación. [cite:1]

## Propósito de la clase

El objetivo principal de la clase es aprender a utilizar herramientas de inteligencia artificial para aumentar la productividad en programación, siguiendo buenas prácticas de la industria. El recorrido combina dos ejes: por un lado, fundamentos de algoritmos y su representación; por otro, uso de IA para asistir en generación, corrección y optimización de código mediante prompts bien diseñados. [cite:1]

## Fundamentos de algoritmos

Un algoritmo es un conjunto finito de pasos ordenados y definidos para resolver un problema. Para que una secuencia sea considerada algoritmo debe tener entrada, proceso, salida, determinismo y finitud. [cite:1]

El pensamiento algorítmico es la capacidad de descomponer un problema complejo en pasos manejables, prever resultados y estructurar una solución lógica. Esta habilidad se apoya en características como secuencialidad, repetición, condicionalidad, abstracción y modularidad. [cite:1]

### Componentes esenciales

Los componentes esenciales de un algoritmo son los datos de entrada y salida, el procesamiento y las variables. Las entradas corresponden a la información que el algoritmo necesita; el procesamiento es el conjunto de reglas que transforma esos datos; y las variables son espacios con nombre donde se almacenan valores que pueden cambiar durante la ejecución. [cite:1]

### Estructuras de control

Las estructuras de control permiten modelar el comportamiento de un algoritmo. La secuencia ejecuta instrucciones en el orden en que aparecen; las condicionales permiten tomar decisiones según una condición; y las estructuras repetitivas permiten ejecutar un bloque varias veces mediante construcciones como `Mientras`, `Repetir-Hasta` o `Para`. Dominar estas estructuras facilita la transición desde el pseudocódigo hacia un lenguaje de programación real. [cite:1]

## Pseudocódigo

El pseudocódigo es una forma intermedia entre lenguaje natural y programación real. Su función es describir la lógica de un algoritmo sin depender de la sintaxis de un lenguaje específico, por lo que se convierte en un puente muy útil entre la idea y la implementación. [cite:1]

Entre sus ventajas destacan la claridad estructural, la reducción de errores de sintaxis tempranos, la facilidad para colaborar y su valor pedagógico. Si la lógica está bien expresada en pseudocódigo, luego resulta más sencillo convertirla en código funcional. [cite:1]

### Reglas básicas de escritura

El material destaca varias reglas básicas: usar `Inicio` y `Fin`, emplear palabras clave como `Leer`, `Mostrar`, `Si`, `Entonces`, `Mientras` y `Para`, usar asignaciones con `←` o `=`, mantener sangrías claras y evitar ambigüedades mediante nombres descriptivos. [cite:1]

## PSeInt

PSeInt se presenta como una herramienta educativa para desarrollar lógica algorítmica con pseudocódigo estructurado. Permite escribir, ejecutar y depurar algoritmos sin necesidad de trabajar directamente con un lenguaje formal. [cite:1]

Entre sus características principales se mencionan la escritura de pseudocódigo en español o inglés, la ejecución paso a paso, la visualización del estado de variables, el editor de diagramas de flujo y el uso de plantillas. También se indica que los algoritmos pueden guardarse con extensión `.psc`. [cite:1]

### Valor del modo paso a paso

La ejecución línea por línea permite observar cómo se evalúan condiciones, cómo avanzan los bucles y cómo cambian las variables durante la ejecución. Esto ayuda a detectar errores lógicos, problemas de inicialización y bucles infinitos, además de fortalecer la intuición algorítmica del estudiante. [cite:1]

## Diagramas de flujo

Los diagramas de flujo representan gráficamente la secuencia lógica de un algoritmo mediante símbolos estandarizados y flechas. Se utilizan para visualizar el proceso completo, detectar errores y comunicar la lógica a otras personas con mayor rapidez. [cite:1]

Los símbolos clave mencionados en la clase son: óvalos para inicio y fin, rectángulos para procesos, rombos para decisiones, paralelogramos para entrada/salida y flechas para indicar el flujo. Entre las herramientas sugeridas aparecen draw.io, Lucidchart, Pencil Project, yEd y el propio PSeInt. [cite:1]

### Pseudocódigo y diagrama: herramientas complementarias

El material subraya que ambas representaciones cumplen funciones diferentes pero complementarias. El pseudocódigo ofrece detalle textual y cercanía a la programación real, mientras que el diagrama de flujo permite ver la lógica global del proceso y detectar conexiones incorrectas o bifurcaciones mal diseñadas. [cite:1]

## IA aplicada a la programación

La clase plantea que el desarrollo de software ya no depende solo de escribir código manualmente. Las herramientas de IA están transformando la productividad del programador al asistir en escritura, corrección, documentación y optimización de código, reduciendo tiempos y mejorando la calidad del software entregado. [cite:1]

Con este cambio, el rol del programador se vuelve más estratégico: no basta con usar una herramienta, sino que es necesario saber qué pedir, cómo evaluar la respuesta y cómo integrarla con criterio dentro del flujo de trabajo. [cite:1]

### Aplicaciones comunes de la IA en desarrollo

La IA puede asistir en tiempo real mientras se escribe código, ofrecer autocompletado inteligente, explicar código, detectar errores, generar boilerplate, convertir código entre lenguajes y crear pruebas unitarias a partir del código fuente. Estas aplicaciones tienen valor tanto para productividad como para aprendizaje. [cite:1]

## ChatGPT como asistente de programación

La clase presenta a ChatGPT como un asistente conversacional con capacidad para interactuar con múltiples lenguajes de programación. Entre sus usos se incluyen consultas de sintaxis, corrección de errores de compilación o lógica, sugerencias de estructuras algorítmicas, revisión de seguridad y generación de documentación técnica como archivos README. [cite:1]

El enfoque correcto no es aceptar automáticamente sus respuestas, sino utilizarlas como apoyo que debe ser validado y refinado por el desarrollador. [cite:1]

## Diseño de prompts

El diseño de prompts ocupa un lugar central en la clase porque la calidad de la respuesta depende directamente de cómo se formula la solicitud. Para analizar un prompt, se propone identificar su propósito, definir con claridad la acción que debe ejecutar el modelo, aportar contexto relevante y añadir detalles o restricciones que guíen la respuesta. [cite:1]

La estructura ideal de un prompt se resume en tres principios: ser claro, ser directo y ser específico. Un prompt ambiguo o demasiado general produce respuestas menos útiles; uno bien delimitado aumenta la precisión y la aplicabilidad del resultado. [cite:1]

## Modelos para estructurar prompts

El material presenta varios modelos de estructuración. RTF organiza el pedido en Rol, Tarea y Formato; Gherkin utiliza la secuencia Given, When, Then para describir escenarios; INVEST ayuda a formular pedidos pequeños, valiosos y comprobables; y CLEAR integra acción, problema, contexto, restricciones, herramienta específica y formato esperado. [cite:1]

Estos modelos no son fórmulas rígidas, sino guías prácticas para lograr que la IA entienda mejor la necesidad y entregue respuestas más alineadas con el objetivo. [cite:1]

### Ejemplo del modelo RTF

En RTF se define primero el rol de la IA, luego la tarea y finalmente el formato de salida. El ejemplo del material propone actuar como especialista en pruebas de software, escribir un caso de prueba para un formulario de inicio de sesión y entregar la respuesta en formato de tabla. [cite:1]

### Ejemplo del modelo Gherkin

Gherkin estructura casos de prueba con el patrón Dado, Cuando, Entonces. El ejemplo expuesto describe la prueba de una API de usuarios: dado un token válido, cuando se envía una solicitud GET al endpoint `/users`, entonces se espera una respuesta HTTP 200 y una lista de usuarios en JSON. [cite:1]

### Sentido práctico de CLEAR

La fórmula CLEAR permite especificar acción, dolor o necesidad, contexto, restricciones, herramienta concreta y formato esperado. La utilidad de esta estructura es que reduce la ambigüedad del pedido y hace más probable que la respuesta sea directamente usable. [cite:1]

## Ciclo de ingeniería de prompts

La clase propone un ciclo de trabajo iterativo para crear prompts efectivos. El proceso incluye definir el objetivo, identificar el contexto, construir una primera versión, probarla, analizar el resultado, refinar el prompt y validar si cumple el objetivo. [cite:1]

Este enfoque enseña que un buen prompt rara vez nace perfecto en el primer intento. La calidad suele aumentar mediante iteraciones sucesivas, comparando resultados y ajustando información, restricciones o formato. [cite:1]

## Mejores prácticas para optimizar prompts

El material enumera diez recomendaciones: asignar personalidad o rol a la IA, usar preguntas dirigidas, incluir contexto básico, agregar detalles relevantes, establecer restricciones, dar ejemplos guía, dividir tareas complejas, registrar resultados útiles, reutilizar lo que ya funcionó y entrenar a la IA para evaluar sus propias respuestas. [cite:1]

Estas prácticas convierten el prompting en una habilidad técnica que se puede mejorar con método, registro y repetición. [cite:1]

## Tipos de inteligencia artificial

La clase distingue varios tipos de IA. La IA generativa crea contenido original como texto, imágenes o código; la predictiva analiza datos históricos para prever resultados; la analítica procesa grandes volúmenes de información para extraer patrones; la conversacional interactúa mediante lenguaje natural; y la adaptativa ajusta su rendimiento en función de nuevos datos o entornos. [cite:1]

La intención de esta clasificación es entender que no todas las herramientas sirven para lo mismo y que elegir bien depende del problema que se desea resolver. [cite:1]

## Herramientas de IA destacadas

El material menciona varias herramientas y sus usos típicos en productos digitales. ChatGPT se orienta a ideación, documentación, testing y refactor conceptual; Gemini destaca en análisis de documentos y contenido multimodal; Claude se asocia a síntesis de entrevistas y documentación de producto; GitHub Copilot ayuda con autocompletado dentro del entorno de desarrollo; y Hugging Face permite prototipar soluciones de IA con modelos preentrenados. [cite:1]

También se nombran Notion AI para organización y priorización, Gamma para presentaciones, Canva AI para material visual y DALL·E para generación de imágenes. La lógica general es que cada herramienta aporta valor en tareas distintas dentro del trabajo digital. [cite:1]

## Beneficios concretos de usar IA en programación

Entre los beneficios señalados están el incremento de la productividad, la mejora en la calidad del código, la aceleración del aprendizaje técnico, la documentación automatizada y el apoyo en debugging y testing. La idea central es que la IA libera tiempo de tareas repetitivas y permite concentrar más esfuerzo en diseño, validación y resolución de problemas de mayor nivel. [cite:1]

Además, al actuar como tutor interactivo, puede explicar errores, proponer alternativas y ayudar a comprender conceptos complejos en lenguaje natural. [cite:1]

## Consideraciones éticas y de seguridad

El material enfatiza que el uso de IA debe ser responsable. Si una herramienta genera código basado en ejemplos populares o repositorios públicos, corresponde citar fuentes cuando el contenido vaya a reutilizarse en contextos académicos, abiertos o comerciales. [cite:1]

También se advierte evitar automatizaciones maliciosas o fraudulentas, como scraping abusivo, bots que infringen normas o desarrollos orientados a violar políticas de uso. En paralelo, se recuerda que la IA no es infalible: puede generar código incorrecto, vulnerable o ineficiente, por lo que siempre debe complementarse con testing, análisis estático y revisión humana. [cite:1]

En entornos empresariales, la formulación de prompts también debe considerar privacidad y seguridad. No basta con obtener una buena respuesta; además, es necesario proteger datos sensibles y cumplir políticas internas. [cite:1]

## Ejercicio aplicado: número primo

El ejercicio principal de la clase consiste en diseñar un algoritmo que determine si un número es primo, representarlo en pseudocódigo, llevarlo a diagrama de flujo y ejecutarlo paso a paso en PSeInt. El propósito de esta actividad es integrar estructuras de control, variables, finitud, determinismo y observación del estado interno del algoritmo durante su ejecución. [cite:1]

La importancia de este ejercicio no está solo en resolver el problema matemático, sino en practicar una secuencia completa de pensamiento computacional: entender el problema, estructurar la solución, representarla en diferentes formatos y validarla mediante simulación. [cite:1]

## Qué se espera dominar para el examen

Según el cierre de la clase, se espera comprender qué es un algoritmo y por qué sirve para resolver problemas, estructurar pseudocódigo con palabras clave correctas, utilizar PSeInt para ejecutar paso a paso, construir diagramas de flujo y reconocer tanto las principales herramientas de IA gratuitas como distintas formas de escribir prompts. [cite:1]

En otras palabras, el examen probablemente no medirá solo memoria, sino también comprensión del flujo lógico completo: desde la formulación de una solución algorítmica hasta el uso crítico y responsable de la IA como apoyo en programación. [cite:1]
