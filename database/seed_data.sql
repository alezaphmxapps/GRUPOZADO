-- database/seed_data.sql
-- This script populates the database with fictitious data for the project.

-- Clear existing data
DELETE FROM DetalleVenta;
DELETE FROM Venta;
DELETE FROM Producto;
DELETE FROM Cliente;

-- Reset autoincrement counters
DELETE FROM sqlite_sequence WHERE name IN ('Cliente', 'Producto', 'Venta', 'DetalleVenta');

-- Insert data into Cliente
INSERT INTO Cliente (nombre, edad, genero, region, fechaRegistro) VALUES
('Ana Torres', 28, 'Femenino', 'Norte', '2023-01-15'),
('Carlos Gomez', 45, 'Masculino', 'Sur', '2022-05-20'),
('Luisa Fernandez', 34, 'Femenino', 'Centro', '2023-03-10'),
('Javier Rodriguez', 52, 'Masculino', 'Norte', '2022-11-01'),
('Maria Lopez', 22, 'Femenino', 'Sur', '2024-02-28'),
('Pedro Martinez', 39, 'Masculino', 'Oeste', '2023-07-19'),
('Sofia Hernandez', 29, 'Femenino', 'Centro', '2023-09-05'),
('Miguel Sanchez', 60, 'Masculino', 'Este', '2022-08-11'),
('Elena Diaz', 31, 'Femenino', 'Norte', '2024-01-20'),
('David Romero', 41, 'Masculino', 'Sur', '2023-12-03');

-- Insert data into Producto
INSERT INTO Producto (nombreProducto, categoria, precioUnitario) VALUES
('Laptop Pro', 'Electrónica', 15000.00),
('Smartphone X', 'Electrónica', 8000.00),
('Teclado Mecánico', 'Accesorios', 1200.00),
('Monitor 4K', 'Electrónica', 7500.00),
('Mouse Inalámbrico', 'Accesorios', 500.00),
('Silla Ergonómica', 'Oficina', 4500.00),
('Libro de Programación', 'Libros', 700.00),
('Mochila para Laptop', 'Accesorios', 900.00),
('Audífonos Bluetooth', 'Electrónica', 2500.00),
('Cafetera Express', 'Hogar', 3200.00);

-- Insert data into Venta and DetalleVenta
-- Venta 1: Ana Torres buys a Laptop and a Mouse
INSERT INTO Venta (idCliente, fechaVenta, totalVenta) VALUES (1, '2023-02-10', 15500.00);
INSERT INTO DetalleVenta (idVenta, idProducto, cantidad) VALUES (1, 1, 1), (1, 5, 1);

-- Venta 2: Carlos Gomez buys 2 ergonomic chairs
INSERT INTO Venta (idCliente, fechaVenta, totalVenta) VALUES (2, '2023-03-15', 9000.00);
INSERT INTO DetalleVenta (idVenta, idProducto, cantidad) VALUES (2, 6, 2);

-- Venta 3: Ana Torres buys a mechanical keyboard
INSERT INTO Venta (idCliente, fechaVenta, totalVenta) VALUES (1, '2023-05-22', 1200.00);
INSERT INTO DetalleVenta (idVenta, idProducto, cantidad) VALUES (3, 3, 1);

-- Venta 4: Luisa Fernandez buys a Smartphone and headphones
INSERT INTO Venta (idCliente, fechaVenta, totalVenta) VALUES (3, '2023-06-01', 10500.00);
INSERT INTO DetalleVenta (idVenta, idProducto, cantidad) VALUES (4, 2, 1), (4, 9, 1);

-- Venta 5: Maria Lopez buys 3 programming books
INSERT INTO Venta (idCliente, fechaVenta, totalVenta) VALUES (5, '2024-03-05', 2100.00);
INSERT INTO DetalleVenta (idVenta, idProducto, cantidad) VALUES (5, 7, 3);

-- Venta 6: Carlos Gomez buys a 4K monitor
INSERT INTO Venta (idCliente, fechaVenta, totalVenta) VALUES (2, '2024-03-10', 7500.00);
INSERT INTO DetalleVenta (idVenta, idProducto, cantidad) VALUES (6, 4, 1);

-- Venta 7: David Romero buys a coffee machine
INSERT INTO Venta (idCliente, fechaVenta, totalVenta) VALUES (10, '2024-01-15', 3200.00);
INSERT INTO DetalleVenta (idVenta, idProducto, cantidad) VALUES (7, 10, 1);

-- Venta 8: Elena Diaz buys a backpack and a mouse
INSERT INTO Venta (idCliente, fechaVenta, totalVenta) VALUES (9, '2024-02-20', 1400.00);
INSERT INTO DetalleVenta (idVenta, idProducto, cantidad) VALUES (8, 8, 1), (8, 5, 1);

-- Venta 9: Carlos Gomez buys 5 programming books
INSERT INTO Venta (idCliente, fechaVenta, totalVenta) VALUES (2, '2024-04-11', 3500.00);
INSERT INTO DetalleVenta (idVenta, idProducto, cantidad) VALUES (9, 7, 5);
