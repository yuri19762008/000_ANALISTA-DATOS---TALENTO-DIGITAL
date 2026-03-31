"""
Proyecto: Análisis exploratorio de datos para decisiones comerciales - ComercioYA
Dataset: ecommerce_sales_data-2.csv

Este script implementa paso a paso las 6 lecciones del módulo de Análisis Exploratorio de Datos:
1) EDA e identificación de variables
2) Estadística descriptiva
3) Correlación
4) Regresiones lineales
5) Análisis visual con Seaborn
6) Visualizaciones personalizadas con Matplotlib
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pathlib import Path

# -----------------------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = Path(r"D:\000_ANALISTA DATOS , TALENTO DIGITAL\003_A4\PROYECTO\ecommerce_sales_data-2.csv")
FIGURES_DIR = BASE_DIR / Path("figures")
FIGURES_DIR.mkdir(exist_ok=True)

sns.set(style="whitegrid", context="talk")


def main():
    # -------------------------------------------------------------------------
    # LECCIÓN 1: EDA INICIAL (IDA) - TIPOS DE VARIABLES Y VALORES FALTANTES
    # -------------------------------------------------------------------------
    print("\n=== LECCIÓN 1: EDA inicial (IDA) ===\n")

    # Carga de datos SIN encabezado, asignando nombres manualmente
    df = pd.read_csv(DATA_PATH)

# Si los nombres no son exactamente estos, puedes renombrarlos:
# print(df.columns) para verlos y luego ajustarlos.
    df.columns = ["Order Date", "Product", "Category", "Region",
              "Quantity", "Sales", "Profit"]


    # Conversión de tipos
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    print("Primeras filas:")
    print(df.head(), "\n")

    print("Información del DataFrame:")
    print(df.info(), "\n")

    # Clasificación de variables
    variables_numericas = ["Quantity", "Sales", "Profit"]
    variables_categoricas = ["Product", "Category", "Region"]

    print("Variables numéricas:", variables_numericas)
    print("Variables categóricas:", variables_categoricas, "\n")

    # Valores faltantes
    missing = df.isna().sum()
    print("Valores faltantes por columna:")
    print(missing, "\n")

    # Resumen estadístico inicial
    print("Resumen estadístico inicial (numéricas):")
    print(df[variables_numericas].describe(), "\n")

    # Columnas temporales
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month

    # -------------------------------------------------------------------------
    # LECCIÓN 2: ESTADÍSTICA DESCRIPTIVA
    # -------------------------------------------------------------------------
    print("\n=== LECCIÓN 2: Estadística descriptiva ===\n")

    desc = df[variables_numericas].describe().T
    desc["variance"] = df[variables_numericas].var().values
    print("Descriptivos extendidos (incluye varianza):")
    print(desc, "\n")

    # Histogramas
    for col in variables_numericas:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col], bins=30, kde=True)
        plt.title(f"Histograma de {col}")
        plt.xlabel(col)
        plt.ylabel("Frecuencia")
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / f"hist_{col.lower()}.png")
        plt.close()

    # Boxplots por Category
    for col in ["Sales", "Profit"]:
        plt.figure(figsize=(8, 5))
        sns.boxplot(data=df, x="Category", y=col)
        plt.title(f"{col} por Category")
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / f"box_{col.lower()}_by_category.png")
        plt.close()

    # Outliers en Profit con IQR
    Q1 = df["Profit"].quantile(0.25)
    Q3 = df["Profit"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers_profit = df[(df["Profit"] < lower_bound) | (df["Profit"] > upper_bound)]
    print(f"Número de outliers en Profit: {len(outliers_profit)}\n")

    # -------------------------------------------------------------------------
    # LECCIÓN 3: CORRELACIÓN
    # -------------------------------------------------------------------------
    print("\n=== LECCIÓN 3: Correlación ===\n")

    corr_matrix = df[variables_numericas].corr(method="pearson")
    print("Matriz de correlación (Pearson):")
    print(corr_matrix, "\n")

    plt.figure(figsize=(6, 5))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title("Matriz de correlación - Variables numéricas")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "heatmap_correlation.png")
    plt.close()

    # Scatterplots clave
    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=df, x="Sales", y="Profit", hue="Category")
    plt.title("Sales vs Profit por Category")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "scatter_sales_profit_category.png")
    plt.close()

    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=df, x="Quantity", y="Profit", hue="Region")
    plt.title("Quantity vs Profit por Region")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "scatter_quantity_profit_region.png")
    plt.close()

    # -------------------------------------------------------------------------
    # LECCIÓN 4: REGRESIONES LINEALES
    # -------------------------------------------------------------------------
    print("\n=== LECCIÓN 4: Regresiones lineales ===\n")

    y = df["Profit"]

    # Modelo simple: Profit ~ Sales
    X_simple = df[["Sales"]]
    X_simple = sm.add_constant(X_simple)
    model_simple = sm.OLS(y, X_simple).fit()
    print("Modelo simple: Profit ~ Sales")
    print(model_simple.summary(), "\n")

    # Modelo múltiple: Profit ~ Sales + Quantity
    X_multi = df[["Sales", "Quantity"]]
    X_multi = sm.add_constant(X_multi)
    model_multi = sm.OLS(y, X_multi).fit()
    print("Modelo múltiple: Profit ~ Sales + Quantity")
    print(model_multi.summary(), "\n")

    # Visualizar regresión simple
    plt.figure(figsize=(7, 5))
    sns.regplot(data=df, x="Sales", y="Profit", scatter_kws={"alpha": 0.5})
    plt.title("Regresión lineal simple: Profit ~ Sales")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "reg_simple_profit_sales.png")
    plt.close()

    # -------------------------------------------------------------------------
    # LECCIÓN 5: ANÁLISIS VISUAL CON SEABORN
    # -------------------------------------------------------------------------
    print("\n=== LECCIÓN 5: Análisis visual con Seaborn ===\n")
    print("\n=== LECCIÓN 5: El Analisis completo fue generado y almacenado ===\n")

    # Pairplot
    sns.pairplot(df[["Sales", "Profit", "Quantity"]])
    plt.savefig(FIGURES_DIR / "pairplot_numeric.png")
    plt.close()

    # Violinplot Profit por Region
    plt.figure(figsize=(8, 5))
    sns.violinplot(data=df, x="Region", y="Profit", inner="quartile")
    plt.title("Distribución de Profit por Region")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "violin_profit_region.png")
    plt.close()

    # Jointplot Sales vs Profit
    jp = sns.jointplot(data=df, x="Sales", y="Profit", kind="hex", height=7)
    jp.fig.suptitle("Jointplot Sales vs Profit", y=1.02)
    jp.savefig(FIGURES_DIR / "joint_sales_profit.png")
    plt.close()

    # FacetGrid: distribución de Sales por Region y Category
    g = sns.FacetGrid(df, col="Region", hue="Category", col_wrap=2, height=4, sharex=False)
    g.map(sns.histplot, "Sales", bins=20, alpha=0.6)
    g.add_legend()
    g.fig.subplots_adjust(top=0.9)
    g.fig.suptitle("Distribución de Sales por Region y Category")
    g.savefig(FIGURES_DIR / "facet_sales_region_category.png")
    plt.close()

    # -------------------------------------------------------------------------
    # LECCIÓN 6: MATPLOTLIB Y FIGURAS PERSONALIZADAS
    # -------------------------------------------------------------------------
    print("\n=== LECCIÓN 6: Visualizaciones personalizadas con Matplotlib ===\n")

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Sales por año
    sales_by_year = df.groupby("Year")["Sales"].sum()
    axes[0].bar(sales_by_year.index, sales_by_year.values, color="steelblue")
    axes[0].set_title("Sales totales por año")
    axes[0].set_xlabel("Año")
    axes[0].set_ylabel("Sales")

    # Sales por Category
    sales_by_cat = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    axes[1].bar(sales_by_cat.index, sales_by_cat.values, color="seagreen")
    axes[1].set_title("Sales totales por Category")
    axes[1].set_xlabel("Category")
    axes[1].tick_params(axis='x', rotation=45)

    # Profit por Region
    profit_by_region = df.groupby("Region")["Profit"].sum()
    axes[2].bar(profit_by_region.index, profit_by_region.values, color="darkorange")
    axes[2].set_title("Profit total por Region")
    axes[2].set_xlabel("Region")

    fig.suptitle("Resumen visual de desempeño de ComercioYA", fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.savefig(FIGURES_DIR / "summary_subplots.png")
    plt.close()

    print("Todos los gráficos fueron guardados en la carpeta 'figures/'.")
    print("Usa estos resultados para redactar tu informe técnico EDA y tu presentación final.\n")


if __name__ == "__main__":
    main()
