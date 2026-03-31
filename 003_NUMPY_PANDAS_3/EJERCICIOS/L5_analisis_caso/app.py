import pandas as pd
import streamlit as st
import plotly.express as px

# =========================
# CONFIGURACIÓN DE LA APP
# =========================
st.set_page_config(
    page_title="Dashboard Fintech - Transacciones",
    page_icon="💳",
    layout="wide"
)


@st.cache_data
def cargar_datos(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Asegurar tipo fecha si existe la columna
    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"])
    return df


# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙️ Controles")

# Selector de archivo: raw vs limpio
opcion_archivo = st.sidebar.selectbox(
    "Archivo a visualizar",
    options=[
        "transacciones_raw.csv",
        "transacciones_limpias.csv"
    ],
    index=0
)

# Ruta base opcional
ruta_base = st.sidebar.text_input(
    "Ruta base (deja vacío si los archivos están en esta carpeta)",
    value=""
)

if ruta_base.strip():
    ruta_completa = ruta_base.rstrip("/") + "/" + opcion_archivo
else:
    ruta_completa = opcion_archivo

st.sidebar.markdown(f"**Archivo seleccionado:** `{ruta_completa}`")
st.sidebar.markdown("---")
st.sidebar.markdown("**Filtros**")

# Cargar datos
df = cargar_datos(ruta_completa)

# Detectar nombre real de columnas clave
col_monto = "monto_transaccion" if "monto_transaccion" in df.columns else "monto"
col_cliente = "cliente_id" if "cliente_id" in df.columns else "id_cliente"

# Filtros dinámicos según las columnas disponibles
if "segmento_cliente" in df.columns:
    segmentos = st.sidebar.multiselect(
        "Segmento cliente",
        options=sorted(df["segmento_cliente"].dropna().unique()),
        default=sorted(df["segmento_cliente"].dropna().unique())
    )
else:
    segmentos = []

if "tipo_transaccion" in df.columns:
    tipos = st.sidebar.multiselect(
        "Tipo de transacción",
        options=sorted(df["tipo_transaccion"].dropna().unique()),
        default=sorted(df["tipo_transaccion"].dropna().unique())
    )
else:
    tipos = []

if "pais" in df.columns:
    paises = st.sidebar.multiselect(
        "País",
        options=sorted(df["pais"].dropna().unique()),
        default=sorted(df["pais"].dropna().unique())
    )
else:
    paises = []

if "fecha" in df.columns:
    fecha_min = df["fecha"].min()
    fecha_max = df["fecha"].max()
    rango_fechas = st.sidebar.date_input(
        "Rango de fechas",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max
    )
else:
    rango_fechas = None

st.sidebar.markdown("---")
st.sidebar.caption("Dashboard demo con Streamlit + Pandas.")


# =========================
# APLICAR FILTROS
# =========================
df_filtrado = df.copy()

if segmentos and "segmento_cliente" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["segmento_cliente"].isin(segmentos)]

if tipos and "tipo_transaccion" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["tipo_transaccion"].isin(tipos)]

if paises and "pais" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["pais"].isin(paises)]

if rango_fechas and "fecha" in df_filtrado.columns:
    inicio, fin = rango_fechas
    df_filtrado = df_filtrado[
        (df_filtrado["fecha"] >= pd.to_datetime(inicio)) &
        (df_filtrado["fecha"] <= pd.to_datetime(fin))
    ]


# =========================
# TÍTULO Y DESCRIPCIÓN
# =========================
st.title("💳 Dashboard de Transacciones Fintech")
st.caption(
    "Explora las transacciones de los archivos `transacciones_raw.csv` "
    "y `transacciones_limpias.csv` con filtros interactivos."
)


# =========================
# MÉTRICAS (KPIs)
# =========================
col1, col2, col3, col4 = st.columns(4)

if col_monto in df_filtrado.columns:
    monto_total = df_filtrado[col_monto].sum()
    monto_promedio = df_filtrado[col_monto].mean()
else:
    monto_total = 0
    monto_promedio = 0

num_transacciones = len(df_filtrado)
if col_cliente in df_filtrado.columns:
    clientes_unicos = df_filtrado[col_cliente].nunique()
else:
    clientes_unicos = 0

col1.metric("Monto total (filtrado)", f"{monto_total:,.2f}")
col2.metric("Monto promedio", f"{monto_promedio:,.2f}")
col3.metric("N° transacciones", num_transacciones)
col4.metric("Clientes únicos", clientes_unicos)


# =========================
# TABLA
# =========================
st.subheader("📄 Tabla de transacciones filtradas")
st.dataframe(df_filtrado, use_container_width=True)


# =========================
# GRÁFICOS
# =========================
st.subheader("📊 Visualizaciones")

tab1, tab2, tab3 = st.tabs(["Monto por fecha", "Monto por país", "Segmento vs Tipo"])

# 1. Monto total por fecha
with tab1:
    if {"fecha", col_monto}.issubset(df_filtrado.columns):
        df_fecha = (
            df_filtrado
            .groupby("fecha", as_index=False)[col_monto]
            .sum()
            .sort_values("fecha")
        )
        fig_fecha = px.line(
            df_fecha,
            x="fecha",
            y=col_monto,
            title=f"Monto total por fecha ({col_monto})",
            markers=True
        )
        st.plotly_chart(fig_fecha, use_container_width=True)
    else:
        st.info("No se pueden generar montos por fecha (faltan columnas de fecha o monto).")

# 2. Monto por país
with tab2:
    if {"pais", col_monto}.issubset(df_filtrado.columns):
        df_pais = (
            df_filtrado
            .groupby("pais", as_index=False)[col_monto]
            .sum()
            .sort_values(col_monto, ascending=False)
        )
        fig_pais = px.bar(
            df_pais,
            x="pais",
            y=col_monto,
            title=f"Monto total por país ({col_monto})",
            text_auto=".2s"
        )
        st.plotly_chart(fig_pais, use_container_width=True)
    else:
        st.info("No se pueden generar montos por país (faltan columnas de país o monto).")

# 3. Monto por segmento y tipo de transacción
with tab3:
    if {"segmento_cliente", "tipo_transaccion", col_monto}.issubset(df_filtrado.columns):
        df_seg_tipo = (
            df_filtrado
            .groupby(["segmento_cliente", "tipo_transaccion"], as_index=False)[col_monto]
            .sum()
        )
        fig_seg_tipo = px.bar(
            df_seg_tipo,
            x="segmento_cliente",
            y=col_monto,
            color="tipo_transaccion",
            barmode="group",
            title=f"Monto por segmento de cliente y tipo de transacción ({col_monto})"
        )
        st.plotly_chart(fig_seg_tipo, use_container_width=True)
    else:
        st.info(
            "No se pueden generar montos por segmento y tipo "
            "(faltan columnas de segmento, tipo o monto)."
        )


# =========================
# DESCARGA DE DATOS FILTRADOS
# =========================
st.subheader("⬇️ Descargar datos filtrados")
csv_filtrado = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Descargar CSV filtrado",
    data=csv_filtrado,
    file_name="transacciones_filtradas.csv",
    mime="text/csv"
)
