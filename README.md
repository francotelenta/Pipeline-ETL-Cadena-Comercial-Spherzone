# Pipeline-ETL-Cadena-Comercial-Spherzone
Pipeline ETL completo para actualizar datos de ventas de la Cadena Comercial Spherzone diariamente usando Python, SQL Server y SSIS. Incluye Staging, Data Warehouse, automatización con SQL Server Agent y dashboard final en Power BI.


Este proyecto implementa un pipeline ETL completo y automatizado para la actualización diaria de información de ventas de una cadena comercial. Incluye:

✔ Generación automática de datos diarios mediante Python

✔ Procesos de ingesta, transformación y carga usando SSIS

✔ Integración con SQL Server (Source → Staging → Data Warehouse)

✔ Dashboard final en Power BI

✔ Orquestación mediante SQL Server Agent

-----------------------------------------------

🔧 Tecnologías Utilizadas

- Python 3.11

- SQL Server 2021

- Integration Services (SSIS)

- SQL Server Agent

- Power BI

- Power Query

- Visual Studio 2022

-----------------------------------------------

Esquema del Pipeline:

1. Python (Imput)

2. SQL Server (Source)
      
3. Python + SQL Server + SSIS (Staging)
      
4. SQL Server (Data Warehouse)
      
5. Power Query (Auxiliar Table)
      
6. Power BI (Visualization)

-----------------------------------------------

⚙ Funcionalidades del Pipeline

1️⃣ Generación automática de ventas (Python)

- Simula ventas diarias basadas en históricos base del 2007 y 2008 (Método de suavización exponencial).

- Alimenta tablas “Source” en SQL Server.
  

2️⃣ Procesamiento ETL en SSIS

- Carga y validación en "Staging".
  
- EDA y calidad de datos.

- Transformaciones (limpieza, fechas, tipos de transacción, validación PK y FK).

- Carga al Data Warehouse (hechos y dimensiones, homologación PK y FK).
  

3️⃣ Orquestación automática

Job en SQL Server Agent ejecuta paquete de SSIS de Visual Studio. Este incluye:

- Scripts Python → Generan data simulada.

- Scripts Python + SSIS → Transforma y refina en Staging.

- SSIS → Refresca el DW

  *Adicionalmente, se incluye una tabla "Login" para la fase Staging que se actualiza cada que se orquesta el flujo.*


4️⃣ Transformación de Tabla Auxiliar de Ubigeos (PDF → Tabla → Power Query → Power BI)

- Fuente: PDF con 27 hojas.

- Procesado en Power Query.

- Concatenación y normalización.

- Integrado al modelo final de Power BI.

  
