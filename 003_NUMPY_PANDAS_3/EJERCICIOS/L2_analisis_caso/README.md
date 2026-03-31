# ANÁLISIS DE CASO: OBTENCIÓN DE DATOS DESDE ARCHIVOS CON PANDAS
## Resumen Ejecutivo y Guía Rápida

---


### 1. **Paso 1 ejecute su entorno virtual**
### 2. **Paso 2 instale dependencias con**  " pip install -r requirements.txt " 
### 3. **Ejecute solucion-pandas.py , si tiene errores verifique rutas**
### 4. **Adicional si ejecute el dashboard**  " streamlit run app.py "
### 5. **Si desea agregue mail, luego deberia abrir navegador en http://localhost:8501**

---

##  CONTENIDO GENERAL

He desarrollado **dos documentos complementarios** para tu caso de análisis:


### 1. **Script Ejecutable Completo** (solucion-pandas.py)
   - Código completamente funcional y listo para ejecutar
   - 10 secciones organizadas y documentadas
   - Genera archivos de salida reales
   - Puedes copiarlo y ejecutar directamente en Jupyter o terminal

### 2. **Esta Guía Rápida** (README)
   - Resumen de conceptos clave
   - Flujo del proceso
   - Comandos esenciales
   - Preguntas frecuentes

---

##  PROPÓSITO DEL CASO

**Contexto:** Una empresa de consultoría recibe datos de múltiples fuentes (CSV, Excel, web) con:
- Valores nulos (missing data)
- Filas duplicadas
- Tipos de datos inconsistentes
- Formatos variados

**Objetivo:** Automatizar un flujo de obtención, limpieza y exportación de datos usando Pandas.

---

##  DATOS DE EJEMPLO

### Datos Originales (7 filas)
```
ID | Nombre             | Departamento | Salario   | Fecha_Ingreso
─────────────────────────────────────────────────────────────────
1  | Juan García        | Ventas       | 45000.00  | 2022-01-15
2  | María López        | TI           | 52000.00  | 2021-06-20
3  | Carlos Pérez       | Finanzas     | 48000.00  | 2022-03-10
4  | Ana Martínez       | Ventas       | [NULL]    | 2020-11-05
5  | Juan García        | Ventas       | 45000.00  | 2022-01-15    ← DUPLICADO
6  | Pedro Rodríguez    | TI           | 51000.00  | [NULL]
7  | Laura Gómez        | RRHH         | 46000.00  | 2023-02-18
```

**Problemas:**
- 2 valores nulos (Salario, Fecha_Ingreso)
- 1 fila duplicada (Juan García)
- Tipos de datos sin validar

### Datos Limpios (5 filas)
```
ID | Nombre           | Departamento | Salario   | Fecha_Ingreso
──────────────────────────────────────────────────────────────
2  | María López      | TI           | 52000.00  | 2021-06-20
6  | Pedro Rodríguez  | TI           | 51500.00  | 2023-02-18 ← Imputado
3  | Carlos Pérez     | Finanzas     | 48000.00  | 2022-03-10
7  | Laura Gómez      | RRHH         | 46000.00  | 2023-02-18
1  | Juan García      | Ventas       | 45000.00  | 2022-01-15
```

**Mejoras:**
-  Sin duplicados
-  Sin valores nulos
-  Tipos validados
-  Datos ordenados por salario

---

##  FLUJO DEL PROCESO

```
┌─────────────────────────────────────┐
│    TAREA 1: CARGAR DATOS            │
│  (CSV, Excel, HTML)                 │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│    TAREA 2: LIMPIAR DATOS           │
│  (Nulos, duplicados, tipos)         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│    TAREA 3: TRANSFORMAR DATOS       │
│  (Seleccionar, renombrar, ordenar)  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│    TAREA 4: EXPORTAR DATOS          │
│  (CSV, Excel, análisis)             │
└─────────────────────────────────────┘
```

---

##  COMANDOS ESENCIALES

### Importación
```python
import pandas as pd
import numpy as np

# Leer diferentes formatos
# no olvidar cambiar rutas 
df_csv = pd.read_csv('archivo.csv')
df_excel = pd.read_excel('archivo.xlsx')
df_html = pd.read_html('url')[0]  # Tabla web
```

### Análisis Inicial
```python
# Exploración
df.head()              # Primeras filas
df.info()              # Tipos y memoria
df.describe()          # Estadísticas
df.isnull().sum()      # Valores nulos
df.duplicated().sum()  # Filas duplicadas
```

### Limpieza
```python
# Eliminar duplicados
df.drop_duplicates(subset=['columna'])

# Manejar nulos
df.fillna(valor)                    # Llenar con valor
df.dropna()                         # Eliminar filas
df.fillna(df.mean())                # Media
df.groupby('grupo').transform(...)  # Por grupo

# Convertir tipos
df['columna'] = df['columna'].astype('tipo')
df['fecha'] = pd.to_datetime(df['fecha'])
```

### Transformación
```python
# Seleccionar columnas
df[['col1', 'col2']]

# Renombrar
df.rename(columns={'viejo': 'nuevo'})

# Ordenar
df.sort_values(by='columna', ascending=False)

# Agregar
df.groupby('grupo').agg({'col': 'sum'})
```

### Exportación
```python
# Guardar
# no olvidar cambiar rutas 
df.to_csv('archivo.csv', index=False)
df.to_excel('archivo.xlsx', index=False)

# Múltiples hojas
with pd.ExcelWriter('archivo.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Hoja1')
    df2.to_excel(writer, sheet_name='Hoja2')
```

---

##  CONCEPTOS CLAVE

### 1. DataFrame
Estructura de datos tabular de Pandas (filas × columnas)
```python
df = pd.DataFrame({
    'columna1': [valores],
    'columna2': [valores]
})
```

### 2. Valores Nulos (NaN)
Datos faltantes. Se manejan con:
- **Imputación:** Rellenar con estimado (media, mediana, etc.)
- **Eliminación:** Borrar filas/columnas con nulos

**Estrategia:**
```python
# Imputar por grupo
df['salario'].fillna(df.groupby('depto')['salario'].transform('mean'))

# Eliminar si es crítico
df.dropna(subset=['fecha_importante'])
```

### 3. Duplicados
Filas idénticas o parcialmente idénticas
```python
# Detectar
df.duplicated(subset=['nombre', 'depto'])

# Eliminar (mantener primero)
df.drop_duplicates(subset=['nombre', 'depto'], keep='first')
```

### 4. Tipos de Datos
Asegurar que las columnas tengan tipos correctos
```python
df.dtypes  # Ver tipos actuales

# Conversiones comunes
df['id'] = df['id'].astype('int64')
df['nombre'] = df['nombre'].astype('string')
df['fecha'] = pd.to_datetime(df['fecha'])
df['categoria'] = df['categoria'].astype('category')
```

### 5. Transformación
Cambios estructura/contenido sin perder información
```python
# Seleccionar
df[['col1', 'col2']]

# Renombrar (mejorar legibilidad)
df.rename(columns={'col_vieja': 'col_nueva'})

# Ordenar
df.sort_values(by='columna', ascending=False)

# Crear derivadas
df['año'] = df['fecha'].dt.year
df['salario_mensual'] = df['salario_anual'] / 12
```

---

##  PREGUNTAS FRECUENTES

**P: ¿Por qué no eliminar todos los valores nulos?**
R: Podrías perder datos importantes. Estrategia mejor:
- Analizar qué datos son críticos vs. dispensables
- Imputar si hay información para estimarlo
- Eliminar solo si hay pocas filas nulas

**P: ¿Cuándo usar imputación vs. eliminación?**
R:
- **Imputación:** Columnas con muchos datos válidos (media, mediana)
- **Eliminación:** Columnas críticas (ID, fecha) o muchos nulos (>50%)

**P: ¿Necesito validar tipos de datos manualmente?**
R: Sí, aunque Pandas inferencias. Pandas puede confundir:
- Fechas como texto: `'2024-01-15'` vs `datetime`
- Números como texto: `'100'` vs `100`
- Categorías como texto: `'Activo'` vs `category`

**P: ¿Cómo detectar duplicados bien?**
R: Especifica columnas clave:
```python
# Solo por nombre y departamento (más específico)
df.drop_duplicates(subset=['nombre', 'depto'])

# Vs. todas las columnas (demasiado estricto)
df.drop_duplicates()
```

**P: ¿Puedo recuperar datos después de eliminar filas?**
R: Sí, trabaja siempre con copia:
```python
df_original = df.copy()  # Respaldo
df = df.drop_duplicates()  # Modificar copia
# Si no funciona, recupera original
```

---

##  IMPACTO DEL CASO

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Filas | 7 | 5 | -28.6% (sin duplicados) |
| Valores nulos | 2 | 0 | 100% |
| Duplicados | 1 | 0 | 100% |
| Tipos validados | No | Sí | 100% |
| Listo para análisis | No | Sí | ✓ |

---

##  APRENDIZAJES CLAVE

1. **Proceso > Herramienta**
   - No es solo ejecutar código, es entender problemas
   - Cada decisión debe tener justificación técnica

2. **Exploratorio Primero**
   - Siempre revisar `df.info()`, `df.describe()`, etc.
   - Entender datos antes de limpiar

3. **Preserve Original**
   - Copia los datos: `df = df.copy()`
   - Facilita debugging si algo sale mal

4. **Documentar Decisiones**
   - ¿Por qué eliminas esa fila?
   - ¿Por qué imputas con media y no mediana?
   - Importante para auditoría y reproducibilidad

5. **Validar Resultados**
   - Después de cada operación, verifica
   - Compara antes vs. después
   - Asegúrate que cambios son correctos

---

##  PRÓXIMOS PASOS

### Nivel Intermedio
-  Cargar datos de bases de datos (SQLite, PostgreSQL)
-  Validación de restricciones de negocio
-  Manejo de archivos muy grandes (chunking)
-  Automatización con scheduling

### Nivel Avanzado
-  Construcción de pipelines (Luigi, Airflow)
-  APIs para consumir datos limpios
-  Monitoreo de calidad en producción
-  Machine Learning con datos preprocesados

---

##  RECURSOS RECOMENDADOS

**Documentación:**
- Pandas Official: https://pandas.pydata.org/
- Stack Overflow: Preguntas sobre Pandas
- Kaggle: Datasets para practicar

**Libros:**
- "Python for Data Analysis" - Wes McKinney (autor de Pandas)
- "Data Cleaning and Preparation" - Mike Tupy

**Tutoriales:**
- YouTube: "Data Cleaning with Pandas"
- DataCamp: "Data Cleaning in Python"

---

##  CHECKLIST PARA TU ENTREGA

Para completar correctamente el caso, asegúrate de:

- [ ] **Código Fuente**
  - [ ] Script Python bien comentado
  - [ ] Importaciones claras
  - [ ] Funciona sin errores

- [ ] **Explicación Detallada**
  - [ ] Cada paso justificado
  - [ ] Problemas identificados
  - [ ] Soluciones aplicadas
  - [ ] Alternativas consideradas

- [ ] **Datos Antes/Después**
  - [ ] Mostrar datos originales (con problemas)
  - [ ] Mostrar datos finales (limpios)
  - [ ] Comparación clara

- [ ] **Análisis Adicionales**
  - [ ] Resumen por departamento
  - [ ] Estadísticas descriptivas
  - [ ] Insights relevantes

- [ ] **Archivos Generados**
  - [ ] CSV limpio sin índice
  - [ ] Excel con múltiples hojas
  - [ ] Archivos validados

- [ ] **Conclusiones**
  - [ ] Importancia del proceso
  - [ ] Impacto en el negocio
  - [ ] Lecciones aprendidas
  - [ ] Mejoras futuras

---

##  SOPORTE

Si tienes dudas sobre el código:

1. **Revisa el script ejecutable** (solucion-pandas.py)
2. **Consulta el documento teórico** (caso-analisis-pandas.md)
3. **Ejecuta paso a paso** en Jupyter Notebook
4. **Agrega prints()** para debug
5. **Compara tu salida** con las esperadas

---

**Documento preparado por:** Yuri Urzua Lebuy 
**Fecha:** Enero 2026   
**Duración estimada:** 2-4 horas para estudiar y ejecutar  


