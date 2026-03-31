# visualizaciones_tips_guardar.py
# Genera todas las figuras del desafío y las guarda en la carpeta "figures"

import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# =========================
# 0. Crear carpeta figures
# =========================
os.makedirs("figures", exist_ok=True)

# =========================
# 1. Carga del dataset
# =========================
df = sns.load_dataset("tips")

# =========================
# 2. Distribución de "tip" con histplot + KDE
# =========================
plt.figure(figsize=(8, 5))
sns.histplot(df["tip"], kde=True, bins=20, color="skyblue")
plt.title("Distribución de las propinas")
plt.xlabel("Monto de propina")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig("figures/01_hist_tip.png")
plt.close()

# =========================
# 3. Relación total_bill vs tip con jointplot (regresión)
# =========================
g = sns.jointplot(data=df, x="total_bill", y="tip", kind="reg", height=6)
g.figure.suptitle("Relación entre total_bill y tip", y=1.02)
g.figure.savefig("figures/02_joint_totalbill_tip.png")
plt.close(g.figure)

# =========================
# 4. Boxplot de tip según day
# =========================
plt.figure(figsize=(8, 5))
sns.boxplot(x="day", y="tip", data=df, palette="Set2")
plt.title("Distribución de propinas por día (Boxplot)")
plt.xlabel("Día")
plt.ylabel("Propina")
plt.tight_layout()
plt.savefig("figures/03_box_tip_day.png")
plt.close()

# =========================
# 5. Violinplot de tip según day
# =========================
plt.figure(figsize=(8, 5))
sns.violinplot(x="day", y="tip", data=df, palette="Set3")
plt.title("Distribución y densidad de propinas por día (Violinplot)")
plt.xlabel("Día")
plt.ylabel("Propina")
plt.tight_layout()
plt.savefig("figures/04_violin_tip_day.png")
plt.close()

# =========================
# 6. Countplot por género (sex)
# =========================
plt.figure(figsize=(6, 4))
sns.countplot(x="sex", data=df, palette="pastel")
plt.title("Cantidad de registros por género")
plt.xlabel("Género")
plt.ylabel("Cantidad")
plt.tight_layout()
plt.savefig("figures/05_count_sex.png")
plt.close()

# =========================
# 7. Countplot por fumador (smoker)
# =========================
plt.figure(figsize=(6, 4))
sns.countplot(x="smoker", data=df, palette="muted")
plt.title("Cantidad de fumadores vs no fumadores")
plt.xlabel("Fumador")
plt.ylabel("Cantidad")
plt.tight_layout()
plt.savefig("figures/06_count_smoker.png")
plt.close()

# =========================
# 8. Matriz de correlación con heatmap
# =========================
correlation = df.corr(numeric_only=True)

plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Matriz de correlación entre variables numéricas")
plt.tight_layout()
plt.savefig("figures/07_heatmap_corr.png")
plt.close()

# =========================
# 9. Pairplot con hue="sex"
# =========================
g = sns.pairplot(df, hue="sex", palette="Set1")
g.savefig("figures/08_pairplot_sex.png")
plt.close('all')
