# importar librerias

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, KFold, cross_val_score, ShuffleSplit, LeaveOneOut
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import numpy as np


# cargar el dataset iris

iris = load_iris()
X, y = iris.data, iris.target

# definir el modelo KNN

model = KNeighborsClassifier(n_neighbors=3)


# dividir en train y test

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# entrenar el modelo

model.fit(X_train, y_train)

# predecir en el conjunto de test

y_pred = model.predict(X_test)


# calcular la exactitud Hold out

accuracy_holdout = accuracy_score(y_test, y_pred)
print(f"Exactitud - Hold-Out: {accuracy_holdout:.2f}")

# validacion cruzada K-Fold (k = 5)

kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores_kfold = cross_val_score(model, X, y, cv=kf)
print(f"Exactitud - K-Fold: {np.mean(scores_kfold):.2f}")

# validacion cruzada Shuffle Split

ss = ShuffleSplit(n_splits=5, test_size=0.3, random_state=42)
scores_shuffle = cross_val_score(model, X, y, cv=ss)
print(f"Exactitud - Shuffle Split: {np.mean(scores_shuffle):.2f}")

# validacion cruzada Leave-One-Out (loocv)

loo = LeaveOneOut()
scores_loo = cross_val_score(model, X, y, cv=loo)
print(f"Exactitud - Leave One Out: {np.mean(scores_loo):.2f}")


## Exactitud - Hold-Out: 1.00
## Exactitud - K-Fold: 0.97
## Exactitud - Shuffle Split: 0.97
## Exactitud - Leave One Out: 0.96
