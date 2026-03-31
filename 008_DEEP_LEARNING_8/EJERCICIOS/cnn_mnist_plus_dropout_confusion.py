import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# 1. Cargar y preparar datos
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

x_train = np.expand_dims(x_train, -1)  # (N, 28, 28, 1)
x_test = np.expand_dims(x_test, -1)

num_clases = 10
y_train_cat = to_categorical(y_train, num_clases)
y_test_cat = to_categorical(y_test, num_clases)

# 2. Modelo CNN con más capas + Dropout
model = Sequential()

# Bloque 1
model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)))
model.add(Conv2D(32, (3, 3), activation="relu"))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))

# Bloque 2
model.add(Conv2D(64, (3, 3), activation="relu"))
model.add(Conv2D(64, (3, 3), activation="relu"))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))

# Clasificador denso
model.add(Flatten())
model.add(Dense(256, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(num_clases, activation="softmax"))

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    x_train,
    y_train_cat,
    epochs=8,
    batch_size=128,
    validation_split=0.1,
    verbose=1
)

loss_test, acc_test = model.evaluate(x_test, y_test_cat, verbose=0)
print(f"Loss test: {loss_test:.4f} | Acc test: {acc_test:.4f}")

# 3. Matriz de confusión
y_probs = model.predict(x_test)
y_pred = np.argmax(y_probs, axis=1)

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=np.arange(10))
disp.plot(cmap="Blues", values_format="d")
plt.title("Matriz de confusión - MNIST CNN")
plt.tight_layout()
plt.show()
