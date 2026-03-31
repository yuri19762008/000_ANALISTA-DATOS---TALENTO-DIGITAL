import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# 1. Cargar dataset MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 2. Normalizar imágenes y agregar canal (28, 28, 1)
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

x_train = np.expand_dims(x_train, -1)  # (N, 28, 28, 1)
x_test = np.expand_dims(x_test, -1)

# 3. One-hot encoding de las etiquetas (0–9)
num_clases = 10
y_train_cat = to_categorical(y_train, num_clases)
y_test_cat = to_categorical(y_test, num_clases)

# 4. Definir la CNN
model = Sequential()

# Conv2D + ReLU + MaxPooling (bloque 1)
model.add(
    Conv2D(
        filters=32,
        kernel_size=(3, 3),
        activation="relu",
        input_shape=(28, 28, 1)
    )
)
model.add(MaxPooling2D(pool_size=(2, 2)))

# Conv2D + ReLU + MaxPooling (bloque 2)
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Flatten + capa totalmente conectada
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dense(num_clases, activation="softmax"))  # salida 10 clases

# 5. Compilar modelo
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# 6. Entrenar modelo
history = model.fit(
    x_train,
    y_train_cat,
    epochs=5,
    batch_size=128,
    validation_split=0.1,
    verbose=1
)

# 7. Evaluar en test
loss_test, acc_test = model.evaluate(x_test, y_test_cat, verbose=0)
print(f"Loss en test: {loss_test:.4f}")
print(f"Accuracy en test: {acc_test:.4f}")

# 8. Mostrar una predicción sobre una imagen real del test set
idx = 1  # puedes cambiar el índice para ver otras imágenes
imagen = x_test[idx]
etiqueta_real = y_test[idx]

# Preparar batch de tamaño 1
imagen_batch = np.expand_dims(imagen, axis=0)
probs = model.predict(imagen_batch)
prediccion = np.argmax(probs, axis=1)[0]

plt.imshow(imagen.squeeze(), cmap="gray")
plt.title(f"Real: {etiqueta_real} | Predicha: {prediccion}")
plt.axis("off")
plt.show()
