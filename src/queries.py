import sqlite3
import os
from datetime import datetime, timedelta

DB_FILE = "customer_data.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    if not os.path.exists(DB_FILE):
        raise FileNotFoundError(f"Database file not found: {DB_FILE}. Please run database_setup.py first.")

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# 1. US03: Clientes que gastan más de $10,000
def query_high_value_customers(min_spend=10000.0):
    """Finds customers who have spent more than a given amount."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT c.nombre, SUM(v.totalVenta) AS totalGastado, COUNT(v.idVenta) AS frecuencia
    FROM Cliente c
    JOIN Venta v ON c.idCliente = v.idCliente
    GROUP BY c.idCliente, c.nombre
    HAVING SUM(v.totalVenta) > ?
    ORDER BY totalGastado DESC;
    """
    cursor.execute(query, (min_spend,))
    results = cursor.fetchall()
    conn.close()
    return results

# 2. US04: Clientes frecuentes de cierta región (frecuencia > 1)
def query_frequent_customers_by_region(region, min_purchases=2):
    """Finds frequent customers from a specific region."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT c.nombre, COUNT(v.idVenta) AS numeroDeCompras
    FROM Cliente c
    JOIN Venta v ON c.idCliente = v.idCliente
    WHERE c.region = ?
    GROUP BY c.idCliente, c.nombre
    HAVING COUNT(v.idVenta) >= ?
    ORDER BY numeroDeCompras DESC;
    """
    cursor.execute(query, (region, min_purchases))
    results = cursor.fetchall()
    conn.close()
    return results

# 3. US05: Consulta con 3 INNER JOIN
def query_sales_with_product_details():
    """Shows a detailed list of sales including customer and product names."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT c.nombre AS cliente, p.nombreProducto AS producto, dv.cantidad, v.fechaVenta
    FROM Cliente c
    JOIN Venta v ON c.idCliente = v.idCliente
    JOIN DetalleVenta dv ON v.idVenta = dv.idVenta
    JOIN Producto p ON dv.idProducto = p.idProducto
    ORDER BY v.fechaVenta DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# 4. US06: Ventas sin detalle registrado
def query_sales_without_details():
    """Finds sales that do not have any detail lines. Should return empty if data is consistent."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT v.idVenta, v.fechaVenta, v.totalVenta
    FROM Venta v
    LEFT JOIN DetalleVenta dv ON v.idVenta = dv.idVenta
    WHERE dv.idDetalle IS NULL;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# 5. US12: Productos más vendidos por mes
def query_top_products_by_month():
    """Finds the total quantity of products sold per month."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT
        strftime('%Y-%m', v.fechaVenta) AS mes,
        p.nombreProducto,
        SUM(dv.cantidad) AS totalVendido
    FROM Venta v
    JOIN DetalleVenta dv ON v.idVenta = dv.idVenta
    JOIN Producto p ON dv.idProducto = p.idProducto
    GROUP BY mes, p.nombreProducto
    ORDER BY mes, totalVendido DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# 6. US14: Clientes nuevos del último trimestre
def query_new_customers_last_quarter():
    """Finds customers who registered in the last 90 days."""
    conn = get_db_connection()
    cursor = conn.cursor()
    ninety_days_ago = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    # Using a fixed date for deterministic results in this academic context
    fixed_date = '2024-04-15'
    ninety_days_before_fixed = (datetime.strptime(fixed_date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y-%m-%d')

    query = """
    SELECT nombre, fechaRegistro
    FROM Cliente
    WHERE fechaRegistro >= ?
    ORDER BY fechaRegistro DESC;
    """
    cursor.execute(query, (ninety_days_before_fixed,))
    results = cursor.fetchall()
    conn.close()
    return results

# 7. Gasto promedio por región
def query_average_spend_by_region():
    """Calculates the average spending per customer for each region."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT
        c.region,
        AVG(ventas_por_cliente.totalGastado) as gastoPromedioPorCliente
    FROM Cliente c
    JOIN (
        SELECT idCliente, SUM(totalVenta) AS totalGastado
        FROM Venta
        GROUP BY idCliente
    ) AS ventas_por_cliente ON c.idCliente = ventas_por_cliente.idCliente
    GROUP BY c.region
    ORDER BY gastoPromedioPorCliente DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# 8. Clientes sin compras
def query_customers_with_no_purchases():
    """Finds customers who have never made a purchase."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT c.nombre, c.fechaRegistro
    FROM Cliente c
    LEFT JOIN Venta v ON c.idCliente = v.idCliente
    WHERE v.idVenta IS NULL;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


def main():
    """Main function to execute and print all queries for testing."""
    print("Executing strategic SQL queries...\n")

    print("--- 1. (US03) Clientes con gasto mayor a $10,000 ---")
    for row in query_high_value_customers(10000.0):
        print(f"  - Cliente: {row['nombre']}, Total Gastado: ${row['totalGastado']:.2f}, Compras: {row['frecuencia']}")
    print("-" * 50)

    print("\n--- 2. (US04) Clientes frecuentes de la región 'Norte' (>= 2 compras) ---")
    for row in query_frequent_customers_by_region('Norte', 2):
        print(f"  - Cliente: {row['nombre']}, Compras: {row['numeroDeCompras']}")
    print("-" * 50)

    print("\n--- 3. (US05) Detalle de ventas (3 INNER JOINs) ---")
    for row in query_sales_with_product_details()[:5]: # Limiting output for brevity
        print(f"  - Cliente: {row['cliente']}, Producto: {row['producto']}, Cantidad: {row['cantidad']}, Fecha: {row['fechaVenta']}")
    print("  ...")
    print("-" * 50)

    print("\n--- 4. (US06) Ventas sin detalle registrado ---")
    results = query_sales_without_details()
    if not results:
        print("  - No se encontraron ventas sin detalle. La base de datos es consistente.")
    else:
        for row in results:
            print(f"  - Venta ID: {row['idVenta']}")
    print("-" * 50)

    print("\n--- 5. (US12) Total de productos vendidos por mes ---")
    for row in query_top_products_by_month():
        print(f"  - Mes: {row['mes']}, Producto: {row['nombreProducto']}, Total Vendido: {row['totalVendido']}")
    print("-" * 50)

    print("\n--- 6. (US14) Clientes nuevos (registrados en los últimos 90 días desde 2024-04-15) ---")
    for row in query_new_customers_last_quarter():
        print(f"  - Cliente: {row['nombre']}, Fecha de Registro: {row['fechaRegistro']}")
    print("-" * 50)

    print("\n--- 7. Gasto promedio por cliente en cada región ---")
    for row in query_average_spend_by_region():
        print(f"  - Región: {row['region']}, Gasto Promedio: ${row['gastoPromedioPorCliente']:.2f}")
    print("-" * 50)

    print("\n--- 8. Clientes que nunca han comprado ---")
    for row in query_customers_with_no_purchases():
        print(f"  - Cliente: {row['nombre']}, Fecha de Registro: {row['fechaRegistro']}")
    print("-" * 50)


if __name__ == "__main__":
    main()
