import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# === 1. Configuración ===
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

# === 2. Conexión a SQL Server ===

engine = create_engine("mssql+pyodbc://Server/SRC_Spherzone?"
                       "driver=ODBC+Driver+17+for+SQL+"
                       "Server&trusted_connection=yes")

# === 3. Leer tablas base ===
df_VentasCabecera = pd.read_sql("SELECT * FROM Fact_VentaCabecera", engine)
df_VentasDetalle = pd.read_sql("SELECT * FROM Fact_VentaDetalle", engine)

# === 4. Conversión de tipo de dato ===
df_VentasCabecera["Fecha_Documento"] = pd.to_datetime(df_VentasCabecera["Fecha_Documento"])

fecha_inicio = datetime.today().date()    #- timedelta(days=1)  #datetime(2009,1,3).date()
fecha_fin = datetime.today().date()

# === 5. Consolidación en una sola tabla ===
df_VentasCabecera_FaltanteDetalle = df_VentasCabecera[(df_VentasCabecera["Fecha_Documento"].dt.date >= fecha_inicio) & (df_VentasCabecera["Fecha_Documento"].dt.date <= fecha_fin)][["Cod_Venta","Venta_MonNacional","Venta_MonExtranjera"]]
df_VentasDetalle_unicos = df_VentasDetalle.drop_duplicates(subset=["Venta_MonNacional","Venta_MonExtranjera"])   # Venta_MonNacion y Extranjera del Detalle (únicos)
df_VentasDetalle_unicos = df_VentasDetalle_unicos[~df_VentasDetalle_unicos["IDVenta"].isin([26913,99999])]
df_Ventas_combinacion = pd.merge(df_VentasCabecera_FaltanteDetalle, df_VentasDetalle_unicos, on=["Venta_MonNacional","Venta_MonExtranjera"], how="left")
df_New_VentasDetalle = df_Ventas_combinacion[["Cod_Venta", "CodigoProducto", "Cantidad", "Venta_MonNacional","Venta_MonExtranjera", "Descuento_MonNacional", "Descuento_MonExtranjera",
                                              "Impuesto_MonNacional", "Impuesto_MonExtranjera", "Costo_MonNacional", "Costo_MonExtranjera", "Codigo_UnidadMedida", "Codigo_UnidadMedida_Venta"]].copy()

df_New_VentasDetalle.rename(columns={"Cod_Venta": "IDVenta"}, inplace=True)

# === Impresión de duplicados (pasible a fallo) ===
#duplicados = df_New_VentasDetalle[df_New_VentasDetalle["IDVenta"].isin(df_VentasDetalle["IDVenta"])]
#print(duplicados.head())

# === Verificación de existencia previa ===
if  df_New_VentasDetalle["IDVenta"].isin(df_VentasDetalle[~df_VentasDetalle["IDVenta"].isin([26913,99999])]["IDVenta"]).any():
    print(f"[ADVERTENCIA] Los IDVenta a insertar ya se encuentran ocupados en STG_Fact_VentaDetalle.")
    print("Ejecución detenida para evitar duplicar información.")
    import sys
    sys.exit()  # Detiene completamente la ejecución del script


# === 6. Insertar en SQL por lotes ===
df_New_VentasDetalle.to_sql(
    "Fact_VentaDetalle",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=10_000
)

print(f"{len(df_New_VentasDetalle):,} detalles de venta simulados insertados.")
