import dash
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Monitor de Resultados Recibidos (Servidor)", style={"textAlign": "center"}),
    html.Button("Actualizar", id="btn-refresh", n_clicks=0, style={"marginBottom": "20px"}),
    dash_table.DataTable(
        id='results-table',
        columns=[
            {'name': 'Algoritmo', 'id': 'algoritmo'},
            {'name': 'Tiempo (s)', 'id': 'tiempo'},
            {'name': 'Datos Procesados', 'id': 'cantidad_datos'},
            {'name': 'Fecha', 'id': 'fecha'}
        ],
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'whiteSpace': 'normal',
            'height': 'auto',
            'backgroundColor': '#e3f2fd',
            'color': '#0d47a1',
            'fontWeight': 'bold',
        },
        style_header={
            'backgroundColor': '#1976d2',
            'color': 'white',
            'fontWeight': 'bold',
            'fontSize': '1.1em',
            'border': '1px solid #1565c0',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#bbdefb',
            },
            {
                'if': {'row_index': 'even'},
                'backgroundColor': '#e3f2fd',
            },
        ]
    ),
    dcc.Graph(id="time-graph"),
])

@app.callback(
    [Output('results-table', 'data'),
     Output('time-graph', 'figure')],
    Input('btn-refresh', 'n_clicks')
)
def update_table(n):
    try:
        with open("recibidos.json", "r") as f:
            results = json.load(f)
    except:
        results = []
    df = pd.DataFrame(results)
    if not df.empty and 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'])
        df = df.sort_values('tiempo')
    if not df.empty:
        avg_df = df.groupby('algoritmo', as_index=False)['tiempo'].mean()
        time_fig = px.bar(
            avg_df,
            x='algoritmo',
            y='tiempo',
            title='Promedio de Tiempo de Ejecución por Algoritmo',
            labels={'tiempo': 'Tiempo Promedio (segundos)', 'algoritmo': 'Algoritmo'},
            color='algoritmo',
            color_discrete_sequence=px.colors.sequential.Blues[2:]
        )
        time_fig.update_layout(
            xaxis_title="Algoritmo",
            yaxis_title="Tiempo Promedio (segundos)",
            showlegend=False
        )
    else:
        time_fig = {}
    return df.to_dict('records'), time_fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8051) 