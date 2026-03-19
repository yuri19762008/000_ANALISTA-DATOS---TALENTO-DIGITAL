import json

# ----- Definición de celdas -----

cells = []

def md(text):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")]
    })

def code(text):
    cells.append({
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [line + "\n" for line in text.split("\n")]
    })

# Celda 1 — Título e imports generales
md("# CNN: Optimización y Transfer Learning\n\n"
   "En este notebook trabajamos con:\n\n"
   "- Una CNN simple en MNIST.\n"
   "- Una CNN más profunda y optimizada en CIFAR-10.\n"
   "- Transfer learning con ResNet50 sobre CIFAR-10.\n")

code(
"import numpy as np\n"
"import matplotlib.pyplot as plt\n\n"
"import tensorflow as tf\n"
"from tensorflow import keras\n"
"from tensorflow.keras import layers\n\n"
"from sklearn.metrics import classification_report\n"
)

# ----- SECCIÓN 1 – MNIST -----

md("## Sección 1 — CNN simple en MNIST")

code(
"# Cargar dataset MNIST\n"
"(x_train_m, y_train_m), (x_test_m, y_test_m) = keras.datasets.mnist.load_data()\n\n"
"# Normalizar a [0, 1]\n"
"x_train_m = x_train_m.astype('float32') / 255.0\n"
"x_test_m  = x_test_m.astype('float32') / 255.0\n\n"
"# Añadir canal (grayscale)\n"
"x_train_m = x_train_m[..., None]\n"
"x_test_m  = x_test_m[..., None]\n\n"
"input_shape_m = (28, 28, 1)\n"
"num_classes_m = 10\n\n"
"print('MNIST shapes:')\n"
"print('x_train:', x_train_m.shape, 'y_train:', y_train_m.shape)\n"
"print('x_test :', x_test_m.shape, 'y_test :', y_test_m.shape)\n"
)

code(
"def make_mnist_cnn():\n"
"    model = keras.Sequential([\n"
"        layers.Conv2D(32, 3, activation='relu', input_shape=input_shape_m),\n"
"        layers.MaxPooling2D(),\n"
"        layers.Conv2D(64, 3, activation='relu'),\n"
"        layers.MaxPooling2D(),\n"
"        layers.Flatten(),\n"
"        layers.Dense(64, activation='relu'),\n"
"        layers.Dense(num_classes_m, activation='softmax'),\n"
"    ])\n"
"    return model\n\n"
"model_mnist = make_mnist_cnn()\n"
"model_mnist.compile(\n"
"    optimizer='adam',\n"
"    loss='sparse_categorical_crossentropy',\n"
"    metrics=['accuracy']\n"
")\n\n"
"history_mnist = model_mnist.fit(\n"
"    x_train_m, y_train_m,\n"
"    epochs=5,\n"
"    batch_size=64,\n"
"    validation_split=0.1,\n"
"    verbose=1,\n"
")\n"
)

code(
"# Evaluación avanzada en test (Precision, Recall, F1)\n"
"y_pred_probs_m = model_mnist.predict(x_test_m)\n"
"y_pred_m = np.argmax(y_pred_probs_m, axis=1)\n\n"
"print(classification_report(y_test_m, y_pred_m, digits=4))\n"
)

# ----- SECCIÓN 2 – CIFAR-10 CNN OPTIMIZADA -----

md("## Sección 2 — CNN más profunda y optimizada en CIFAR-10")

code(
"from tensorflow.keras.datasets import cifar10\n\n"
"(x_train, y_train), (x_test, y_test) = cifar10.load_data()\n\n"
"# Normalizar\n"
"x_train = x_train.astype('float32') / 255.0\n"
"x_test  = x_test.astype('float32') / 255.0\n\n"
"y_train = y_train.reshape(-1)\n"
"y_test  = y_test.reshape(-1)\n\n"
"from sklearn.model_selection import train_test_split\n\n"
"x_train_c, x_val_c, y_train_c, y_val_c = train_test_split(\n"
"    x_train, y_train, test_size=0.1, random_state=42, stratify=y_train\n"
")\n\n"
"input_shape = (32, 32, 3)\n"
"num_classes = 10\n\n"
"print('CIFAR-10 shapes:')\n"
"print('x_train:', x_train_c.shape, 'y_train:', y_train_c.shape)\n"
"print('x_val  :', x_val_c.shape, 'y_val  :', y_val_c.shape)\n"
"print('x_test :', x_test.shape,  'y_test :', y_test.shape)\n"
)

code(
"data_augmentation = keras.Sequential([\n"
"    layers.RandomFlip('horizontal'),\n"
"    layers.RandomRotation(0.1),\n"
"    layers.RandomZoom(0.1),\n"
"])\n"
)

code(
"def make_cifar_vgg_like():\n"
"    inputs = keras.Input(shape=input_shape)\n"
"\n"
"    x = data_augmentation(inputs)\n"
"\n"
"    # Bloque 1\n"
"    x = layers.Conv2D(32, 3, padding='same', activation='relu')(x)\n"
"    x = layers.Conv2D(32, 3, padding='same', activation='relu')(x)\n"
"    x = layers.MaxPooling2D()(x)\n"
"    x = layers.Dropout(0.25)(x)\n"
"\n"
"    # Bloque 2\n"
"    x = layers.Conv2D(64, 3, padding='same', activation='relu')(x)\n"
"    x = layers.Conv2D(64, 3, padding='same', activation='relu')(x)\n"
"    x = layers.MaxPooling2D()(x)\n"
"    x = layers.Dropout(0.25)(x)\n"
"\n"
"    # Bloque 3\n"
"    x = layers.Conv2D(128, 3, padding='same', activation='relu')(x)\n"
"    x = layers.Conv2D(128, 3, padding='same', activation='relu')(x)\n"
"    x = layers.MaxPooling2D()(x)\n"
"    x = layers.Dropout(0.25)(x)\n"
"\n"
"    x = layers.Flatten()(x)\n"
"    x = layers.Dense(256, activation='relu')(x)\n"
"    x = layers.Dropout(0.5)(x)\n"
"    outputs = layers.Dense(num_classes, activation='softmax')(x)\n"
"\n"
"    model = keras.Model(inputs, outputs)\n"
"    return model\n\n"
"model_cifar_opt = make_cifar_vgg_like()\n"
"model_cifar_opt.compile(\n"
"    optimizer=keras.optimizers.Adam(learning_rate=1e-3),\n"
"    loss='sparse_categorical_crossentropy',\n"
"    metrics=['accuracy']\n"
")\n"
)

code(
"callbacks = [\n"
"    keras.callbacks.EarlyStopping(\n"
"        monitor='val_loss',\n"
"        patience=5,\n"
"        restore_best_weights=True\n"
"    ),\n"
"    keras.callbacks.ReduceLROnPlateau(\n"
"        monitor='val_loss',\n"
"        factor=0.5,\n"
"        patience=2,\n"
"        min_lr=1e-6\n"
"    ),\n"
"]\n\n"
"history_cifar_opt = model_cifar_opt.fit(\n"
"    x_train_c, y_train_c,\n"
"    epochs=50,\n"
"    batch_size=64,\n"
"    validation_data=(x_val_c, y_val_c),\n"
"    callbacks=callbacks,\n"
"    verbose=1,\n"
")\n"
)

code(
"y_val_pred_probs = model_cifar_opt.predict(x_val_c)\n"
"y_val_pred = np.argmax(y_val_pred_probs, axis=1)\n\n"
"print('CNN VGG-like optimizada (validación):')\n"
"print(classification_report(y_val_c, y_val_pred, digits=4))\n\n"
"y_test_pred_probs = model_cifar_opt.predict(x_test)\n"
"y_test_pred = np.argmax(y_test_pred_probs, axis=1)\n\n"
"print('CNN VGG-like optimizada (test):')\n"
"print(classification_report(y_test, y_test_pred, digits=4))\n"
)

# ----- SECCIÓN 3 – TRANSFER LEARNING RESNET50 -----

md("## Sección 3 — Transfer learning con ResNet50 en CIFAR-10")

code(
"from tensorflow.keras.applications import ResNet50\n"
"from tensorflow.keras.applications.resnet50 import preprocess_input\n\n"
"base_resnet = ResNet50(\n"
"    weights='imagenet',\n"
"    include_top=False,\n"
"    pooling='avg'\n"
")\n"
"base_resnet.trainable = False\n\n"
"inputs_tl = keras.Input(shape=input_shape)\n"
"x = layers.Resizing(224, 224)(inputs_tl)\n"
"x = preprocess_input(x)\n"
"x = base_resnet(x)\n"
"x = layers.Dense(256, activation='relu')(x)\n"
"x = layers.Dropout(0.5)(x)\n"
"outputs_tl = layers.Dense(num_classes, activation='softmax')(x)\n\n"
"model_tl = keras.Model(inputs_tl, outputs_tl)\n"
"model_tl.compile(\n"
"    optimizer=keras.optimizers.Adam(learning_rate=1e-3),\n"
"    loss='sparse_categorical_crossentropy',\n"
"    metrics=['accuracy']\n"
")\n"
)

code(
"history_tl = model_tl.fit(\n"
"    x_train_c, y_train_c,\n"
"    epochs=10,\n"
"    batch_size=64,\n"
"    validation_data=(x_val_c, y_val_c),\n"
"    verbose=1,\n"
")\n\n"
"y_val_pred_probs_tl = model_tl.predict(x_val_c)\n"
"y_val_pred_tl = np.argmax(y_val_pred_probs_tl, axis=1)\n\n"
"print('Transfer learning ResNet50 (validación, solo cabeza):')\n"
"print(classification_report(y_val_c, y_val_pred_tl, digits=4))\n"
)

code(
"# Fine-tuning de las últimas capas de ResNet50\n"
"base_resnet.trainable = True\n"
"for layer in base_resnet.layers[:-20]:\n"
"    layer.trainable = False\n\n"
"model_tl.compile(\n"
"    optimizer=keras.optimizers.Adam(learning_rate=1e-5),\n"
"    loss='sparse_categorical_crossentropy',\n"
"    metrics=['accuracy']\n"
")\n\n"
"history_tl_ft = model_tl.fit(\n"
"    x_train_c, y_train_c,\n"
"    epochs=10,\n"
"    batch_size=64,\n"
"    validation_data=(x_val_c, y_val_c),\n"
"    verbose=1,\n"
")\n\n"
"y_val_pred_probs_tl_ft = model_tl.predict(x_val_c)\n"
"y_val_pred_tl_ft = np.argmax(y_val_pred_probs_tl_ft, axis=1)\n\n"
"print('Transfer learning ResNet50 (validación, fine-tuning):')\n"
"print(classification_report(y_val_c, y_val_pred_tl_ft, digits=4))\n"
)

# ----- Construcción del notebook -----

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.x"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

fname = r"d:\000_ANALISTA_DATOS\Bootcamp-main\Modulo8\Leccion4\CNN_optimizacion_y_transfer.ipynb"

with open(fname, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=2)

print("Notebook generado:", fname)
