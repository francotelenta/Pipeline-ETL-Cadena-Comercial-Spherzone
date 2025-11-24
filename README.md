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

----

**Arquitectura del pipeline**

<img width="1520" height="802" alt="arquitectura_proceso" src="https://github.com/user-attachments/assets/ad041752-677b-4f86-9925-c37355d0fb3b" />


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


----

**Dashboard de la Cadena Comercial Spherzone**

Finalmente, luego de haberse obtenido la data limpia y transformada ya disponible en el Data Warehouse, se procedió con el análisis de la misma de manera que se determinó una anomalía en el KPI de Ticket promedio. A partir de esta necesidad, es como surgió la idea de elaborar un dashboard basado en explicar el origen de este problema. Las vistas del dashboard se muestran a continuación:

**Storytelling general del Ticket promedio**

<img width="1856" height="1044" alt="dashboard_pestaña_principal" src="https://github.com/user-attachments/assets/5c18794b-bcc8-4ba1-bed2-4feddf53ab36" />

----
**Storytelling del primer origen de la caída**

<img width="1853" height="1037" alt="dashboard_pestaña_caidaTicket_N°1" src="https://github.com/user-attachments/assets/9428bd07-e574-4c1b-921e-5a40dd514b83" />

----
**Storytelling del segundo origen de la caída**

<img width="1858" height="1041" alt="dashboard_pestaña_caidaTicket_N°2" src="https://github.com/user-attachments/assets/d983da86-e7b6-473a-8b65-7537ae3c3b5c" />

-----------------------------------------------

Gracias a dicho análisis basado en data storytelling, se llegó a la conclusión que, las caídas en dicho KPI para Octubre de 2024 (valor más bajo en los últimos 10 años), no se vio influenciado por el Valor Total de la Venta, los Ingresos o el %Margen de Utilidad, si no más bien, por una caída en el volumen de ventas de determinadas famiilias de productos.
Las familias de productos que disminuyeron sus ventas en Octubre de 2024 fueron:

- Artículos para el Hogar -> Muebles para el Comedor
        
- Artículos Tecnológicos -> Parlantes y Amplificadores 
        
  
