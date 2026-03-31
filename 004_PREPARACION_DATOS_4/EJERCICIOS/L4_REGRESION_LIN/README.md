## Conclusiones

### 1. Modelo simple vs. modelo múltiple

- El modelo simple con solo `MedInc` captura una parte importante de la variación del precio, pero deja una proporción considerable sin explicar.  
- El modelo múltiple con `MedInc`, `HouseAge` y `AveRooms` mejora las métricas (aumenta R² y disminuyen los errores) al incorporar más información relevante de las viviendas.  
- Esto muestra que, cuando las variables adicionales tienen relación con la variable objetivo, el modelo múltiple resulta más informativo y útil que el modelo simple.

### 2. Importancia de las variables

- `MedInc` aparece como una de las variables más relevantes, con coeficiente significativo, lo que confirma que el ingreso medio de la zona está fuertemente asociado al precio de la vivienda.  
- `HouseAge` y `AveRooms` también aportan poder explicativo, aunque su impacto puede ser menor o depender de la combinación con otras variables.  
- La variable ficticia `HighDensity` (basada en la densidad de población) permite capturar diferencias sistemáticas entre zonas más y menos pobladas, añadiendo matices al modelo.

### 3. Supuestos del modelo

- El gráfico de residuos vs. valores ajustados no muestra patrones claros, lo que sugiere una homocedasticidad razonable (varianza aproximadamente constante de los errores).  
- El QQ‑plot de residuos indica que la distribución de los errores es aproximadamente normal, lo que respalda el uso de inferencia basada en p‑valores y otros intervalos.  
- Los valores de VIF no presentan niveles extremos, por lo que no se detecta multicolinealidad severa entre las variables consideradas, permitiendo interpretar los coeficientes con mayor confianza.

### 4. Efecto de la variable ficticia (plus)

- Al añadir `HighDensity`, se observa una ligera mejora en R² y una reducción en métricas de error (MAE, MSE, RMSE), lo que indica que la segmentación por densidad de población ayuda a explicar mejor el precio.  
- Si el coeficiente asociado a `HighDensity` resulta significativo, puede interpretarse que, manteniendo constantes el ingreso, la edad de la vivienda y el número de habitaciones, las zonas de alta densidad presentan un patrón de precios diferente.

### 5. Limitaciones y posibles mejoras

- Aunque el modelo explica una parte significativa de la variabilidad del precio, sigue habiendo factores no capturados, como la ubicación geográfica detallada, la calidad de la construcción o la disponibilidad de servicios.  
- Incluir nuevas variables o considerar transformaciones (no linealidades, interacciones) podría mejorar el ajuste, pero también aumenta la complejidad del modelo y la posibilidad de sobreajuste, por lo que siempre es necesario revisar nuevamente métricas y supuestos.
