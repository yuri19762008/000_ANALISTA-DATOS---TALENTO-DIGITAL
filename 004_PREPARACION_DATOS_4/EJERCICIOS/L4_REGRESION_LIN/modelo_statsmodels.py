# modelo_statsmodels.py

import os
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import fetch_california_housing
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# =========================
# 0. Carpeta para guardar figuras
# =========================
FIG_DIR = "figures"
os.makedirs(FIG_DIR, exist_ok=True)

def save_current_fig(name):
    """Guarda la figura actual en la carpeta figures con el nombre dado."""
    path = os.path.join(FIG_DIR, name)
    plt.savefig(path, dpi=300, bbox_inches="tight")


# =========================
# 1. Carga del dataset
# =========================
california = fetch_california_housing(as_frame=True)
df = california.frame  # incluye todas las columnas + target

# Renombramos para que quede claro
df = df.rename(columns={"MedHouseVal": "price"})

# Variable ficticia: zona de alta densidad poblacional
population_median = df["Population"].median()
df["HighDensity"] = (df["Population"] > population_median).astype(int)

print(df.head())
print(df.describe())

# =========================
# 2. Modelo simple (solo MedInc)
# =========================
X_simple = df[["MedInc"]]
y = df["price"]

# Agregar constante para statsmodels
X_simple_const = sm.add_constant(X_simple)

modelo_simple = sm.OLS(y, X_simple_const).fit()
print("\n=== Resumen modelo simple (statsmodels) ===")
print(modelo_simple.summary())

# Predicciones y métricas
y_pred_simple = modelo_simple.predict(X_simple_const)

mae_simple = mean_absolute_error(y, y_pred_simple)
mse_simple = mean_squared_error(y, y_pred_simple)
rmse_simple = np.sqrt(mse_simple)
r2_simple = r2_score(y, y_pred_simple)

print("\nMétricas modelo simple:")
print(f"MAE  : {mae_simple:.4f}")
print(f"MSE  : {mse_simple:.4f}")
print(f"RMSE : {rmse_simple:.4f}")
print(f"R²   : {r2_simple:.4f}")

# =========================
# 3. Modelo múltiple base (MedInc, HouseAge, AveRooms)
# =========================
X_multi = df[["MedInc", "HouseAge", "AveRooms"]]
y = df["price"]

X_multi_const = sm.add_constant(X_multi)

modelo_multi = sm.OLS(y, X_multi_const).fit()
print("\n=== Resumen modelo múltiple base (statsmodels) ===")
print(modelo_multi.summary())

y_pred_multi = modelo_multi.predict(X_multi_const)

mae_multi = mean_absolute_error(y, y_pred_multi)
mse_multi = mean_squared_error(y, y_pred_multi)
rmse_multi = np.sqrt(mse_multi)
r2_multi = r2_score(y, y_pred_multi)

print("\nMétricas modelo múltiple base:")
print(f"MAE  : {mae_multi:.4f}")
print(f"MSE  : {mse_multi:.4f}")
print(f"RMSE : {rmse_multi:.4f}")
print(f"R²   : {r2_multi:.4f}")

# =========================
# 4. Modelo múltiple extendido (plus con variable ficticia)
# =========================
X_multi_ext = df[["MedInc", "HouseAge", "AveRooms", "HighDensity"]]
X_multi_ext_const = sm.add_constant(X_multi_ext)

modelo_multi_ext = sm.OLS(y, X_multi_ext_const).fit()
print("\n=== Resumen modelo múltiple extendido (statsmodels) ===")
print(modelo_multi_ext.summary())

y_pred_multi_ext = modelo_multi_ext.predict(X_multi_ext_const)

mae_multi_ext = mean_absolute_error(y, y_pred_multi_ext)
mse_multi_ext = mean_squared_error(y, y_pred_multi_ext)
rmse_multi_ext = np.sqrt(mse_multi_ext)
r2_multi_ext = r2_score(y, y_pred_multi_ext)

print("\nMétricas modelo múltiple extendido (con HighDensity):")
print(f"MAE  : {mae_multi_ext:.4f}")
print(f"MSE  : {mse_multi_ext:.4f}")
print(f"RMSE : {rmse_multi_ext:.4f}")
print(f"R²   : {r2_multi_ext:.4f}")

# =========================
# 5. Verificación de supuestos (modelo extendido)
# =========================

# Residuos del modelo múltiple extendido
residuos = modelo_multi_ext.resid
fitted = modelo_multi_ext.fittedvalues

# 5.1 Homocedasticidad: residuos vs valores ajustados
plt.figure(figsize=(6, 4))
plt.scatter(fitted, residuos, alpha=0.4)
plt.axhline(y=0, color="red", linestyle="--")
plt.xlabel("Valores ajustados")
plt.ylabel("Residuos")
plt.title("Residuos vs Valores ajustados (modelo múltiple extendido)")
plt.tight_layout()
save_current_fig("statsmodels_ext_residuos_vs_fitted.png")
plt.show()

# 5.2 Normalidad del error: QQ-plot
plt.figure()
sm.qqplot(residuos, line="45", fit=True)
plt.title("QQ-plot de residuos (modelo múltiple extendido)")
plt.tight_layout()
save_current_fig("statsmodels_ext_qqplot_residuos.png")
plt.show()

# 5.3 Multicolinealidad: VIF para modelo extendido
X_vif_ext = X_multi_ext_const.copy()

vif_data_ext = []
for i in range(1, X_vif_ext.shape[1]):  # saltamos la constante
    vif = variance_inflation_factor(X_vif_ext.values, i)
    vif_data_ext.append({"variable": X_vif_ext.columns[i], "VIF": vif})

vif_df_ext = pd.DataFrame(vif_data_ext)
print("\n=== VIF (modelo múltiple extendido) ===")
print(vif_df_ext)

# =========================
# 6. Visualización de relaciones
# =========================

# Pairplot base (sin HighDensity)
sns.pairplot(
    df[["price", "MedInc", "HouseAge", "AveRooms"]],
    diag_kind="kde"
)
plt.suptitle("Relaciones entre precio y predictores (modelo base)", y=1.02)
save_current_fig("statsmodels_pairplot_relaciones_base.png")
plt.show()

# Relación MedInc vs price coloreando por HighDensity
sns.lmplot(
    data=df,
    x="MedInc",
    y="price",
    hue="HighDensity",
    line_kws={"color": "black"}
)
plt.title("Ingreso medio vs precio por densidad (HighDensity)")
plt.tight_layout()
plt.gcf().savefig(
    os.path.join(FIG_DIR, "statsmodels_lmplot_medinc_price_highdensity.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()
