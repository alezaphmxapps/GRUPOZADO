import sqlite3
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np
from datetime import datetime

DB_FILE = "customer_data.db"
# Use a fixed date for recency calculation to ensure deterministic results
ANALYSIS_DATE = datetime(2024, 5, 1)

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    return conn

def prepare_rfm_data():
    """
    Fetches data from the database and calculates Recency, Frequency, and Monetary values for each customer.
    """
    conn = get_db_connection()
    # Query to get sales data for each customer
    query = """
    SELECT
        c.idCliente,
        v.fechaVenta,
        v.totalVenta
    FROM
        Cliente c
    LEFT JOIN
        Venta v ON c.idCliente = v.idCliente;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Handle customers with no sales
    df['fechaVenta'] = pd.to_datetime(df['fechaVenta'])
    df_customers_with_sales = df.dropna(subset=['fechaVenta'])

    # Calculate Recency, Frequency, Monetary values
    rfm = df_customers_with_sales.groupby('idCliente').agg(
        Recency=('fechaVenta', lambda date: (ANALYSIS_DATE - date.max()).days),
        Frequency=('fechaVenta', 'count'),
        Monetary=('totalVenta', 'sum')
    ).reset_index()

    # Include customers with no sales in the RFM table
    all_customer_ids = pd.read_sql_query("SELECT idCliente FROM Cliente", get_db_connection())
    rfm = pd.merge(all_customer_ids, rfm, on='idCliente', how='left').fillna(0)

    # For customers with no sales, recency should be high (bad)
    # Let's set it to a value higher than any existing recency
    if not rfm.empty and rfm['Recency'].max() > 0:
        max_recency = rfm['Recency'].max()
        rfm['Recency'] = rfm['Recency'].replace(0, max_recency * 1.5)
        # But if they also have 0 frequency and monetary, they are inactive, so a high value is correct.
        # Let's adjust the logic for filling NA
        rfm.fillna({'Frequency': 0, 'Monetary': 0, 'Recency': 999}, inplace=True)


    return rfm

def run_segmentation(n_clusters=3):
    """
    Runs the full segmentation process: data prep, clustering, and saving results.
    """
    print("Starting customer segmentation...")

    rfm_df = prepare_rfm_data()

    if rfm_df.empty or len(rfm_df) < n_clusters:
        print("Not enough data to perform clustering.")
        return

    # Prepare data for clustering
    features = rfm_df[['Recency', 'Frequency', 'Monetary']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Apply K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(scaled_features)

    # Add cluster labels to the dataframe
    rfm_df['cluster'] = kmeans.labels_

    # Analyze clusters to create meaningful segment names
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    # Order clusters by Monetary value (desc) to identify high-value customers
    sorted_clusters_indices = np.argsort(cluster_centers[:, 2])[::-1]

    segment_map = {}
    segment_names = ["Campeones", "Potenciales", "En Riesgo"] # High, Medium, Low value

    for i, idx in enumerate(sorted_clusters_indices):
        segment_map[idx] = (segment_names[i], f"Recency: {cluster_centers[idx, 0]:.0f} days, Freq: {cluster_centers[idx, 1]:.1f}, Spend: ${cluster_centers[idx, 2]:.2f}")

    rfm_df['segmentName'] = rfm_df['cluster'].map(lambda x: segment_map[x][0])
    rfm_df['segmentDescription'] = rfm_df['cluster'].map(lambda x: segment_map[x][1])

    print("Segmentation complete. Saving results to database...")
    save_results_to_db(rfm_df, segment_map)

    return rfm_df

def save_results_to_db(df, segment_map):
    """
    Saves the segmentation results into the Segmento and ResultadoIA tables.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear previous results
    cursor.execute("DELETE FROM ResultadoIA;")
    cursor.execute("DELETE FROM Segmento;")

    # Save new segments
    segment_id_map = {}
    for cluster_id, (name, desc) in segment_map.items():
        cursor.execute("INSERT INTO Segmento (nombreSegmento, descripcion) VALUES (?, ?)", (name, desc))
        segment_id_map[name] = cursor.lastrowid

    # Save customer segmentation results
    today = datetime.now().strftime('%Y-%m-%d')
    for _, row in df.iterrows():
        segment_id = segment_id_map[row['segmentName']]
        # Score could be distance to centroid, but let's keep it simple for now and use 0
        cursor.execute(
            "INSERT INTO ResultadoIA (idCliente, idSegmento, score, fechaAnalisis) VALUES (?, ?, ?, ?)",
            (row['idCliente'], segment_id, 0.0, today)
        )

    conn.commit()
    conn.close()
    print("Results saved to database.")

import matplotlib.pyplot as plt
import seaborn as sns

def create_visualizations(df):
    """
    Creates and saves visualizations for the customer segments.
    """
    if df.empty:
        print("Dataframe is empty, skipping visualization.")
        return

    print("\nCreating visualizations...")
    output_dir = "visualizations"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Scatter plot of Recency vs Monetary
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df,
        x='Recency',
        y='Monetary',
        hue='segmentName',
        palette='viridis',
        s=100,  # size of points
        alpha=0.7
    )
    plt.title('Segmentación de Clientes (Recencia vs. Gasto)', fontsize=16)
    plt.xlabel('Recencia (días)', fontsize=12)
    plt.ylabel('Gasto Monetario ($)', fontsize=12)
    plt.legend(title='Segmento')
    plt.grid(True)
    scatter_path = os.path.join(output_dir, "segment_scatter_plot.png")
    plt.savefig(scatter_path)
    plt.close()
    print(f"Saved scatter plot to {scatter_path}")

    # Bar plots for RFM characteristics
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Características Promedio por Segmento', fontsize=16)

    # Recency
    sns.barplot(data=df, x='segmentName', y='Recency', ax=axes[0], palette='viridis', order=df.groupby('segmentName')['Recency'].mean().sort_values().index)
    axes[0].set_title('Recencia Promedio')
    axes[0].set_xlabel('Segmento')
    axes[0].set_ylabel('Días')

    # Frequency
    sns.barplot(data=df, x='segmentName', y='Frequency', ax=axes[1], palette='viridis', order=df.groupby('segmentName')['Frequency'].mean().sort_values(ascending=False).index)
    axes[1].set_title('Frecuencia Promedio')
    axes[1].set_xlabel('Segmento')
    axes[1].set_ylabel('Número de Compras')

    # Monetary
    sns.barplot(data=df, x='segmentName', y='Monetary', ax=axes[2], palette='viridis', order=df.groupby('segmentName')['Monetary'].mean().sort_values(ascending=False).index)
    axes[2].set_title('Gasto Monetario Promedio')
    axes[2].set_xlabel('Segmento')
    axes[2].set_ylabel('Gasto Total ($)')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    barchart_path = os.path.join(output_dir, "segment_characteristics.png")
    plt.savefig(barchart_path)
    plt.close()
    print(f"Saved bar charts to {barchart_path}")


if __name__ == "__main__":
    results_df = run_segmentation()
    if results_df is not None:
        print("\n--- Segmentation Results Summary ---")
        # Display summary by segment
        summary = results_df.groupby('segmentName').agg(
            Numero_de_Clientes=('idCliente', 'count'),
            Recencia_Promedio=('Recency', 'mean'),
            Frecuencia_Promedio=('Frequency', 'mean'),
            Gasto_Promedio=('Monetary', 'mean')
        ).reset_index()
        print(summary)

        print("\n--- Sample of Segmented Customers ---")
        print(results_df.head())

        # Create and save visualizations
        create_visualizations(results_df)
