import os
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


import matplotlib.pyplot as plt

# Paso 0: carpeta absoluta donde se guardarán las figuras
FIG_DIR = r"D:\000_ANALISTA_DATOS\008_MODULO_8\EJERCICIOS\figuras"
os.makedirs(FIG_DIR, exist_ok=True)

# Paso 1: crear dataset sintético de regresión
X, y = make_regression(
    n_samples=1000,
    n_features=1,
    noise=5,
    random_state=0
)

# Paso 2: dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Paso 3: escalar los datos (solo X)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Paso 4: definir el modelo secuencial
model = Sequential()
model.add(Dense(64, activation="relu", input_shape=(1,)))
model.add(Dense(32, activation="relu"))
model.add(Dense(1))  # salida lineal para regresión

# Paso 5: compilar el modelo
model.compile(
    optimizer="adam",
    loss="mean_squared_error",
    metrics=["mae"]
)

# Paso 6: entrenar el modelo
history = model.fit(
    X_train,
    y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Paso 7: evaluar en el conjunto de prueba
mse, mae = model.evaluate(X_test, y_test, verbose=0)
print(f"MSE en test: {mse:.2f}")
print(f"MAE en test: {mae:.2f}")

# Paso 8: curva de pérdida y GUARDAR en la ruta indicada
plt.figure(figsize=(8, 4))
plt.plot(history.history["loss"], label="Entrenamiento")
plt.plot(history.history["val_loss"], label="Validación")
plt.title("Pérdida durante el entrenamiento")
plt.xlabel("Épocas")
plt.ylabel("Error cuadrático medio (MSE)")
plt.legend()
plt.tight_layout()

loss_path = os.path.join(FIG_DIR, "curva_perdida.png")
plt.savefig(loss_path, dpi=150)
plt.close()

# Paso 9: reales vs predichos y GUARDAR en la ruta indicada
y_pred = model.predict(X_test).flatten()

plt.figure(figsize=(6, 6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.xlabel("Valores reales")
plt.ylabel("Predicciones")
plt.title("Regresión: reales vs predichos")
plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    "r--",
    label="Línea ideal"
)
plt.legend()
plt.tight_layout()

scatter_path = os.path.join(FIG_DIR, "reales_vs_predichos.png")
plt.savefig(scatter_path, dpi=150)
plt.close()
