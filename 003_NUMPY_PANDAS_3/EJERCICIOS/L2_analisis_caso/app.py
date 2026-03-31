import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ CONFIGURACIÓN BÁSICA ------------------ #
st.set_page_config(
    page_title="Dashboard Empleados",
    page_icon="📊",
    layout="wide"
)

st.title(" Dashboard de Empleados - Pandas + Streamlit")
st.markdown("Dashboard local basado en los datos limpiados del caso de obtención de datos desde archivos.")

# ------------------ CARGA DE DATOS ------------------ #
@st.cache_data
def cargar_datos():
    df = pd.read_csv(r"D:\000_ANALISTA DATOS , TALENTO DIGITAL\002_A3\L2_analisis_caso\empleados_limpiados.csv")
    # Si en tu script renombraste columnas, ajusta aquí:
    # id_empleado, nombre_completo, departamento, salario_anual, fecha_ingreso, año_ingreso
    if "fecha_ingreso" in df.columns:
        df["fecha_ingreso"] = pd.to_datetime(df["fecha_ingreso"])
    return df

df = cargar_datos()

st.sidebar.header("Filtros")

# Filtro por departamento
deptos = df["departamento"].unique() if "departamento" in df.columns else df["Departamento"].unique()
col_depto = "departamento" if "departamento" in df.columns else "Departamento"

depto_sel = st.sidebar.multiselect(
    "Selecciona departamento(s)",
    options=sorted(deptos),
    default=list(deptos)
)

# Filtro por rango de salario
col_salario = "salario_anual" if "salario_anual" in df.columns else "Salario"
sal_min = float(df[col_salario].min())
sal_max = float(df[col_salario].max())

rango_salario = st.sidebar.slider(
    "Rango de salario",
    min_value=sal_min,
    max_value=sal_max,
    value=(sal_min, sal_max)
)

# Aplicar filtros
df_filtrado = df[
    (df[col_depto].isin(depto_sel)) &
    (df[col_salario] >= rango_salario[0]) &
    (df[col_salario] <= rango_salario[1])
]

# ------------------ MÉTRICAS RESUMEN ------------------ #
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total empleados", len(df_filtrado))
col2.metric("Salario promedio", f"{df_filtrado[col_salario].mean():,.0f}")
col3.metric("Salario mínimo", f"{df_filtrado[col_salario].min():,.0f}")
col4.metric("Salario máximo", f"{df_filtrado[col_salario].max():,.0f}")

st.markdown("---")

# ------------------ GRÁFICOS ------------------ #
col_g1, col_g2 = st.columns(2)

# 1) Salario promedio por departamento
with col_g1:
    st.subheader("Salario promedio por departamento")
    df_group = (
        df_filtrado
        .groupby(col_depto)[col_salario]
        .mean()
        .reset_index()
        .sort_values(col_salario, ascending=False)
    )
    fig1 = px.bar(
        df_group,
        x=col_depto,
        y=col_salario,
        text=col_salario,
        labels={col_depto: "Departamento", col_salario: "Salario promedio"},
        color=col_depto
    )
    fig1.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig1.update_layout(yaxis_title="Salario promedio")
    st.plotly_chart(fig1, use_container_width=True)

# 2) Distribución de salarios
with col_g2:
    st.subheader("Distribución de salarios")
    fig2 = px.histogram(
        df_filtrado,
        x=col_salario,
        nbins=10,
        labels={col_salario: "Salario"},
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ------------------ TABLA DETALLADA ------------------ #
st.subheader("Tabla de empleados filtrados")

st.dataframe(df_filtrado, use_container_width=True)

# Botón para descargar CSV filtrado
csv_filtrado = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Descargar CSV filtrado",
    data=csv_filtrado,
    file_name="empleados_filtrados.csv",
    mime="text/csv"
)
