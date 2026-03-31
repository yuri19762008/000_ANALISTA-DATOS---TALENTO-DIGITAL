import pandas as pd
import numpy as np


def cargar_y_explorar(ruta_csv: str) -> pd.DataFrame:
    print("=== 1. CARGA Y EXPLORACIÓN DE DATOS ===")
    df = pd.read_csv(ruta_csv)

    print("\nPrimeras filas del dataset original:")
    print(df.head())

    print("\nInformación del DataFrame:")
    df.info()

    print("\nEstadísticas descriptivas (numéricas):")
    print(df.describe())

    print("\nValores nulos por columna:")
    print(df.isna().sum())

    duplicados = df.duplicated().sum()
    print(f"\nCantidad de filas duplicadas: {duplicados}")

    return df


def limpiar_y_transformar(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== 2. LIMPIEZA Y TRANSFORMACIÓN ===")
    df_limpio = df.copy()

    # Imputación numérica para 'monto' y 'tasa_interes'
    for col in ["monto", "tasa_interes"]:
        if col in df_limpio.columns:
            media = df_limpio[col].mean()
            df_limpio[col] = df_limpio[col].fillna(media)
            print(f"Imputada media en columna numérica '{col}': {media}")

    # Imputación categórica para 'tipo_transaccion' y 'segmento_cliente'
    for col in ["tipo_transaccion", "segmento_cliente"]:
        if col in df_limpio.columns:
            moda = df_limpio[col].mode()
            if not moda.empty:
                df_limpio[col] = df_limpio[col].fillna(moda[0])
                print(f"Imputada moda en columna categórica '{col}': {moda[0]}")

    # Eliminar duplicados
    antes = len(df_limpio)
    df_limpio = df_limpio.drop_duplicates()
    despues = len(df_limpio)
    print(f"\nFilas antes de eliminar duplicados: {antes}")
    print(f"Filas después de eliminar duplicados: {despues}")
    print(f"Duplicados eliminados: {antes - despues}")

    return df_limpio


def codificar_categoricas(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== 2.b CONVERSIÓN DE CATEGÓRICAS A NUMÉRICAS ===")
    df_modelo = df.copy()

    # Mapeo manual para 'tipo_transaccion'
    if "tipo_transaccion" in df_modelo.columns:
        mapa_tipo = {
            "pago": 0,
            "retiro": 1,
            "transferencia": 2,
            "deposito": 3
        }
        df_modelo["tipo_transaccion_cod"] = df_modelo["tipo_transaccion"].map(mapa_tipo)
        print("Columna 'tipo_transaccion_cod' creada mediante mapeo manual.")

    # One-hot encoding para 'segmento_cliente'
    if "segmento_cliente" in df_modelo.columns:
        dummies_segmento = pd.get_dummies(df_modelo["segmento_cliente"], prefix="segmento")
        df_modelo = pd.concat([df_modelo.drop(columns=["segmento_cliente"]), dummies_segmento], axis=1)
        print("Columnas dummies creadas para 'segmento_cliente'.")

    return df_modelo


def optimizar_y_estructurar(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== 3. OPTIMIZACIÓN Y ESTRUCTURACIÓN ===")
    df_final = df.copy()

    # Resumen por cliente
    if "id_cliente" in df_final.columns and "monto" in df_final.columns:
        resumen_cliente = (
            df_final
            .groupby("id_cliente")
            .agg(
                monto_total=("monto", "sum"),
                monto_promedio=("monto", "mean"),
                transacciones=("monto", "count")
            )
            .reset_index()
        )
        print("\nResumen por cliente (primeras filas):")
        print(resumen_cliente.head())

    # Filtro de transacciones con monto > 1000
    if "monto" in df_final.columns:
        df_montos_altos = df_final[df_final["monto"] > 1000]
        print("\nTransacciones con monto > 1000 (primeras filas):")
        print(df_montos_altos.head())

    # Renombrar columnas
    df_final = df_final.rename(columns={
        "id_cliente": "cliente_id",
        "monto": "monto_transaccion"
    })

    # Reordenar columnas principales
    columnas_deseadas = [
        col for col in
        ["cliente_id", "id_transaccion", "fecha", "monto_transaccion", "tipo_transaccion", "tasa_interes", "pais"]
        if col in df_final.columns
    ]
    otras_columnas = [c for c in df_final.columns if c not in columnas_deseadas]
    df_final = df_final[columnas_deseadas + otras_columnas]

    print("\nDataFrame final estructurado (primeras filas):")
    print(df_final.head())

    return df_final


def exportar(df_final: pd.DataFrame,
             csv_salida: str = "transacciones_limpias.csv",
             xlsx_salida: str = "transacciones_limpias.xlsx") -> None:
    print("\n=== 4. EXPORTACIÓN ===")
    df_final.to_csv(csv_salida, index=False)
    df_final.to_excel(xlsx_salida, index=False)
    print(f"Archivos exportados: {csv_salida} y {xlsx_salida}")


def main():
    ruta_csv = "transacciones_raw.csv"

    df = cargar_y_explorar(ruta_csv)

    print("\n--- EJEMPLO ANTES DE LIMPIEZA ---")
    print(df.head())

    df_limpio = limpiar_y_transformar(df)
    df_modelo = codificar_categoricas(df_limpio)
    df_final = optimizar_y_estructurar(df_modelo)

    print("\n--- EJEMPLO DESPUÉS DE TRANSFORMACIÓN ---")
    print(df_final.head())

    exportar(df_final)


if __name__ == "__main__":
    main()
