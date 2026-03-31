# distribuciones_interactivas_app.py
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as stats
import streamlit as st

st.set_page_config(page_title="Distribuciones interactivas", layout="wide")

st.title("Actividad: ¿Qué distribución usarías? – Versión interactiva")

st.markdown("""
Usa la barra lateral para elegir el **tipo de problema** (casos 1–10) y ajusta los parámetros
con los *sliders* para ver cómo cambia la distribución.
""")

# --------- SIDEBAR: selección de caso ---------
st.sidebar.header("Configuración")

casos = {
    "1) Número de clientes en una hora (Poisson)": 1,
    "2) Tiempo hasta falla de servidor (Exponencial)": 2,
    "3) Puntaje prueba estandarizada (Normal)": 3,
    "4) Media con σ desconocida (t de Student)": 4,
    "5) Comparar variabilidad de ventas (F)": 5,
    "6) Número de éxitos en 20 intentos (Binomial)": 6,
    "7) Tiempo hasta próxima llamada (Exponencial)": 7,
    "8) Relación género vs preferencia (χ²)": 8,
    "9) Altura de personas adultas (Normal)": 9,
    "10) Comparar medias de tres grupos (F – ANOVA)": 10,
}

opcion = st.sidebar.selectbox("Elige el caso:", list(casos.keys()))
caso = casos[opcion]

fig, ax = plt.subplots(figsize=(7, 4))

# --------- CASO 1: Poisson (clientes por hora) ---------
if caso == 1:
    st.subheader("Caso 1: Número de clientes que llegan a una tienda en una hora")
    lam = st.sidebar.slider("λ (clientes promedio por hora)", 1, 60, 10)
    max_x = lam + 4 * int(np.sqrt(lam))
    x = np.arange(0, max_x + 1)
    pmf = stats.poisson(lam).pmf(x)

    ax.stem(x, pmf)
    ax.set_xlabel("Número de clientes en una hora (X)")
    ax.set_ylabel("P(X = x)")
    ax.set_title(f"Poisson(λ = {lam})")
    ax.grid(True)

# --------- CASO 2: Exponencial (fallo servidor) ---------
elif caso == 2:
    st.subheader("Caso 2: Tiempo que tarda en fallar un servidor")
    media = st.sidebar.slider("Media del tiempo hasta fallo (horas)", 1, 200, 50)
    x = np.linspace(0, media * 5, 400)
    pdf = stats.expon(scale=media).pdf(x)

    ax.plot(x, pdf)
    ax.set_xlabel("Horas hasta el fallo (X)")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Exponencial(media = {media} horas)")
    ax.grid(True)

# --------- CASO 3: Normal (puntaje prueba) ---------
elif caso == 3:
    st.subheader("Caso 3: Puntaje de una prueba estandarizada")
    mu = st.sidebar.slider("Media μ del puntaje", 200, 800, 500, step=10)
    sigma = st.sidebar.slider("Desviación estándar σ", 10, 200, 100, step=5)
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 400)
    pdf = stats.norm(mu, sigma).pdf(x)

    ax.plot(x, pdf)
    ax.set_xlabel("Puntaje")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Normal(μ = {mu}, σ = {sigma})")
    ax.grid(True)

# --------- CASO 4: t de Student ---------
elif caso == 4:
    st.subheader("Caso 4: Proporción/media con σ desconocida en muestra pequeña")
    df = st.sidebar.slider("Grados de libertad (n - 1)", 1, 40, 9)
    x = np.linspace(-4, 4, 400)
    pdf = stats.t(df=df).pdf(x)

    ax.plot(x, pdf)
    ax.set_xlabel("t")
    ax.set_ylabel("f(t)")
    ax.set_title(f"t de Student (gl = {df})")
    ax.grid(True)

# --------- CASO 5: F (varianzas / ventas) ---------
elif caso == 5:
    st.subheader("Caso 5: Comparar la variabilidad de ventas entre dos sucursales")
    df1 = st.sidebar.slider("gl1 (numerador)", 1, 40, 5)
    df2 = st.sidebar.slider("gl2 (denominador)", 1, 80, 10)
    x = np.linspace(0, 5, 400)
    pdf = stats.f(df1, df2).pdf(x)

    ax.plot(x, pdf)
    ax.set_xlabel("F")
    ax.set_ylabel("f(F)")
    ax.set_title(f"Distribución F (gl1 = {df1}, gl2 = {df2})")
    ax.grid(True)

# --------- CASO 6: Binomial (20 intentos) ---------
elif caso == 6:
    st.subheader("Caso 6: Número de éxitos en 20 intentos (éxito/fracaso)")
    n = st.sidebar.slider("Número de intentos n", 1, 50, 20)
    p = st.sidebar.slider("Probabilidad de éxito p", 0.01, 0.99, 0.3)
    x = np.arange(0, n + 1)
    pmf = stats.binom(n, p).pmf(x)

    ax.stem(x, pmf)
    ax.set_xlabel(f"Número de éxitos en {n} intentos (X)")
    ax.set_ylabel("P(X = x)")
    ax.set_title(f"Binomial(n = {n}, p = {p:.2f})")
    ax.grid(True)

# --------- CASO 7: Exponencial (llamada call center) ---------
elif caso == 7:
    st.subheader("Caso 7: Tiempo hasta que llegue la próxima llamada al call center")
    media = st.sidebar.slider("Media del tiempo entre llamadas (minutos)", 1, 60, 3)
    x = np.linspace(0, media * 5, 400)
    pdf = stats.expon(scale=media).pdf(x)

    ax.plot(x, pdf)
    ax.set_xlabel("Minutos hasta la próxima llamada (X)")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Exponencial(media = {media} min)")
    ax.grid(True)

# --------- CASO 8: χ² (tablas categóricas) ---------
elif caso == 8:
    st.subheader("Caso 8: Relación entre género y preferencia de producto (χ²)")
    df = st.sidebar.slider("Grados de libertad χ²", 1, 40, 4)
    x = np.linspace(0, df * 4, 400)
    pdf = stats.chi2(df=df).pdf(x)

    ax.plot(x, pdf)
    ax.set_xlabel("χ²")
    ax.set_ylabel("f(χ²)")
    ax.set_title(f"Distribución χ² (gl = {df})")
    ax.grid(True)

# --------- CASO 9: Normal (altura) ---------
elif caso == 9:
    st.subheader("Caso 9: Medición de altura de personas adultas")
    mu = st.sidebar.slider("Media de altura μ (cm)", 140, 200, 170)
    sigma = st.sidebar.slider("Desviación estándar σ (cm)", 1, 30, 8)
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 400)
    pdf = stats.norm(mu, sigma).pdf(x)

    ax.plot(x, pdf)
    ax.set_xlabel("Altura (cm)")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Normal(μ = {mu}, σ = {sigma})")
    ax.grid(True)

# --------- CASO 10: F (ANOVA 3 grupos) ---------
elif caso == 10:
    st.subheader("Caso 10: Comparar medias de tres grupos (ANOVA)")
    df1 = st.sidebar.slider("gl1 = k - 1", 1, 10, 2)
    df2 = st.sidebar.slider("gl2 = N - k", 2, 200, 27)
    x = np.linspace(0, 5, 400)
    pdf = stats.f(df1, df2).pdf(x)

    ax.plot(x, pdf)
    ax.set_xlabel("F")
    ax.set_ylabel("f(F)")
    ax.set_title(f"Distribución F (ANOVA, gl1 = {df1}, gl2 = {df2})")
    ax.grid(True)

plt.tight_layout()
st.pyplot(fig)
