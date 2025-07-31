import os
import src.database_setup as db_setup
import src.queries as queries
import src.segmentation as segmentation

def main():
    """
    Main function to orchestrate the entire customer segmentation project workflow.
    """
    print("=================================================")
    print("  Proyecto: Segmentación de Clientes con IA")
    print("=================================================\n")

    # --- Step 1: Database Setup ---
    # Check if the database exists, if not, create and seed it.
    if not os.path.exists(db_setup.DB_FILE):
        print("--- Step 1: Configurando la base de datos... ---")
        db_setup.setup_database()
        print("--- Base de datos configurada. ---\n")
    else:
        print("--- Step 1: La base de datos ya existe. Omitiendo configuración. ---\n")

    # --- Step 2: Run Strategic SQL Queries ---
    print("--- Step 2: Ejecutando consultas SQL estratégicas... ---")
    queries.main()
    print("--- Consultas finalizadas. ---\n")

    # --- Step 3 & 4: AI Segmentation and Visualization ---
    print("--- Step 3: Ejecutando segmentación de clientes con IA... ---")
    results_df = segmentation.run_segmentation()

    if results_df is not None:
        print("\n--- Resumen de la Segmentación ---")
        summary = results_df.groupby('segmentName').agg(
            Numero_de_Clientes=('idCliente', 'count'),
            Recencia_Promedio=('Recency', 'mean'),
            Frecuencia_Promedio=('Frequency', 'mean'),
            Gasto_Promedio=('Monetary', 'mean')
        ).reset_index()
        print(summary)

        print("\n--- Step 4: Creando visualizaciones de los segmentos... ---")
        segmentation.create_visualizations(results_df)
        print("--- Visualizaciones creadas en la carpeta 'visualizations/'. ---\n")
    else:
        print("No se pudo completar la segmentación.")

    print("=================================================")
    print("            Flujo del proyecto completado")
    print("=================================================")

if __name__ == "__main__":
    main()
