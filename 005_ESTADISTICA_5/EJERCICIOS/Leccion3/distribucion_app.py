# distribucion_app.py
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as stats
import streamlit as st

st.set_page_config(page_title="Distribuciones", layout="centered")

st.title("Distribuciones según el tipo de problema")

casos = {
    "1. Número de clientes (Poisson)": 1,
    "2. Tiempo hasta fallo de servidor (Exponencial)": 2,
    "3. Puntaje prueba estandarizada (Normal)": 3,
    "4. Proporción defectuosos, σ desconocida (t)": 4,
    "5. Variabilidad ventas dos sucursales (F)": 5,
    "6. Éxitos en 20 intentos (Binomial)": 6,
    "7. Tiempo hasta próxima llamada (Exponencial)": 7,
    "8. Relación género vs preferencia (χ²)": 8,
    "9. Altura adultos (Normal)": 9,
    "10. Comparar medias tres grupos (F ANOVA)": 10,
}

opcion = st.selectbox("Elige un caso:", list(casos.keys()))
caso = casos[opcion]

fig, ax = plt.subplots()

if caso == 1:
    mu = st.slider("λ (promedio clientes por hora)", 1, 30, 10)
    x = np.arange(0, mu + 20)
    pmf = stats.poisson(mu).pmf(x)
    ax.stem(x, pmf)
    ax.set_xlabel("Número de clientes en una hora")
    ax.set_ylabel("P(X = x)")
    ax.set_title(f"Poisson(λ = {mu})")

elif caso == 2:
    media = st.slider("Media de tiempo hasta fallo (horas)", 1, 24, 5)
    x = np.linspace(0, media * 5, 300)
    pdf = stats.expon(scale=media).pdf(x)
    ax.plot(x, pdf)
    ax.set_xlabel("Horas hasta el fallo")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Exponencial(media = {media} horas)")

elif caso == 3:
    mu = st.slider("Media del puntaje", 200, 800, 500, step=10)
    sigma = st.slider("Desviación estándar", 10, 200, 100, step=5)
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 300)
    pdf = stats.norm(mu, sigma).pdf(x)
    ax.plot(x, pdf)
    ax.set_xlabel("Puntaje")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Normal(μ = {mu}, σ = {sigma})")

elif caso == 4:
    df = st.slider("Grados de libertad (n - 1)", 1, 30, 9)
    x = np.linspace(-4, 4, 300)
    pdf = stats.t(df=df).pdf(x)
    ax.plot(x, pdf)
    ax.set_xlabel("t")
    ax.set_ylabel("f(t)")
    ax.set_title(f"t de Student (gl = {df})")

elif caso == 5:
    df1 = st.slider("gl1 (numerador)", 1, 30, 5)
    df2 = st.slider("gl2 (denominador)", 1, 60, 10)
    x = np.linspace(0, 5, 300)
    pdf = stats.f(df1, df2).pdf(x)
    ax.plot(x, pdf)
    ax.set_xlabel("F")
    ax.set_ylabel("f(F)")
    ax.set_title(f"Distribución F (gl1 = {df1}, gl2 = {df2})")

elif caso == 6:
    n = st.slider("Número de ensayos n", 1, 50, 20)
    p = st.slider("Probabilidad de éxito p", 0.01, 0.99, 0.3)
    x = np.arange(0, n + 1)
    pmf = stats.binom(n, p).pmf(x)
    ax.stem(x, pmf)
    ax.set_xlabel(f"Número de éxitos en {n} intentos")
    ax.set_ylabel("P(X = x)")
    ax.set_title(f"Binomial(n = {n}, p = {p:.2f})")

elif caso == 7:
    media = st.slider("Media del tiempo entre llamadas (min)", 1, 30, 3)
    x = np.linspace(0, media * 5, 300)
    pdf = stats.expon(scale=media).pdf(x)
    ax.plot(x, pdf)
    ax.set_xlabel("Minutos hasta la próxima llamada")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Exponencial(media = {media} min)")

elif caso == 8:
    df = st.slider("Grados de libertad χ²", 1, 30, 4)
    x = np.linspace(0, df * 5, 300)
    pdf = stats.chi2(df=df).pdf(x)
    ax.plot(x, pdf)
    ax.set_xlabel("χ²")
    ax.set_ylabel("f(χ²)")
    ax.set_title(f"Distribución χ² (gl = {df})")

elif caso == 9:
    mu = st.slider("Media de altura (cm)", 140, 200, 170)
    sigma = st.slider("Desviación estándar (cm)", 1, 20, 8)
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 300)
    pdf = stats.norm(mu, sigma).pdf(x)
    ax.plot(x, pdf)
    ax.set_xlabel("Altura (cm)")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Normal(μ = {mu}, σ = {sigma})")

elif caso == 10:
    df1 = st.slider("gl1 (k - 1)", 1, 10, 2)
    df2 = st.slider("gl2 (N - k)", 1, 100, 27)
    x = np.linspace(0, 5, 300)
    pdf = stats.f(df1, df2).pdf(x)
    ax.plot(x, pdf)
    ax.set_xlabel("F")
    ax.set_ylabel("f(F)")
    ax.set_title(f"Distribución F (ANOVA, gl1 = {df1}, gl2 = {df2})")

ax.grid(True)
plt.tight_layout()
st.pyplot(fig)
