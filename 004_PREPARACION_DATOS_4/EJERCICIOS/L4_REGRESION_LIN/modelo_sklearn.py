# modelo_sklearn.py

import os
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

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
df = california.frame
df = df.rename(columns={"MedHouseVal": "price"})

# Variable ficticia: zona de alta densidad poblacional
population_median = df["Population"].median()
df["HighDensity"] = (df["Population"] > population_median).astype(int)

print(df.head())
print(df.describe())

# =========================
# 2. Modelo simple con sklearn (solo MedInc)
# =========================
X_simple = df[["MedInc"]]
y = df["price"]

modelo_simple = LinearRegression()
modelo_simple.fit(X_simple, y)

y_pred_simple = modelo_simple.predict(X_simple)

mae_simple = mean_absolute_error(y, y_pred_simple)
mse_simple = mean_squared_error(y, y_pred_simple)
rmse_simple = np.sqrt(mse_simple)
r2_simple = r2_score(y, y_pred_simple)

print("\n=== Modelo simple (sklearn) ===")
print(f"Intercepto: {modelo_simple.intercept_:.4f}")
print(f"Coeficiente MedInc: {modelo_simple.coef_[0]:.4f}")
print("Métricas:")
print(f"MAE  : {mae_simple:.4f}")
print(f"MSE  : {mse_simple:.4f}")
print(f"RMSE : {rmse_simple:.4f}")
print(f"R²   : {r2_simple:.4f}")

# =========================
# 3. Modelo múltiple base con sklearn (MedInc, HouseAge, AveRooms)
# =========================
X_multi = df[["MedInc", "HouseAge", "AveRooms"]]
y = df["price"]

modelo_multi = LinearRegression()
modelo_multi.fit(X_multi, y)

y_pred_multi = modelo_multi.predict(X_multi)

mae_multi = mean_absolute_error(y, y_pred_multi)
mse_multi = mean_squared_error(y, y_pred_multi)
rmse_multi = np.sqrt(mse_multi)
r2_multi = r2_score(y, y_pred_multi)

print("\n=== Modelo múltiple base (sklearn) ===")
print(f"Intercepto: {modelo_multi.intercept_:.4f}")
print("Coeficientes:")
for nombre, coef in zip(X_multi.columns, modelo_multi.coef_):
    print(f"  {nombre}: {coef:.4f}")

print("Métricas:")
print(f"MAE  : {mae_multi:.4f}")
print(f"MSE  : {mse_multi:.4f}")
print(f"RMSE : {rmse_multi:.4f}")
print(f"R²   : {r2_multi:.4f}")

# =========================
# 4. Modelo múltiple extendido (plus con HighDensity)
# =========================
X_multi_ext = df[["MedInc", "HouseAge", "AveRooms", "HighDensity"]]

modelo_multi_ext = LinearRegression()
modelo_multi_ext.fit(X_multi_ext, y)

y_pred_multi_ext = modelo_multi_ext.predict(X_multi_ext)

mae_multi_ext = mean_absolute_error(y, y_pred_multi_ext)
mse_multi_ext = mean_squared_error(y, y_pred_multi_ext)
rmse_multi_ext = np.sqrt(mse_multi_ext)
r2_multi_ext = r2_score(y, y_pred_multi_ext)

print("\n=== Modelo múltiple extendido (sklearn, con HighDensity) ===")
print(f"Intercepto: {modelo_multi_ext.intercept_:.4f}")
print("Coeficientes:")
for nombre, coef in zip(X_multi_ext.columns, modelo_multi_ext.coef_):
    print(f"  {nombre}: {coef:.4f}")

print("Métricas:")
print(f"MAE  : {mae_multi_ext:.4f}")
print(f"MSE  : {mse_multi_ext:.4f}")
print(f"RMSE : {rmse_multi_ext:.4f}")
print(f"R²   : {r2_multi_ext:.4f}")

# =========================
# 5. Comparación visual simple vs múltiple (predicciones)
# =========================

df_compare = pd.DataFrame({
    "y_real": y,
    "y_pred_simple": y_pred_simple,
    "y_pred_multi": y_pred_multi,
    "y_pred_multi_ext": y_pred_multi_ext
})

print("\n=== Primeras filas comparación real vs predicciones ===")
print(df_compare.head())

# Visual: real vs predicción múltiple base
plt.figure(figsize=(6, 6))
plt.scatter(y, y_pred_multi, alpha=0.4, label="Predicción múltiple base")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--", label="Línea ideal")
plt.xlabel("Precio real")
plt.ylabel("Precio predicho (múltiple base)")
plt.title("Real vs predicho - modelo múltiple base (sklearn)")
plt.legend()
plt.tight_layout()
save_current_fig("sklearn_real_vs_pred_multi_base.png")
plt.show()

# Visual: real vs predicción múltiple extendido
plt.figure(figsize=(6, 6))
plt.scatter(y, y_pred_multi_ext, alpha=0.4, label="Predicción múltiple extendido")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--", label="Línea ideal")
plt.xlabel("Precio real")
plt.ylabel("Precio predicho (múltiple extendido)")
plt.title("Real vs predicho - modelo múltiple extendido (sklearn)")
plt.legend()
plt.tight_layout()
save_current_fig("sklearn_real_vs_pred_multi_ext.png")
plt.show()

# Visual: real vs predicción simple
plt.figure(figsize=(6, 6))
plt.scatter(y, y_pred_simple, alpha=0.4, label="Predicción simple")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--", label="Línea ideal")
plt.xlabel("Precio real")
plt.ylabel("Precio predicho (simple)")
plt.title("Real vs predicho - modelo simple (sklearn)")
plt.legend()
plt.tight_layout()
save_current_fig("sklearn_real_vs_pred_simple.png")
plt.show()

# =========================
# 6. Visual extra: MedInc vs price por HighDensity
# =========================
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
    os.path.join(FIG_DIR, "sklearn_lmplot_medinc_price_highdensity.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.show()
