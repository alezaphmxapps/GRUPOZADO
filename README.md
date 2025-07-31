# Proyecto: Segmentación de Clientes con Base de Datos para Inteligencia Artificial

Este proyecto es una solución de software que realiza una segmentación de clientes utilizando un análisis RFM (Recencia, Frecuencia, Gasto Monetario) y un algoritmo de clustering K-Means. El sistema está construido en Python y utiliza una base de datos SQLite para el almacenamiento de datos.

El propósito es identificar distintos grupos de clientes basados en su comportamiento de compra, permitiendo a una empresa dirigir estrategias de marketing de manera más efectiva.

## Características Principales

*   **Base de Datos Relacional**: Utiliza SQLite para almacenar datos de clientes, productos y ventas.
*   **Consultas SQL Estratégicas**: Incluye 8 consultas SQL complejas para extraer insights del negocio.
*   **Segmentación con IA**: Aplica el algoritmo K-Means para agrupar clientes en segmentos significativos (ej. "Campeones", "Potenciales", "En Riesgo").
*   **Visualización de Datos**: Genera gráficos (scatter plots y bar charts) para visualizar los segmentos y sus características.
*   **Orquestación Completa**: Un script principal (`main.py`) que ejecuta todo el flujo de trabajo, desde la creación de la base de datos hasta la generación de visualizaciones.

## Estructura del Proyecto

```
.
├── customer_data.db      # Base de datos SQLite (generada al ejecutar)
├── database/
│   ├── schema.sql        # Script SQL para crear la estructura de la BD
│   └── seed_data.sql     # Script SQL para poblar la BD con datos de prueba
├── main.py               # Script principal para ejecutar todo el proyecto
├── README.md             # Este archivo
├── requirements.txt      # Dependencias de Python
├── src/
│   ├── database_setup.py # Script para inicializar la base de datos
│   ├── queries.py        # Script con las 8 consultas SQL estratégicas
│   └── segmentation.py   # Script para la segmentación con IA y visualización
└── visualizations/       # Directorio donde se guardan los gráficos (generado)
    ├── segment_characteristics.png
    └── segment_scatter_plot.png
```

## Requisitos

*   Python 3.x
*   pip (manejador de paquetes de Python)

## Cómo Empezar

Siga estos pasos para configurar y ejecutar el proyecto en su entorno local.

### 1. Clonar el Repositorio

Primero, clone este repositorio en su máquina local:
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_DIRECTORIO>
```

### 2. Instalar Dependencias

Instale todas las librerías de Python necesarias utilizando el archivo `requirements.txt`. Se recomienda crear un entorno virtual primero.

```bash
# Crear y activar un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar las dependencias
pip install -r requirements.txt
```

### 3. Ejecutar el Proyecto

Una vez instaladas las dependencias, puede ejecutar el proyecto completo con un solo comando:

```bash
python main.py
```

El script `main.py` se encargará de todo:
1.  Creará y poblará la base de datos (`customer_data.db`) si no existe.
2.  Ejecutará las 8 consultas SQL y mostrará los resultados en la consola.
3.  Realizará la segmentación de clientes y guardará los resultados en la base de datos.
4.  Creará los gráficos de visualización y los guardará en la carpeta `visualizations/`.

¡Y eso es todo! Ahora puede revisar los resultados en la consola y los gráficos en la carpeta `visualizations`.
