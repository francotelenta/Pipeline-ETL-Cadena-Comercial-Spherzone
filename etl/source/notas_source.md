**TABLAS UTILIZADAS EN _DATA SOURCE_**

_Dimensiones_
- Dim_Producto
- Dim_Familia_Producto
- Dim_Tipo_Producto
- Dim_Rubro_Producto
- Dim_Cliente
- Dim_Vendedor
- Dim_Tienda
- Dim_Ubigeo

_Hechos_
- Fact_Venta_Cabecera
- Fact_Venta_Detalle


**_Obs:_** Para realizar la proyección de la data se tomó de base ventas de los años 2007-2008, luego, utilizando el Método de Suavización Exponencial se creó la lógica y programa en Python para la generación de nuevas ventas _Cabecera_ y _Detalle_ (simulación) de manera automática diariamente.
