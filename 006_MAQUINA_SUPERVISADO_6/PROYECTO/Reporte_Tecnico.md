##  Borrador de reporte técnico

### 1. Objetivo de negocio

La empresa de e-commerce desea anticipar el monto de venta por pedido para personalizar campañas, gestionar stock y estimar ingresos esperados por cliente. El proyecto construye un modelo de **regresión supervisada** que predice `total_sales` a partir de datos de clientes, productos y logística.

### 2. Datos y preparación

Se utiliza el dataset `amazon_sales_dataset.csv` con 10.000 registros y 23 columnas, incluyendo fechas de orden, envío y entrega; atributos de cliente (país, estado, ciudad), producto (categoría, subcategoría, marca) y variables numéricas como cantidad, precio unitario, descuento, costo de envío y `total_sales`.
Se crean dos variables derivadas: `shipping_delay_days` (días entre orden y envío) y `delivery_delay_days` (días entre envío y entrega). Se imputan nulos con mediana/moda, se escalan numéricas con `StandardScaler` y se codifican categóricas mediante `OneHotEncoder` dentro de un `ColumnTransformer` integrado en los pipelines.

### 3. Estrategia de modelado

Se parte de un modelo base de regresión lineal simple para establecer una línea base de desempeño, evaluado con errores de entrenamiento, prueba y validación cruzada K-Fold. Luego se entrenan modelos de regresión lineal con preprocesamiento completo, regresión polinomial (grado 2) y modelos regularizados (Ridge con `GridSearchCV`). Finalmente se implementa un modelo avanzado de ensamble con `GradientBoostingRegressor`, también optimizado mediante grilla de hiperparámetros.

### 4. Evaluación de desempeño

Para cada modelo se calculan MAE, MSE, RMSE y R² sobre el conjunto de prueba, consolidando los resultados en una tabla comparativa. Esto permite observar la reducción progresiva del error al pasar de la regresión lineal simple a los modelos regularizados y al boosting. El modelo de Gradient Boosting optimizado logra el menor RMSE y un R² más alto, mostrando mejor capacidad de generalización sobre datos no vistos.

### 5. Modelo final y valor para el negocio

Se selecciona como modelo final el `GradientBoostingRegressor` optimizado, por su menor error y estabilidad en validación cruzada, manteniendo un balance razonable entre complejidad y interpretabilidad (a través de importancias de variables). Este modelo permite estimar el gasto esperado por pedido y podría integrarse en un sistema de recomendación o en el motor de campañas para definir descuentos personalizados, límites de crédito o prioridades de stock para clientes de alto valor.

### 6. Limitaciones y trabajo futuro

El modelo depende de la calidad del histórico: errores en las fechas o en los montos pueden afectar el ajuste. No se han incluido aún variables de comportamiento en tiempo real (clics, tiempo en página), que podrían enriquecer la capacidad predictiva. Como trabajo futuro se propone incorporar más fuentes de datos, probar otros métodos de boosting (XGBoost, LightGBM), monitorear el rendimiento del modelo en producción y establecer un esquema de reentrenamiento periódico para adaptarse a cambios en patrones de compra.