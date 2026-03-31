# app.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path

# -------------------------
# Configuración general
# -------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ecommerce_sales_data-2.csv"

st.set_page_config(
    page_title="Dashboard ComercioYA",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = ["Order Date", "Product", "Category", "Region",
                  "Quantity", "Sales", "Profit"]
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    return df

df = load_data()
variables_numericas = ["Quantity", "Sales", "Profit"]

# -------------------------
# Sidebar: filtros
# -------------------------
st.sidebar.title("Filtros")

years = sorted(df["Year"].unique())
year_sel = st.sidebar.multiselect("Año", years, default=years)

categories = sorted(df["Category"].unique())
cat_sel = st.sidebar.multiselect("Categoría", categories, default=categories)

regions = sorted(df["Region"].unique())
reg_sel = st.sidebar.multiselect("Región", regions, default=regions)

df_f = df[
    df["Year"].isin(year_sel)
    & df["Category"].isin(cat_sel)
    & df["Region"].isin(reg_sel)
]

st.sidebar.markdown(f"Registros filtrados: **{len(df_f)}**")

# -------------------------
# Cabecera
# -------------------------
st.title("Dashboard EDA ComercioYA")
st.caption("Basado en ecommerce_sales_data-2.csv - Ventas, cantidad y ganancia por producto, categoría y región.")
st.caption("Desarrollado por: Yuri Urzua Lebuy - Analista de Datos")


# Tabs para organizar todo
st.subheader("SELECCION DE ETIQUETAS Y GRAFICOS")
tab_resumen, tab_tablas, tab_graficos1, tab_graficos2 = st.tabs(
    ["RESUMEN", "TABLAS", "GRAFICOS EDA", "GRAFICOS AVANZADOS"]
)

# =====================================================
# TAB 1: RESUMEN (KPIs + tabla de vista rápida)
# =====================================================
with tab_resumen:
    st.subheader("Indicadores generales")

    total_sales = df_f["Sales"].sum()
    total_profit = df_f["Profit"].sum()
    avg_profit = df_f["Profit"].mean()
    total_qty = df_f["Quantity"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ventas totales (Sales)", f"${total_sales:,.0f}")
    col2.metric("Ganancia total (Profit)", f"${total_profit:,.0f}")
    col3.metric("Ganancia promedio", f"${avg_profit:,.1f}")
    col4.metric("Unidades vendidas", f"{total_qty:,}")

    st.markdown("### Vista rápida de datos filtrados")
    st.dataframe(df_f.head(50))

# =====================================================
# TAB 2: TABLAS (todas las tablas agregadas)
# =====================================================
with tab_tablas:
    st.subheader("Tablas de análisis")

    st.markdown("#### 1) Estadística descriptiva (variables numéricas)")
    desc = df_f[variables_numericas].describe().T
    desc["variance"] = df_f[variables_numericas].var().values
    st.dataframe(desc)

    st.markdown("#### 2) Ventas y ganancia por categoría")
    sales_profit_cat = (
        df_f.groupby("Category")[["Sales", "Profit", "Quantity"]]
        .sum()
        .sort_values("Sales", ascending=False)
        .reset_index()
    )
    st.dataframe(sales_profit_cat)

    st.markdown("#### 3) Ventas y ganancia por región")
    sales_profit_reg = (
        df_f.groupby("Region")[["Sales", "Profit", "Quantity"]]
        .sum()
        .sort_values("Sales", ascending=False)
        .reset_index()
    )
    st.dataframe(sales_profit_reg)

    st.markdown("#### 4) Ventas y ganancia por año")
    sales_profit_year = (
        df_f.groupby("Year")[["Sales", "Profit", "Quantity"]]
        .sum()
        .reset_index()
    )
    st.dataframe(sales_profit_year)

    st.markdown("#### 5) Top 15 productos por ganancia")
    top_products = (
        df_f.groupby("Product")[["Sales", "Profit", "Quantity"]]
        .sum()
        .sort_values("Profit", ascending=False)
        .head(15)
        .reset_index()
    )
    st.dataframe(top_products)

# =====================================================
# TAB 3: GRÁFICOS EDA (equivalentes a main.py básicos)
# =====================================================
with tab_graficos1:
    st.subheader("Gráficos exploratorios")

    col_g1, col_g2 = st.columns(2)

    # Histograma de Sales
    with col_g1:
        st.markdown("##### Histograma de Ventas (Sales)")
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.histplot(df_f["Sales"], bins=30, kde=True, ax=ax)
        ax.set_title("Histograma de Ventas (Sales)")
        st.pyplot(fig)

    # Histograma de Profit
    with col_g2:
        st.markdown("##### Histograma de Ganancia (Profit)")
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.histplot(df_f["Profit"], bins=30, kde=True, ax=ax)
        ax.set_title("Histograma de Ganancia (Profit)")
        st.pyplot(fig)

    col_g3, col_g4 = st.columns(2)

    # Boxplot Sales por Category
    with col_g3:
        st.markdown("##### Ventas (Sales) por Categoría")
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.boxplot(data=df_f, x="Category", y="Sales", ax=ax)
        ax.set_title("Ventas (Sales) por Categoría")
        ax.tick_params(axis="x")
        st.pyplot(fig)

    # Boxplot Profit por Region
    with col_g4:
        st.markdown("##### Ganancia (Profit) por Región")
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.boxplot(data=df_f, x="Region", y="Profit", ax=ax)
        ax.set_title("Ganancia (Profit) por Región")
        st.pyplot(fig)

    st.markdown("##### Matriz de correlación (Quantity, Sales, Profit)")
    corr = df_f[variables_numericas].corr()
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
    ax.set_title("Matriz de correlación")
    st.pyplot(fig)

# =====================================================
# TAB 4: GRÁFICOS AVANZADOS (scatter, pairplot, barras)
# =====================================================
with tab_graficos2:
    st.subheader("Gráficos avanzados")

    col_a1, col_a2 = st.columns(2)

    # Scatter Sales vs Profit
    with col_a1:
        st.markdown("##### Ventas (Sales) vs Ganancia (Profit) por categoría")
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.scatterplot(
            data=df_f,
            x="Sales",
            y="Profit",
            hue="Category",
            alpha=0.7,
            ax=ax
        )
        ax.set_title("Sales vs Profit")
        st.pyplot(fig)

    # Scatter Quantity vs Profit
    with col_a2:
        st.markdown("##### Cantidad (Quantity) vs Ganancia (Profit) por región")
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.scatterplot(
            data=df_f,
            x="Quantity",
            y="Profit",
            hue="Region",
            alpha=0.7,
            ax=ax
        )
        ax.set_title("Quantity vs Profit")
        st.pyplot(fig)

    st.markdown("##### Ventas (Sales) totales por año y categoría")
    sales_year_cat = (
        df_f.groupby(["Year", "Category"])["Sales"]
        .sum()
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=sales_year_cat, x="Year", y="Sales", hue="Category", ax=ax)
    ax.set_title("Ventas (Sales) totales por año y categoría")
    st.pyplot(fig)

    st.markdown("##### Pairplot (Ventas, Ganancia, Cantidad)")
    # Para no explotar el navegador, limitamos a una muestra si hay muchos registros
    sample = df_f[["Sales", "Profit", "Quantity"]]
    if len(sample) > 300:
        sample = sample.sample(300, random_state=42)

    fig = sns.pairplot(sample)
    st.pyplot(fig)
