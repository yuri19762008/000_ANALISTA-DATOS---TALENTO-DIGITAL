import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# 1. Cargar CIFAR-10
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# 2. Normalizar a [0, 1]
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# 3. One-hot encoding de etiquetas (0–9)
num_clases = 10
y_train_cat = to_categorical(y_train, num_clases)
y_test_cat = to_categorical(y_test, num_clases)

# 4. Definir CNN (similar a la plus de MNIST)
model = Sequential()

# Bloque 1
model.add(Conv2D(32, (3, 3), activation="relu", padding="same",
                 input_shape=(32, 32, 3)))
model.add(Conv2D(32, (3, 3), activation="relu", padding="same"))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))

# Bloque 2
model.add(Conv2D(64, (3, 3), activation="relu", padding="same"))
model.add(Conv2D(64, (3, 3), activation="relu", padding="same"))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))

# Clasificador denso
model.add(Flatten())
model.add(Dense(512, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(num_clases, activation="softmax"))

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# 5. Entrenar
history = model.fit(
    x_train,
    y_train_cat,
    epochs=25,
    batch_size=128,
    validation_split=0.1,
    verbose=1
)

# 6. Evaluar
loss_test, acc_test = model.evaluate(x_test, y_test_cat, verbose=0)
print(f"Loss test: {loss_test:.4f} | Acc test: {acc_test:.4f}")

# 7. Mostrar una imagen de test y su predicción
clases = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck"
]

idx = 1  # puedes cambiar el índice
img = x_test[idx]

# y_test tiene forma (N,1), por eso usamos [0]
real_idx = int(y_test[idx][0])
real = clases[real_idx]

probs = model.predict(img[None, ...])
pred_idx = int(np.argmax(probs, axis=1)[0])
pred = clases[pred_idx]

plt.imshow(img)
plt.title(f"Real: {real} | Predicha: {pred}")
plt.axis("off")
plt.show()
