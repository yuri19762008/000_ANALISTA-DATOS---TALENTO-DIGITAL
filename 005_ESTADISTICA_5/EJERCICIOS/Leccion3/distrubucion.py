# distribucion.py
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as stats

# Carpeta figures junto al script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def grafica_1_poisson():
    mu = 10
    x = np.arange(0, 25)
    pmf = stats.poisson(mu).pmf(x)

    plt.figure()
    plt.stem(x, pmf)
    plt.xlabel("Número de clientes en una hora")
    plt.ylabel("P(X = x)")
    plt.title("Caso 1: Poisson(λ = 10)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "caso1_poisson.png"))

def grafica_2_exponencial_fallo_servidor():
    media = 5
    x = np.linspace(0, 25, 300)
    pdf = stats.expon(scale=media).pdf(x)

    plt.figure()
    plt.plot(x, pdf)
    plt.xlabel("Horas hasta el fallo")
    plt.ylabel("f(x)")
    plt.title("Caso 2: Exponencial(media = 5 horas)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "caso2_exponencial_fallo.png"))

def grafica_3_normal_prueba():
    mu, sigma = 500, 100
    x = np.linspace(200, 800, 300)
    pdf = stats.norm(mu, sigma).pdf(x)

    plt.figure()
    plt.plot(x, pdf)
    plt.xlabel("Puntaje")
    plt.ylabel("f(x)")
    plt.title("Caso 3: Normal(μ = 500, σ = 100)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "caso3_normal_prueba.png"))

def grafica_4_t_piezas_defectuosas():
    df = 9
    x = np.linspace(-4, 4, 300)
    pdf = stats.t(df=df).pdf(x)

    plt.figure()
    plt.plot(x, pdf)
    plt.xlabel("t")
    plt.ylabel("f(t)")
    plt.title("Caso 4: t de Student (gl = 9)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "caso4_t_student.png"))

def grafica_5_f_variabilidad_ventas():
    df1, df2 = 5, 10
    x = np.linspace(0, 5, 300)
    pdf = stats.f(df1, df2).pdf(x)

    plt.figure()
    plt.plot(x, pdf)
    plt.xlabel("F")
    plt.ylabel("f(F)")
    plt.title("Caso 5: Distribución F (gl1 = 5, gl2 = 10)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "caso5_f_ventas.png"))

def grafica_6_binomial_exitos():
    n, p = 20, 0.3
    x = np.arange(0, n + 1)
    pmf = stats.binom(n, p).pmf(x)

    plt.figure()
    plt.stem(x, pmf)
    plt.xlabel("Número de éxitos en 20 intentos")
    plt.ylabel("P(X = x)")
    plt.title("Caso 6: Binomial(n = 20, p = 0.3)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "caso6_binomial.png"))

def grafica_7_exponencial_llamada():
    media = 3
    x = np.linspace(0, 20, 300)
    pdf = stats.expon(scale=media).pdf(x)

    plt.figure()
    plt.plot(x, pdf)
    plt.xlabel("Minutos hasta la próxima llamada")
    plt.ylabel("f(x)")
    plt.title("Caso 7: Exponencial(media = 3 minutos)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "caso7_exponencial_llamada.png"))

def grafica_8_chi_cuadrado():
    df = 4
    x = np.linspace(0, 20, 300)
    pdf = stats.chi2(df=df).pdf(x)

    plt.figure()
    plt.plot(x, pdf)
    plt.xlabel("χ²")
    plt.ylabel("f(χ²)")
    plt.title("Caso 8: Distribución χ² (gl = 4)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "caso8_chi2.png"))

def grafica_9_normal_altura():
    mu, sigma = 170, 8
    x = np.linspace(140, 200, 300)
    pdf = stats.norm(mu, sigma).pdf(x)

    plt.figure()
    plt.plot(x, pdf)
    plt.xlabel("Altura (cm)")
    plt.ylabel("f(x)")
    plt.title("Caso 9: Normal(μ = 170, σ = 8)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "caso9_normal_altura.png"))

def grafica_10_f_anova():
    df1, df2 = 2, 27
    x = np.linspace(0, 5, 300)
    pdf = stats.f(df1, df2).pdf(x)

    plt.figure()
    plt.plot(x, pdf)
    plt.xlabel("F")
    plt.ylabel("f(F)")
    plt.title("Caso 10: Distribución F (gl1 = 2, gl2 = 27)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "caso10_f_anova.png"))

def main():
    grafica_1_poisson()
    grafica_2_exponencial_fallo_servidor()
    grafica_3_normal_prueba()
    grafica_4_t_piezas_defectuosas()
    grafica_5_f_variabilidad_ventas()
    grafica_6_binomial_exitos()
    grafica_7_exponencial_llamada()
    grafica_8_chi_cuadrado()
    grafica_9_normal_altura()
    grafica_10_f_anova()
    plt.show()

if __name__ == "__main__":
    main()
