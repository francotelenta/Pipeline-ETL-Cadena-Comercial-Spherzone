# 📦 ETL de Ventas con SSIS + Python + SQL Server

En este apartado, se documenta el flujo ETL implementado con Visual Studio con un paquete **SSIS**, complementado con generación automática de ventas mediante **Python**, y organizado en un flujo **SRC → STG → DW** para garantizar calidad, integridad y trazabilidad de los datos.

Se incluyen etiquetas (A, B, C, D, E y F) para relacionar el diagrama anotado con la descripción técnica.

---

# 📘 1. Descripción General

Este proyecto implementa un **pipeline ETL completo** para procesar información comercial (ventas, productos y maestros) usando:

* **Python** para generar automáticamente ventas diarias (SRC), realizazr la exploración, análisis de calidad, validación y refinamiento de datos (STG).
* **SQL Server** como base de datos para las capas Source (SRC), Staging (STG) y Data Warehouse (DW).
* **SSIS** para ejecutar el flujo de extracción, transformación y carga.

El objetivo es automatizar la ingesta de ventas y preparar datos limpios y consistentes para reporting y análisis.

---

# 🗺️ 2. Arquitectura del ETL

A continuación la estructura conceptual del pipeline, dividida en áreas clave.

```
A → Productos
B → Maestros
C → Generación de Ventas e ingesta a capa SRC
D → Capa STG
E → Capa DW
```

Cada bloque corresponde a un *Sequence Container* o sección específica del paquete SSIS.

---

# 🟦 A. Procesamiento de Productos

Este contenedor administra tablas maestras relacionadas al catálogo de productos.

Incluye:

* Familia de Producto
* Rubro de Producto
* Tipo de Producto
* Producto

Proceso para cada entidad:

1. **Login_src** → Obtiene datos desde la fuente (CSV/ERP).
2. **Carga DW** → Inserta o actualiza en la tabla del Data Warehouse.
3. **Validación** → Revisa conteos e integridad.

Este módulo asegura que las ventas se puedan relacionar correctamente con la dimensión producto.

---

# 🟧 B. Procesamiento de Maestros

Contiene entidades base usadas en ventas:

* Cliente
* Vendedor
* Tienda
* Ubigeo

Flujo para cada maestro:

1. Registro desde SRC.
2. Carga al DW.
3. Validación.

Estas entidades deben procesarse antes del bloque de ventas para garantizar integridad en claves foráneas.

---

# 🟩 C. Generación Automática de Ventas e Ingesta a Capa SRC

Previo al ETL principal, se ejecutan dos scripts Python encargados de generar ventas diarias:

* `Generar_VentasCabecera.py`
* `Generar_VentasDetalle.py`

Ambos crean archivos diarios (cabecera y detalle), simulando transacciones reales.

Al finalizar la creación de las nuevas transacciones, estas son imputadas sin transformación a las tablas `fact_VentaCabecera` y `fact_VentaDetalle` en la BD SRC_Spherzone en SQL Server.

(Estos archivos son la entrada del flujo de ventas)

Ventajas:

* Mantener trazabilidad del dato crudo.
* Poder reejecutar el ETL si fuera necesario.

---

# 🟨 D. Transformación en STG

En esta capa se depura y valida la información:

* Conversión de tipos de datos.
* Control de nulos.
* Validación de claves foráneas (cliente, vendedor, producto, tienda).
* Integridad cabecera-detalle.

Incluye pasos de **refinamiento**, donde se aplican reglas de negocio.

---

# 🟪 E. Carga al Data Warehouse (DW)

Una vez validados y refinados los datos:

* Se insertan en `fact_VentaCabecera` y `fact_VentaDetalle` en la BD DW_Spherzone en SQL Server.
* Se realizan merge, actualizaciones y creación de registros nuevos.

Estas tablas son consumidas por sistemas de BI como Power BI.

---


# 🖼️ 3. Diagrama del ETL

A continuación se muestra la el diagrama en Visual Studio señalando cada una de las fases (A–F) del proceso ETL.


<img width="1811" height="1007" alt="diseño_paquete_etl" src="https://github.com/user-attachments/assets/f5461072-221a-4b3e-82df-4d4bf0cc8435" />


---

# 📌 4. Consideraciones Técnicas

* Se recomienda ejecutar el ETL mediante SQL Server Agent (Jobs diarios).
* Los scripts Python pueden integrarse con paquetes SSIS mediante "Execute Process Task".
* La capa STG actúa como control de calidad para evitar anomalías.
* Las validaciones finales garantizan consistencia antes de cargar el DW.

---

# 🚀 5. Próximas Mejoras

* Automatizar envíos de alertas por correo.
* Migración del ETL a Azure Data Factory o Prefect.
* Implementar pruebas unitarias para transformación de datos.


