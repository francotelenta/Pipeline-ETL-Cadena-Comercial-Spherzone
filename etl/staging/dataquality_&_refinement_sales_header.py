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
df_STG_VentasCabecera = pd.read_sql("SELECT * FROM STG_Fact_VentaCabecera", engineSTG)
df_DW_Vendedor = pd.read_sql("SELECT * FROM Dim_Vendedor", engineDW)
df_DW_Cliente = pd.read_sql("SELECT * FROM Dim_Cliente", engineDW)
df_DW_Tienda = pd.read_sql("SELECT * FROM Dim_Tienda", engineDW)

df_STG_VentasCabecera["Fecha_Documento"] = pd.to_datetime(df_STG_VentasCabecera["Fecha_Documento"]).dt.date


# === 4. Leer tablas de dimensiones con cuyos Primary Keys están como Foreign Keys en la tabla de análisis ===
foreign_keys = {
    "CodigoVendedor": df_DW_Vendedor["IDVendedor"],
    "Codigo_Cliente": df_DW_Cliente["CodCliente"],
    "Codigo_Tienda": df_DW_Tienda["IDTienda"]
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
            "Cardinalidad": col_data.nunique() / len(df) * 100,
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

        # Validación de llaves foráneas
        if foreign_keys is not None and col in foreign_keys.keys():
            fk_values = foreign_keys[col]
            info["FK Huerfanas"] = (~df[col].isin(fk_values)).unique().sum()

        if foreign_keys is not None and col in foreign_keys.keys():
            fk_values = foreign_keys[col]
            info["Filas c/FK Huerfanas"] = (~df[col].isin(fk_values)).sum()

        # Validación de rangos
        if ranges is not None and col in ranges.keys():
            min_val, max_val = ranges[col]
            fuera = ((df[col] < min_val) | (df[col] > max_val)).sum()
            info["Fuera de Rango"] = fuera
        else:
            info["Fuera de Rango"] = "No aplica"

        report.append(info)

    return pd.DataFrame(report)


# === 7. Refinamiento de datos ===

df_clean = df_STG_VentasCabecera.copy()
df_clean =  df_clean.drop_duplicates(subset=["Cod_Venta"])
df_clean['Codigo_Cliente'] =  df_clean['Codigo_Cliente'].fillna(1)
df_clean["Venta_MonNacional"] = df_clean["Venta_MonNacional"].abs()
df_clean["Venta_MonExtranjera"] = df_clean["Venta_MonExtranjera"].abs()
df_clean["Fecha_Documento"] = pd.to_datetime(df_clean["Fecha_Documento"]).dt.date

dq = data_quality_report(df_clean, foreign_keys=foreign_keys, ranges=ranges)
print(dq)  # Podemos insertar "df_clean" a Refined


# === 8. Importación de datos ===

df_clean.to_sql(
    "STG_Ref_Fact_VentaCabecera",
    con=engineSTG,
    if_exists="append",
    index=False,
    chunksize=10_000
)


print(f"{len(df_clean):,} ventas simuladas insertadas entre {df_clean['Fecha_Documento'].min()} y {df_clean['Fecha_Documento'].max()}.")




