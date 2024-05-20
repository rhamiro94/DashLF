import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import dash_table
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv("datos.csv")


fecha_actual = datetime.now()

# Construir la fecha de inicio del año actual
fecha_inicio_anio = datetime(fecha_actual.year, 1, 1)

# Formato de fecha para la API (DD/MM/AA)
fecha_formato_api = "%d/%m/%y"
df['Fecha'] = pd.to_datetime(df['Fecha'])

df['Mes'] = df['Fecha'].dt.month

coltab1 = ['Tipo Instrumento', ' Monto', 'Mes']
# Define la propiedad 'columns' con las columnas seleccionadas
coltab2 = ['Segmento', 'Periodo', ' Tasa']

df_tab1 = df[coltab1].groupby(['Tipo Instrumento', 'Mes']).sum().groupby(level=0).cumsum().reset_index()
df_tab2 = df[coltab2].groupby(['Segmento', 'Periodo']).mean().groupby(level=0).cumsum().reset_index()

pivot_table1 = df.pivot_table(index='Tipo Instrumento', columns='Mes', values=' Monto', aggfunc='sum',
                              fill_value=0).reset_index()

columnas_a_sumar = pivot_table1.columns[1:]  # Excluye la primera columna

# Suma por fila, saltando la primera columna
pivot_table1['Total'] = pivot_table1[columnas_a_sumar].sum(axis=1)

suma_por_columna = pivot_table1.iloc[:, 1:].sum()

# Agregar la fila de suma por columna a pivot_table1
pivot_table1.loc['Total por Columna'] = ['Total'] + suma_por_columna.tolist()

pivot_table2 = df.pivot_table(index='Segmento', columns='Periodo', values=' Tasa', aggfunc='mean',
                              fill_value=0).reset_index()

pivot_table1 = pivot_table1.apply(pd.to_numeric, errors='ignore')

pivot_table1['Total por Instrumento'] = pivot_table1.sum()

meses = df['Mes'].unique()
accumulated_df = df.groupby(['Mes', 'Segmento'])[' Monto'].sum().reset_index()
pivot_table1.drop(columns=['Total por Instrumento'], inplace=True)

# Supongamos que ya tienes definido tu dataframe df

app = dash.Dash(__name__)
server = app.server
# Define tus datos, por ejemplo df para el dataframe de tus datos

app.layout = html.Div([
    html.H1("MAV 2024 ARG VALORES"),

    html.Div([
    html.Div([
        html.Label("Selecciona un mes:"),
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': mes, 'value': mes} for mes in meses],
            value=meses.tolist(),
            multi=True,  # Establecer el valor predeterminado como el primer mes en el dataframe
        ),
    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top'}),  # Estilo para el primer dropdown
    
    html.Div([
        html.Label("Selecciona Segmento:"),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': category, 'value': category} for category in df['Segmento'].unique()],  # Define las opciones del dropdown
            value=[],
            multi=True,
        ),
    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top'})]),
    html.Div([
        dash_table.DataTable(
            id='table-1',
            columns=[{'name': str(col), 'id': str(col)} for col in pivot_table1.columns],  # Define las columnas de la tabla
            data=pivot_table1.to_dict('records'),
            style_table={'overflowX': 'auto'},  # Ajustar el ancho de la tabla al contenido
            style_cell={'textAlign': 'center'},  # Define los datos de la tabla
        )
    ], style={'display': 'inline-block', 'width': '48%', 'marginRight': '2%'}),
    html.Div([
        dash_table.DataTable(
            id='table-2',
            columns=[{'name': str(col), 'id': str(col)} for col in pivot_table2.columns],
            data=pivot_table2.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
        )
    ], style={'display': 'inline-block', 'width': '50%'}),
    html.Div([
        dcc.Graph(
            id='scatter-plot',
            figure=px.scatter(df, x='dias_entre_fechas', y=' Tasa', color='Segmento', title='Scatter Plot'),
        )
    ], style={'display': 'inline-block', 'width': '50%'}),
    html.Div([
        dcc.Graph(
            id='bar-chart',
            figure=px.bar(accumulated_df, x='Mes', y=' Monto', color='Segmento', barmode='stack',
                          title='Insturmentos operados por mes'),  # Define la figura del gráfico de barras
        )
    ], style={'display': 'inline-block', 'width': '50%'}),

])

# Callback para actualizar las tablas


# Callback para actualizar las tablas
# Callback para actualizar las tablas
@app.callback(
    Output('table-1', 'data'),
    Output('table-2', 'data'),
    Output('scatter-plot', 'figure'),
    Output('bar-chart', 'figure'),
    Input('month-dropdown', 'value'),
    Input('category-dropdown', 'value')
)
def update_tables(selected_month, categories):
    filtered_df = df.copy()

    if selected_month:
        filtered_df = filtered_df[filtered_df['Mes'].isin(selected_month)]

    if categories:
        filtered_df = filtered_df[filtered_df['Segmento'].isin(categories)]

    pivot_table1 = filtered_df.pivot_table(index='Tipo Instrumento', columns='Mes', values=' Monto', aggfunc='sum',
                                           fill_value=0).reset_index()
    columnas_a_sumar = pivot_table1.columns[1:]
    pivot_table1['Total'] = pivot_table1[columnas_a_sumar].sum(axis=1)
    pivot_table1.loc['Total por Columna'] = ['Total'] + pivot_table1[columnas_a_sumar].sum().tolist() + [pivot_table1['Total'].sum()]


    pivot_table2 = filtered_df.pivot_table(index='Segmento', columns='Periodo', values=' Tasa', aggfunc='mean',
                                           fill_value=0).reset_index()
    scatter_fig = px.scatter(filtered_df, x='dias_entre_fechas', y=' Tasa', color='Segmento', title='Scatter Plot')
    bar_fig = px.bar(filtered_df.groupby(['Mes', 'Segmento'])[' Monto'].sum().reset_index(), x='Mes', y=' Monto',
                     color='Segmento', barmode='stack', title='Instrumentos operados por mes')
    pivot_table2 = pivot_table2.round(2)

    return pivot_table1.to_dict('records'), pivot_table2.to_dict('records'), scatter_fig, bar_fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)