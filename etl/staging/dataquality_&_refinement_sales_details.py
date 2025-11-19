import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# === 1. Configuración general ===
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

# === 2. Conexión a SQL Server ===
engineSTG = create_engine("mssql+pyodbc://ServerName/STG_Spherzone?"
                        "driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

engineDW = create_engine("mssql+pyodbc://ServerName/DW_Spherzone?"
                        "driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

# === 3. Leer tablas base ===
df_STG_VentasDetalle = pd.read_sql("SELECT * FROM STG_Fact_VentaDetalle", engineSTG)
df_STG_VentasCabecera = pd.read_sql("SELECT * FROM STG_Fact_VentaCabecera", engineSTG)
df_DW_Producto = pd.read_sql("SELECT * FROM Dim_Producto", engineDW)


# === 4. Leer tablas de dimensiones con cuyos Primary Keys están como Foreign Keys en la tabla de análisis ===
foreign_keys = {
    "IDVenta": df_STG_VentasCabecera["Cod_Venta"],
    "CodigoProducto": df_DW_Producto["IDProducto"]
}

# === 5. Establecer los rangos que tendrán los campos de métricas (Montos de Ventas) ===

ranges = {
    "Venta_MonNacional": (0, 15000),
    "Venta_MonExtranjera": (0, 9000),
}

# === Opc. Establecer los rangos a partir de los valores actuales ===
'''
def get_recommended_ranges(df, cols=None):
    ranges = {}
    if cols is None:
        cols = df.select_dtypes(include='number').columns

    for col in cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        ranges[col] = (
            max(0, Q1 - 1.5 * IQR),
            Q3 + 1.5 * IQR
        )
    return ranges

ranges = get_recommended_ranges(df_STG_VentasCabecera)
print(ranges)
'''

# === 6. Definir función de limpieza de datos ===
def data_quality_report(df, foreign_keys=None, ranges=None):
    """
    Genera un reporte completo de calidad de datos.

    Parámetros:
    -----------
    df : DataFrame
    foreign_keys : dict opcional.
        Ejemplo: {"Cod_Cliente": clientes_df["Cod_Cliente"],
                  "Cod_Tienda": tiendas_df["Cod_Tienda"]}
    ranges : dict opcional.
        Ejemplo: {"Venta_MonNacional": (0, 100000), "Cantidad": (1, 2000)}

    Retorna:
    --------
    DataFrame resumen
    """
    report = []

    for col in df.columns:

        col_data = df[col]

        info = {
            "Columna": col,
            "Tipo": col_data.dtype,
            "TotalValores": col_data.count(),
            "Valores Únicos": col_data.nunique(),
            "Cardinalidad": (col_data.nunique() / len(df)) * 100,
            "Duplicados": df.duplicated(subset=[col]).sum(),
            "Nulos (%)": col_data.isna().mean() * 100,
        }
        # Valores Negativos (-)
        if np.issubdtype(col_data.dtype, np.number):
            info["Negativos (%)"] = ((col_data < 0).sum() / len(col_data)) * 100
        else:
            info["Negativos (%)"] = "No aplica"

        # Outliers solo para columnas numéricas
        if np.issubdtype(col_data.dtype, np.number):
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            low = max(0, Q1 - 1.5 * IQR)
            info["Limit Inf. Outlier"] = low
        else:
            info["Limit Inf. Outlier"] = "No aplica"

        if np.issubdtype(col_data.dtype, np.number):
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            high = Q3 + 1.5 * IQR
            info["Limit Sup. Outlier"] = high
        else:
            info["Limit Sup. Outlier"] = "No aplica"

        if np.issubdtype(col_data.dtype, np.number):
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            low = Q1 - 1.5 * IQR
            high = Q3 + 1.5 * IQR
            outliers = ((col_data < low) | (col_data > high)).sum()
            info["Outliers"] = outliers
        else:
            info["Outliers"] = "No aplica"

        # Validación de rangos
        if ranges is not None and col in ranges.keys():
            min_val, max_val = ranges[col]
            fuera = ((df[col] < min_val) | (df[col] > max_val)).sum()
            info["Fuera de Rango"] = fuera
        else:
            info["Fuera de Rango"] = "No aplica"

        # Validación de llaves foráneas
        if foreign_keys is not None and col in foreign_keys.keys():
            fk_values = foreign_keys[col]
            info["FK Huerfanas"] = (~df[col].isin(fk_values)).unique().sum()

        if foreign_keys is not None and col in foreign_keys.keys():
            fk_values = foreign_keys[col]
            info["Filas c/FK Huerfanas"] = (~df[col].isin(fk_values)).sum()

        report.append(info)

    return pd.DataFrame(report)

# === 7. Refinamiento de datos ===

df_clean = df_STG_VentasDetalle.copy()
df_clean = df_clean.drop_duplicates(subset=["IDVenta"])
df_clean = df_clean.dropna(subset=["CodigoProducto"])
df_clean = df_clean.dropna(subset=["Cantidad"])
df_clean["Cantidad"] = df_clean["Cantidad"].abs()
df_clean["Venta_MonNacional"] = df_clean["Venta_MonNacional"].abs()
df_clean["Venta_MonExtranjera"] = df_clean["Venta_MonExtranjera"].abs()
df_clean = df_clean.dropna(subset=["Impuesto_MonNacional"])
df_clean["Impuesto_MonNacional"] = df_clean["Impuesto_MonNacional"].abs()
df_clean = df_clean.dropna(subset=["Impuesto_MonExtranjera"])
df_clean["Impuesto_MonExtranjera"] = df_clean["Impuesto_MonExtranjera"].abs()
df_clean = df_clean.dropna(subset=["Costo_MonNacional"])
df_clean = df_clean.dropna(subset=["Costo_MonExtranjera"])


dq = data_quality_report(df_clean, foreign_keys=foreign_keys, ranges=ranges)
print(dq)


# === 8. Importación de datos ===

df_clean.to_sql(
    "STG_Ref_Fact_VentaDetalle",
    con=engineSTG,
    if_exists="append",
    index=False,
    chunksize=10_000
)

print(f"{len(df_clean):,} detalles de venta simuladas insertados.")
