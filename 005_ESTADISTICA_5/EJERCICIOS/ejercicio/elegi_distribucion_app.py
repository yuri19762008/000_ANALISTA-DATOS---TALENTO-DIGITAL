# elegi_distribucion_app.py
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as stats
import streamlit as st

st.set_page_config(page_title="Distribución", layout="centered")

st.title("Distribución")

st.markdown("""
**Paso a paso:**
1. Identifique si hay una cantidad fija de intentos o un intervalo de tiempo.  
2. Determine si los eventos son raros o tienen alta probabilidad.  
3. Asocie la distribución correcta: binomial o Poisson.  
4. Justifique su elección con base en sus características.  
5. Grafique cómo se vería la probabilidad en cada caso.
""")

casos = {
    "1) Producción defectuosa en 20 piezas (p = 0.1)": 1,
    "2) Mensajes de error por minuto (λ = 2)": 2,
    "3) Respuestas correctas al azar en 10 preguntas (p = 0.5)": 3,
}

opcion = st.selectbox("Elige el caso a analizar:", list(casos.keys()))
caso = casos[opcion]

fig, ax = plt.subplots()

# ----------------- CASO 1 -----------------
if caso == 1:
    st.subheader("Caso 1: Producción defectuosa")
    st.markdown("""
    - Ensayos fijos: 20 piezas.  
    - Cada pieza puede ser **defectuosa / no defectuosa**.  
    - Probabilidad de defecto conocida: \\(p = 0.1\\).  
    → **Distribución binomial**.
    """)

    # Permitir al usuario ajustar ligeramente p
    p = st.slider("Probabilidad de defecto p", 0.01, 0.5, 0.1)
    n = 20
    x = np.arange(0, n + 1)
    pmf = stats.binom(n, p).pmf(x)

    ax.stem(x, pmf)
    ax.set_xlabel("Número de piezas defectuosas en la muestra (X)")
    ax.set_ylabel("P(X = x)")
    ax.set_title(f"Binomial(n = {n}, p = {p:.2f})")
    ax.grid(True)

    st.markdown("""
    **Interpretación:**  
    La altura de cada “palito” indica la probabilidad de obtener exactamente ese número de piezas defectuosas en la muestra de 20.
    """)

# ----------------- CASO 2 -----------------
elif caso == 2:
    st.subheader("Caso 2: Mensajes de error por minuto")
    st.markdown("""
    - Contamos cuántos errores llegan en **un intervalo de tiempo** (1 minuto).  
    - No hay un número máximo de mensajes posible.  
    - En promedio llegan 2 errores por minuto.  
    → **Distribución de Poisson** con \\(\\lambda = 2\\).
    """)

    lam = st.slider("Tasa promedio λ (errores por minuto)", 0.5, 10.0, 2.0)
    # rango suficiente alrededor de λ
    max_x = int(lam + 5 * np.sqrt(lam)) + 1
    x = np.arange(0, max_x)
    pmf = stats.poisson(lam).pmf(x)

    ax.stem(x, pmf)
    ax.set_xlabel("Número de mensajes de error en un minuto (X)")
    ax.set_ylabel("P(X = x)")
    ax.set_title(f"Poisson(λ = {lam:.2f})")
    ax.grid(True)

    st.markdown("""
    **Interpretación:**  
    La curva muestra la probabilidad de observar 0, 1, 2, … errores en un minuto, suponiendo una tasa media constante λ.
    """)

# ----------------- CASO 3 -----------------
elif caso == 3:
    st.subheader("Caso 3: Respuestas correctas al azar")
    st.markdown("""
    - Hay **10 preguntas**, cada una con dos opciones.  
    - Se responde completamente al azar → probabilidad de acierto \\(p = 0.5\\).  
    - Interesa el número de respuestas correctas.  
    → **Distribución binomial** con \\(n = 10, p = 0.5\\).
    """)

    n = 10
    p = st.slider("Probabilidad de acertar p", 0.1, 0.9, 0.5)
    x = np.arange(0, n + 1)
    pmf = stats.binom(n, p).pmf(x)

    ax.stem(x, pmf)
    ax.set_xlabel("Número de respuestas correctas (X)")
    ax.set_ylabel("P(X = x)")
    ax.set_title(f"Binomial(n = {n}, p = {p:.2f})")
    ax.grid(True)

    st.markdown("""
    **Interpretación:**  
    La mayor probabilidad se concentra alrededor de \\(np\\) respuestas correctas, y la forma es más o menos simétrica cuando \\(p \\approx 0.5\\).
    """)

plt.tight_layout()
st.pyplot(fig)
