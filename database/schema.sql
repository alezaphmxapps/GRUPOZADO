-- database/schema.sql
-- This script defines the database schema for the customer segmentation project.

-- Turn on foreign key support
PRAGMA foreign_keys = ON;

-- Table: Cliente
-- Stores customer information.
CREATE TABLE IF NOT EXISTS Cliente (
    idCliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER,
    genero TEXT,
    region TEXT,
    fechaRegistro DATE NOT NULL
);

-- Table: Producto
-- Stores product information.
CREATE TABLE IF NOT EXISTS Producto (
    idProducto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombreProducto TEXT NOT NULL,
    categoria TEXT,
    precioUnitario REAL NOT NULL
);

-- Table: Venta
-- Stores sales transactions, linked to a customer.
CREATE TABLE IF NOT EXISTS Venta (
    idVenta INTEGER PRIMARY KEY AUTOINCREMENT,
    idCliente INTEGER NOT NULL,
    fechaVenta DATE NOT NULL,
    totalVenta REAL NOT NULL,
    FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente)
);

-- Table: DetalleVenta
-- Stores the details of each sale, linking products to a sale.
CREATE TABLE IF NOT EXISTS DetalleVenta (
    idDetalle INTEGER PRIMARY KEY AUTOINCREMENT,
    idVenta INTEGER NOT NULL,
    idProducto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    FOREIGN KEY (idVenta) REFERENCES Venta(idVenta),
    FOREIGN KEY (idProducto) REFERENCES Producto(idProducto)
);

-- Table: Segmento
-- Stores the definitions of customer segments identified by the AI model.
CREATE TABLE IF NOT EXISTS Segmento (
    idSegmento INTEGER PRIMARY KEY AUTOINCREMENT,
    nombreSegmento TEXT NOT NULL UNIQUE,
    descripcion TEXT
);

-- Table: ResultadoIA
-- Stores the segmentation result for each customer.
CREATE TABLE IF NOT EXISTS ResultadoIA (
    idResultado INTEGER PRIMARY KEY AUTOINCREMENT,
    idCliente INTEGER NOT NULL,
    idSegmento INTEGER NOT NULL,
    score REAL, -- e.g., distance to cluster centroid
    fechaAnalisis DATE NOT NULL,
    FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente),
    FOREIGN KEY (idSegmento) REFERENCES Segmento(idSegmento)
);
