theme: jekyll-theme-Slate
# Pipeline ETL — Cadena Comercial Spherzone

Pipeline ETL completo y automatizado para la actualización diaria de datos de ventas de la Cadena Comercial Spherzone, utilizando Python, SQL Server, SSIS y visualización final en Power BI.
El proyecto sigue una arquitectura Source → Staging → Data Warehouse y concluye con un análisis de anomalías mediante Data Storytelling.

----

**🧩 Descripción General**

Este proyecto implementa un pipeline de datos de punta a punta:

✔ Generación automática de ventas simuladas con Python

✔ Ingesta, limpieza, validación y transformación en SSIS

✔ Carga optimizada a Staging y DW en SQL Server

✔ Orquestación diaria con SQL Server Agent

✔ Normalización auxiliar (PDF → Tabla → Power Query)

✔ Dashboard analítico en Power BI basado en anomalías del Ticket Promedio

El flujo está diseñado para ejecutarse de forma automática, auditada y escalable.

**🛠 Tecnologías Utilizadas**

- Python 3.11

- SQL Server 2021

- SQL Server Agent

- Integration Services (SSIS) – Visual Studio 2022

- Power BI

- Power Query

- Pandas / NumPy / Matplotlib

----

**🏗 Arquitectura del Pipeline**

- Generación de datos (Python → SQL Server Source)

- Ingesta a Staging (SSIS + SQL + Python)

- Limpieza y transformaciones

- Carga final al DW (SSIS)

- Procesos auxiliares (Ubigeo PDF → Tabla → Power Query)

- Dashboard en Power BI

<br> <img width="1520" height="802" alt="arquitectura_proceso" src="https://github.com/user-attachments/assets/ad041752-677b-4f86-9925-c37355d0fb3b" />

----

⚙️ Funcionalidades del Pipeline

1️⃣ Generación automática de ventas (Python)

- Simulación de ventas usando suavización exponencial basada en históricos 2007–2008.

- Inserción directa en tablas Source de SQL Server.

2️⃣ Proceso ETL en SSIS (Staging)

- Validación de integridad de datos (PK, FK, tipos, fechas).

- Limpieza de inconsistencias.

- Homologación de catálogos y normalización.

- Auditoría por tabla de “Login” en Staging.

3️⃣ Carga al Data Warehouse

- Creación y mantenimiento de dimensiones y hechos.

- Aplicación de modelos relacionales y surrogates keys.

- Carga incremental optimizada.

4️⃣ Orquestación automática (SQL Server Agent)

- Ejecución diaria del paquete SSIS

- Llamado interno a scripts Python

- Monitorización por tabla de control

5️⃣ Normalización de Ubigeos (PDF → Tabla → PQ)

- PDF original con 27 páginas

- Transformación y limpieza en Power Query

- Integración con el modelo de Power BI

----

📊 Dashboard Analítico — Ticket Promedio

Tras procesar el Data Warehouse, se detectó una anomalía significativa:
Octubre 2024 mostró el Ticket Promedio más bajo de los últimos 10 años.

La investigación se centró en explicar el origen de esta caída mediante:

- Tendencias anuales

- Análisis YoY

- Ranking histórico

- Variabilidad por tienda, cliente, vendedor y producto

- Boxplots por Familias y Tipos de Producto
----

## ❄️Modelo Snowflake en Power BI
<img width="1821" height="1080" alt="modelo_datos" src="https://github.com/user-attachments/assets/c9329891-8e10-4dca-a24b-7bd198727f47" />


## Panel de Visualización
**📌 Vista principal (Storytelling General)**
 
<img width="1856" height="1044" alt="dashboard_pestaña_principal" src="https://github.com/user-attachments/assets/5c18794b-bcc8-4ba1-bed2-4feddf53ab36" />

#
**📌 Origen de la caída — Vista 1**
 
<img width="1853" height="1037" alt="dashboard_pestaña_caidaTicket_N°1" src="https://github.com/user-attachments/assets/9428bd07-e574-4c1b-921e-5a40dd514b83" />

#
**📌 Origen de la caída — Vista 2**
 
<img width="1858" height="1041" alt="dashboard_pestaña_caidaTicket_N°2" src="https://github.com/user-attachments/assets/d983da86-e7b6-473a-8b65-7537ae3c3b5c" />

----

**🧠 Conclusiones del Análisis**

El descenso del Ticket Promedio (Octubre 2024) NO estuvo explicado por:

❌ Valor Total de Venta

❌ Ingresos

❌ Margen de Utilidad

El origen real fue:

**📉 Caída en el volumen de ventas de familias específicas de productos**

Las familias afectadas fueron:

**1. Artículos para el Hogar → Muebles para el Comedor**

**2. Artículos Tecnológicos → Parlantes y Amplificadores**

Estas categorías presentaron:

- Mayor variabilidad histórica

- Caídas marcadas en Octubre 2024

- Alto peso relativo en el mix de ventas 

----

📬 Contacto

Si deseas más detalles o revisar el código fuente, puedes explorar las carpetas del repositorio o contactarme por estos medios:
- Correo: franco.telenta@gmail.com
- LinkedIn: linkedin.com/in/franco-telenta-chavez.

----



<details>
<summary>🔒 <b>Ver Licencia de Propiedad Intelectual y Derechos de Autor (© 2025)</b></summary>
<br>

Este proyecto, que incluye código fuente, scripts de bases de datos, lógica de simulación, arquitecturas ETL (SSIS), reportes de Power BI y documentación asociada, ha sido desarrollado de forma independiente por el autor como portafolio profesional y demostración de competencias técnicas en Ingeniería de Datos y Analítica de Negocios.

<b>1. PROHIBICIÓN DE COPIA Y DISTRIBUCIÓN:</b> Queda estrictamente prohibida la copia, reproducción, distribución, modificación, reventa o uso total o parcial de este material para fines comerciales, laborales, educativos o presentaciones públicas ajenas al autor sin su consentimiento explícito y por escrito.

<b>2. FINES DE EVALUACIÓN:</b> Este repositorio se expone públicamente única y exclusivamente con fines de evaluación profesional (reclutadores, gerentes de contratación y profesionales de la industria) para validar las capacidades técnicas y de resolución de problemas del autor.

El registro histórico de contribuciones (commits) de GitHub sirve como prueba legal y trazable de la fecha de creación y autoría original de este proyecto ante cualquier intento de plagio comercial o personal.

</details>


  
