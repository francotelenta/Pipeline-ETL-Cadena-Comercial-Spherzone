USE DW_Spherzone;

CREATE TABLE Dim_Tienda (
IDTienda	INT PRIMARY KEY,
Descripcion_Tienda	NVARCHAR(255) NULL,
Descripcion_Tienda_Larga	NVARCHAR(255) NULL,
CO_UNID	INT NULL,
Codigo_Empresa	INT NULL,
Descripcion_Direccion	NVARCHAR(255) NULL,
CodigoUbigeo	INT NULL,
Codigo_Pais	NVARCHAR(255) NULL,
Numero_Telefono1	NVARCHAR(255) NULL,
Numero_Telefono2	NVARCHAR(255) NULL,
Numero_Fax	NVARCHAR(255) NULL
);


CREATE TABLE Dim_Cliente (
CodCliente	INT PRIMARY KEY,
Nombre_Cliente	NVARCHAR(255) NULL,
Codigo_Tipo_Cliente	INT NULL,
Codigo_Empresa	INT NULL,
Tipo_Naturaleza	NVARCHAR(255) NULL,
Fecha_Ingreso	NVARCHAR(255) NULL,
Codigo_Zona	NVARCHAR(255) NULL,
Descripcion_Zona	NVARCHAR(255) NULL,
Codigo_Moneda_Credito	NVARCHAR(255) NULL,
Importe_Limite_Credito	INT NULL
);


CREATE TABLE Dim_Vendedor (
IDVendedor	INT PRIMARY KEY,
Nombre_Vendedor	NVARCHAR(255) NULL,
Codigo_Tipo_Vendedor	INT NULL,
Codigo_Tienda_Actual	INT NULL,
Codigo_Empresa	INT NULL,
);


CREATE TABLE Fact_VentaCabecera (
Cod_Venta	INT PRIMARY KEY,
Numero_Documento	NVARCHAR(255) NULL,
Tipo_Documento	NVARCHAR(255) NULL,
Correlativo	INT NULL,
Codigo_Unidad	INT NULL,
Codigo_Empresa	INT NULL,
Codigo_Tipo_Documento	NVARCHAR(255) NULL,
Codigo_Unidad_Venta	INT NULL,
CodigoVendedor	INT NULL,
Codigo_Cliente	INT NULL,
Codigo_Tipo_Facturacion	NVARCHAR(255) NULL,
Codigo_Almacen	INT NULL,
Codigo_Condicion_Pago	INT NULL,
Codigo_Tienda	INT NULL,
Numero_Signo	INT NULL,
Fecha_Documento	DATE NULL,
Venta_MonNacional	FLOAT NULL,
Venta_MonExtranjera	FLOAT NULL,
);


CREATE TABLE Fact_VentaDetalle (
IDVenta INT NULL UNIQUE,
CodigoProducto	INT NULL,
Cantidad	INT NULL,
Venta_MonNacional	FLOAT NULL,
Venta_MonExtranjera	FLOAT NULL,
Descuento_MonNacional	FLOAT NULL,
Descuento_MonExtranjera	FLOAT NULL,
Impuesto_MonNacional	FLOAT NULL,
Impuesto_MonExtranjera	FLOAT NULL,
Costo_MonNacional	FLOAT NULL,
Costo_MonExtranjera	FLOAT NULL,
Codigo_UnidadMedida	NVARCHAR(255) NULL,
Codigo_UnidadMedida_Venta	NVARCHAR(255) NULL
);



CREATE TABLE Dim_Producto (
IDProducto	INT PRIMARY KEY,
Descripcion_Articulo	NVARCHAR(255) NULL,
Descripcion_Articulo_Largo	NVARCHAR(255) NULL,
Codigo_Familia	INT NULL,
Val_MonedaNacional	FLOAT NULL,
Val_MonedaExtranjera	FLOAT NULL,
Codigo_Marca	NVARCHAR(255) NULL,
Descripcion_Marca	NVARCHAR(255) NULL,
Tipo_Presentacion	NVARCHAR(255) NULL,
Descripcion_Tipo_Presentacion	NVARCHAR(255) NULL,
Codigo_Empresa	NVARCHAR(255) NULL,
Codigo_UnidadMedida	NVARCHAR(255) NULL,
Descripcion_UnidadMedida	NVARCHAR(255) NULL
);


CREATE TABLE Dim_Tipo_Producto (
Codigo_Tipo_Producto INT PRIMARY KEY,
Descripcion_TipoProducto NVARCHAR(255) NULL
);


CREATE TABLE Dim_Rubro_Producto (
IDRubro	INT PRIMARY KEY,
Descripcion_Rubro_Producto NVARCHAR(255) NULL,	
Codigo_Tipo INT NULL,
);

CREATE TABLE Dim_Familia_Producto (
CodigoFamilia INT PRIMARY KEY,
FamiliaProducto	NVARCHAR(255) NULL,
CodigoRubro INT NULL
);


CREATE TABLE Dim_Ubigeo (
IDUbigeo INT PRIMARY KEY,
Descripcion_Ubicacion_Geografica NVARCHAR(255) NULL
);
