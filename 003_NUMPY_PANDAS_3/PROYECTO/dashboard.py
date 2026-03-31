import pandas as pd
import streamlit as st

st.set_page_config(page_title="Clientes E-commerce", layout="wide")

st.title("Dashboard - Clientes E-commerce")

# -----------------------
# Carga de datos
# -----------------------
@st.cache_data
def cargar_dataset_final():
    return pd.read_csv("dataset_final.csv")

df = cargar_dataset_final()

st.subheader("Vista general del dataset final")
st.dataframe(df, use_container_width=True)

# -----------------------
# Filtros en sidebar
# -----------------------
st.sidebar.header("Filtros")

ciudades = ["(Todas)"] + sorted(df["Ciudad"].dropna().unique().tolist()) \
    if "Ciudad" in df.columns else ["(Todas)"]
ciudad_sel = st.sidebar.selectbox("Ciudad", ciudades)

segmentos = ["(Todos)"] + sorted(df["Segmento_Monto"].dropna().unique().tolist()) \
    if "Segmento_Monto" in df.columns else ["(Todos)"]
segmento_sel = st.sidebar.selectbox("Segmento de monto", segmentos)

df_filtrado = df.copy()
if "Ciudad" in df.columns and ciudad_sel != "(Todas)":
    df_filtrado = df_filtrado[df_filtrado["Ciudad"] == ciudad_sel]

if "Segmento_Monto" in df.columns and segmento_sel != "(Todos)":
    df_filtrado = df_filtrado[df_filtrado["Segmento_Monto"] == segmento_sel]

st.subheader("Datos filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# -----------------------
# Métricas principales
# -----------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total clientes", len(df_filtrado))

with col2:
    st.metric(
        "Monto total",
        f"{df_filtrado['Monto_Total'].sum():,.0f}"
        if "Monto_Total" in df_filtrado.columns else "N/A",
    )

with col3:
    st.metric(
        "Ticket promedio",
        f"{df_filtrado['Ticket_Promedio'].mean():.1f}"
        if "Ticket_Promedio" in df_filtrado.columns else "N/A",
    )

# -----------------------
# Gráficos
# -----------------------
st.subheader("Compras por ciudad")

if "Ciudad" in df_filtrado.columns and "Monto_Total" in df_filtrado.columns:
    compras_ciudad = (
        df_filtrado.groupby("Ciudad")["Monto_Total"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(compras_ciudad)
else:
    st.write("No hay columnas 'Ciudad' y 'Monto_Total' para graficar.")

st.subheader("Distribución de monto total")

if "Monto_Total" in df_filtrado.columns:
    st.hist_chart = st.bar_chart(
        df_filtrado["Monto_Total"].value_counts().sort_index()
    )
else:
    st.write("No hay columna 'Monto_Total' para la distribución.")
