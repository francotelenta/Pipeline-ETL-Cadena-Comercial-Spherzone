import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import calendar

# === 1. Configuración general ===
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

# === 2. Conexión a SQL Server ===
engine = create_engine("mssql+pyodbc://ServerName/SRC_Spherzone?"
                       "driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

# === 3. Leer tablas base ===
df_VentasCabecera = pd.read_sql("SELECT * FROM Fact_VentaCabecera", engine)
df_VentasCabecera["Fecha_Documento"] = pd.to_datetime(df_VentasCabecera["Fecha_Documento"]).dt.date

# === 4. Definir rango de fechas de proyección ===
fecha_inicio = datetime.today().date()  #- timedelta(days=1)   #(datetime(2009, 1, 3)).date()
fecha_fin = datetime.today().date()

# === Verificación de existencia previa ===
if  (df_VentasCabecera["Fecha_Documento"] == fecha_inicio).any() or (df_VentasCabecera["Fecha_Documento"] == fecha_fin).any() :
    print(f"[ADVERTENCIA] Ya existen registros con Fecha_Documento = {fecha_inicio} en Fact_VentaCabecera.")
    print("Ejecución detenida para evitar duplicar información.")
    import sys
    sys.exit()  # Detiene completamente la ejecución del script

# === 5. Crear rango de fechas ===
fechas = pd.date_range(start=fecha_inicio, end=fecha_fin, freq="D")


# === 5. Calcular métricas base ===
df_VentasDia = df_VentasCabecera.groupby('Fecha_Documento', as_index=False)[["Cod_Venta"]].count()
df_VentasDia["Periodo_Documento"] = pd.to_datetime(df_VentasDia["Fecha_Documento"]).dt.strftime('%Y%m')
df_VentasDia["Fecha_Documento"] = pd.to_datetime(df_VentasDia["Fecha_Documento"], errors='coerce')
df_VentasDiaxMes = df_VentasDia.groupby('Periodo_Documento', as_index=False)[["Cod_Venta"]].agg(['mean'])
df_VentasDiaxMes["Cod_Venta"] = df_VentasDiaxMes["Cod_Venta"].round()
df_VentasDiaxMes["Año"] = df_VentasDiaxMes["Periodo_Documento"].astype(str).str[:4].astype(int)
df_VentasDiaxMes["Mes"] = df_VentasDiaxMes["Periodo_Documento"].astype(str).str[4:6].astype(int)

# === 6. Determinar el último año completo y base ===
meses_por_año = df_VentasDiaxMes.groupby("Año")["Mes"].nunique()
ultimo_año_completo = meses_por_año[meses_por_año == 12].index.max()
df_filtrado = df_VentasDiaxMes[df_VentasDiaxMes["Año"] == ultimo_año_completo]
df_VentasBase = df_filtrado["Cod_Venta"].reset_index(drop=True)
ventas_base = [int(df_VentasBase.iloc[i]["mean"]) for i in range(12)]

# === 7. Funciones auxiliares ===
def calcular_incremento(df):
    """Calcula incremento mensual promedio entre los dos últimos años con datos"""
    df_pivot = df.pivot(index='Mes', columns='Año', values=('Cod_Venta', 'mean'))
    años = sorted(df_pivot.columns)
    if len(años) < 2:
        return np.zeros(12)
    inc_relativo = (df_pivot[años[-1]] - df_pivot[años[-2]]) / df_pivot[años[-2]]
    return inc_relativo.fillna(0).values

def calcular_sigma_mensual(df):
    """Calcula desviación estándar diaria promedio por mes"""
    df["Mes"] = df["Fecha_Documento"].dt.month
    sigma = df.groupby("Mes")["Cod_Venta"].std().fillna(1)
    return sigma.values




# === 8. Obtener incrementos y variabilidad histórica ===
incremento_mensual = calcular_incremento(df_VentasDiaxMes)
sigma_mensual = calcular_sigma_mensual(df_VentasDia)

# === 9. Simular ventas diarias (modelo mixto con control) ===
np.random.seed(42)
n_ventas_dia = []

for fecha in fechas:
    mes = fecha.month
    años_simulados = fecha.year - ultimo_año_completo

    # Promedio de crecimiento mensual (histórico)
    crecimiento_promedio = np.mean(incremento_mensual)

    # Aplicar un crecimiento anual moderado (ajustable con el factor 0.5)
    factor_crecimiento = 1 + (crecimiento_promedio * años_simulados * 0.5)

    # Media y sigma ajustadas
    media_mes = ventas_base[mes - 1] * factor_crecimiento
    sigma_mes = sigma_mensual[mes - 1]

    # Generar ventas diarias mediante distribución normal
    ventas_generadas = np.random.normal(loc=media_mes, scale=sigma_mes)

    # Asegurar valores positivos y enteros
    ventas_generadas = max(0, int(round(ventas_generadas)))
    n_ventas_dia.append(ventas_generadas)

    # === Actualizar la base al cierre de mes (controlado al 40%) ===
    if fecha.day == calendar.monthrange(fecha.year, fecha.month)[1]:
        ventas_base[mes - 1] = round(ventas_base[mes - 1] * 0.6 + ventas_generadas * 0.4)

# === 10. Calcular totales y replicar ventas ===
total_ventas = np.sum(n_ventas_dia)
fechas_repetidas = np.repeat(fechas, n_ventas_dia)
print(f"Promedio diario generado: {np.mean(n_ventas_dia):.2f}")
print(f"Se generarán aproximadamente {total_ventas:,} registros de ventas...")

# === 11. Generar muestras desde tabla base ===
muestras = df_VentasCabecera.sample(n=total_ventas, replace=True).reset_index(drop=True)
muestras["Fecha_Documento"] = fechas_repetidas

# === 12. Generar Cod_Venta incremental ===
max_cod_venta = df_VentasCabecera.loc[df_VentasCabecera["Cod_Venta"] != 99999, "Cod_Venta"].max()
muestras["Cod_Venta"] = np.arange(max_cod_venta + 1, max_cod_venta + 1 + total_ventas)

# === 13. Reordenar columnas ===
columnas = [
    "Cod_Venta", "Numero_Documento", "Tipo_Documento", "Correlativo",
    "Codigo_Unidad", "Codigo_Empresa", "Codigo_Tipo_Documento",
    "Codigo_Unidad_Venta", "CodigoVendedor", "Codigo_Cliente",
    "Codigo_Tipo_Facturacion", "Codigo_Almacen", "Codigo_Condicion_Pago",
    "Codigo_Tienda", "Numero_Signo", "Fecha_Documento",
    "Venta_MonNacional", "Venta_MonExtranjera"
]
df_ventas_total = muestras[columnas].copy()

# === 14. Insertar en SQL por lotes ===
df_ventas_total.to_sql(
    "Fact_VentaCabecera",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=10_000
)

print(f"{len(df_ventas_total):,} ventas simuladas insertadas entre {fecha_inicio} y {fecha_fin}.")
