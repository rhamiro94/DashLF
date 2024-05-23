import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import dash_table
import plotly.express as px
import psycopg2
import pandas as pd
from datetime import datetime, timedelta

# Conecta a la base de datos PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="xxxx",
    user="postgres",
    password="xxxx"
)

# Define una función para cargar los datos de PostgreSQL en un DataFrame
def carga_df_psql():
    query = "SELECT * FROM mav2024;"
    df = pd.read_sql(query, conn)
    return df

# Carga los datos de PostgreSQL en un DataFrame
df = carga_df_psql()

# Guardar el DataFrame como un archivo CSV
csv_file_path = "datos.csv"
df.to_csv(csv_file_path, index=False)
