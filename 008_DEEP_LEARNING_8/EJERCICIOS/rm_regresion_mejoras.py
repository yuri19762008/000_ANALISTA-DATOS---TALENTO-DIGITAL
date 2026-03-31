import os
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras import regularizers
from tensorflow.keras.optimizers import Adam

# ================================
# 0. RUTA PARA GUARDAR FIGURAS
# ================================
FIG_DIR = r"D:\000_ANALISTA_DATOS\008_MODULO_8\EJERCICIOS\figuras"
os.makedirs(FIG_DIR, exist_ok=True)

# ================================
# 1. DATOS
# ================================
X, y = make_regression(
    n_samples=1000,
    n_features=1,
    noise=15,
    random_state=0
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Función auxiliar para entrenar y evaluar modelos
def entrenar_modelo(model, nombre, lr=0.001, epochs=50):
    optimizer = Adam(learning_rate=lr)
    model.compile(optimizer=optimizer, loss="mse", metrics=["mae"])
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=32,
        validation_split=0.2,
        verbose=0
    )
    mse, mae = model.evaluate(X_test, y_test, verbose=0)
    print(f"{nombre} -> MSE: {mse:.2f}, MAE: {mae:.2f}")

    # Guardar curva de pérdida
    plt.figure(figsize=(8, 4))
    plt.plot(history.history["loss"], label="Entrenamiento")
    plt.plot(history.history["val_loss"], label="Validación")
    plt.title(f"Pérdida - {nombre}")
    plt.xlabel("Épocas")
    plt.ylabel("MSE")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, f"curva_perdida_{nombre}.png"), dpi=150)
    plt.close()

    return mse, mae

# ================================
# 2. MODELO BASE
# ================================
model_base = Sequential()
model_base.add(Dense(64, activation="relu", input_shape=(1,)))
model_base.add(Dense(32, activation="relu"))
model_base.add(Dense(1))

mse_base, mae_base = entrenar_modelo(model_base, "base", lr=0.001, epochs=50)

# ================================
# 3. MODELO A: MÁS CAPAS + DROPOUT
# ================================
model_dropout = Sequential()
model_dropout.add(Dense(128, activation="relu", input_shape=(1,)))
model_dropout.add(Dropout(0.3))              # apaga 30% de neuronas
model_dropout.add(Dense(64, activation="relu"))
model_dropout.add(Dropout(0.3))
model_dropout.add(Dense(1))

mse_drop, mae_drop = entrenar_modelo(model_dropout, "dropout", lr=0.001, epochs=50)

# ================================
# 4. MODELO B: REGULARIZACIÓN L2 + LR MÁS BAJO
# ================================
l2_reg = regularizers.l2(0.001)

model_l2 = Sequential()
model_l2.add(Dense(64, activation="relu", input_shape=(1,),
                   kernel_regularizer=l2_reg))
model_l2.add(Dense(64, activation="relu",
                   kernel_regularizer=l2_reg))
model_l2.add(Dense(1))

mse_l2, mae_l2 = entrenar_modelo(model_l2, "l2_lr_bajo", lr=0.0005, epochs=50)

# ================================
# 5. RESUMEN EN CONSOLA
# ================================
print("\n=== RESUMEN DE MODELOS ===")
print(f"Base      -> MSE: {mse_base:.2f}, MAE: {mae_base:.2f}")
print(f"Dropout   -> MSE: {mse_drop:.2f}, MAE: {mae_drop:.2f}")
print(f"L2+LR bajo-> MSE: {mse_l2:.2f}, MAE: {mae_l2:.2f}")
