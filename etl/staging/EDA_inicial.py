import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import calendar
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# === 1. Configuración general ===
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

# === 2. Conexión a SQL Server ===
engineSTG = create_engine("mssql+pyodbc://ServerName/STG_Spherzone?"
                       "driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

# === 3. Leer tablas base ===
df_VentasCabecera = pd.read_sql("SELECT * FROM STG_Fact_VentaCabecera", engineSTG)
df_VentasCabecera["Fecha_Documento"] = pd.to_datetime(df_VentasCabecera["Fecha_Documento"]).dt.date

def eda_preliminar(df):
    #Explora rápidamente el dataset: muestra muestra aleatoria, info general, nulos, duplicados y frecuencia de valores categóricos.
    print('Muestra aleatoria.')
    print(df.sample(10))
    print("-----------------")
    print('Detalles por columna')
    print(df.info())
    print("-----------------")
    print('% de Nulos')
    print(round(df.isna().sum() / df.shape[0] * 100, 2))
    print("-----------------")
    print('Filas Duplicadas')
    print(df.duplicated().sum())             #Cuenta si hay filas completas repetidas
    print("-----------------")
    print('Frecuencia de Valores Únicos')
    for col in df.select_dtypes(include='O').columns:     #Selecciona todas las columnas con tipo 'O' (Objeto) = (Fechas y Cadenas de texto)
        print(df[col].value_counts())                     #Hace un recuento por cada valor único para ver su frecuencia de repetición
        print("---------------------")

eda_preliminar(df_VentasCabecera)



def subplot_col_cat(df):
    #Muestra gráficos de barras para todas las columnas categóricas detectadas automáticamente.
    col_cat = df.select_dtypes(include=['object','category']).columns

    if len(col_cat) == 0:
        print("No hay columnas categóricas")
        return

    num_cols = len(col_cat)
    num_filas = (num_cols + 2) // 3      # Filas dentro de la pizarra al mostrar los gráficos

    fig, axes = plt.subplots(num_filas, 3, figsize=(15, num_filas * 5))
    axes = axes.flatten()

    for i, col in enumerate(col_cat):
        sns.countplot(data=df, x=col, ax=axes[i], palette="tab10")
        axes[i].set_title(f'Distribución de {col}')
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('Frecuencia')
        axes[i].tick_params(axis='x', rotation=90)

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()        # Evita superposición de gráficos
    plt.show()


subplot_col_cat(df_VentasCabecera)



def subplot_col_num(df):
    # Detectar columnas numéricas automáticamente
    cols = df.select_dtypes(include=['int', 'float']).columns.tolist()

    if not cols:
        print("No se encontraron columnas numéricas en el DataFrame.")
        return

    #Grafica histogramas y boxplots para columnas numéricas.
    num_graph = len(cols)           # Cantidad de columnas numéricas
    num_rows = num_graph            # Cada columna ocupa una fila
    # num_rows = (num_graph + 2) // 2   # Cantidad de filas en el panel de dibujo

    fig, axes = plt.subplots(num_graph, 2, figsize=(15, num_rows*1))   # Crea la grilla en donde irán los gráficos

    # Si solo hay una columna, axes dejará de ser una matriz → normalizamos
    if num_graph == 1:
        axes = np.array([axes])

    for i, c in enumerate(cols):                  # i => indice (posición de la columna), c => nombre de la columna
        sns.histplot(data=df, x=c, ax=axes[i,0], bins=200)
        axes[i,0].set_title(f'Distribución de {c}')
        axes[i,0].set_xlabel(c)
        axes[i,0].set_ylabel('Frecuencia')

        sns.boxplot(data=df, x=c, ax=axes[i,1])
        axes[i,1].set_title(f'Boxplot de {c}')

    plt.tight_layout()
    plt.show()

subplot_col_num(df_VentasCabecera)
