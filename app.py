import dash
from dash import Dash, html, dcc, dash_table, ctx
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import threading
from threads_sockets.client_side import ejecutar_algoritmo, algos
import time
from datetime import datetime

# Inicializar la aplicación Dash
app = Dash(__name__)

# Paleta de azules
BLUES = px.colors.sequential.Blues[2:]

# Layout de la aplicación
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Benchmark de Algoritmos de Ordenamiento", 
                className="header-title"),
        html.P("Comparativa de rendimiento entre diferentes algoritmos de ordenamiento",
               className="header-description")
    ], className="header"),

    # Contenedor principal
    html.Div([
        # Panel de control
        html.Div([
            html.H3("Conexión al Servidor", className="panel-title"),
            html.Div([
                dcc.Input(id="input-ip", type="text", placeholder="IP del servidor", value="127.0.0.1", style={"marginRight": "10px"}),
                dcc.Input(id="input-port", type="number", placeholder="Puerto", value=8080, min=1, max=65535, style={"marginRight": "10px"}),
                html.Button("Conectar", id="btn-connect", className="algo-button", n_clicks=0),
            ], style={"marginBottom": "20px"}),
            dcc.Store(id="server-config"),

            html.H3("Controles", className="panel-title"),
            html.Div([
                html.Button(f"Ejecutar {algo}", 
                           id=f"btn-{algo}", 
                           className="algo-button",
                           n_clicks=0,
                           disabled=True) 
                for algo in algos.keys()
            ], className="button-container"),
            html.Button("Ejecutar Todos", 
                       id="btn-all", 
                       className="all-button",
                       n_clicks=0,
                       disabled=True),
            html.Button("Actualizar", id="btn-refresh", className="algo-button", n_clicks=0),
            html.Div(id="status-message", className="status-message")
        ], className="control-panel"),

        # Gráficos
        html.Div([
            html.Div([
                html.H3("Promedio de Tiempo de Ejecución", className="panel-title"),
                dcc.Graph(id="time-graph")
            ], className="graph-container"),
            
            html.Div([
                html.H3("Distribución de Tiempos por Algoritmo", className="panel-title"),
                dcc.Graph(id="comparison-graph")
            ], className="graph-container")
        ], className="graphs-container"),

        # Tabla de resultados
        html.Div([
            html.H3("Resultados Detallados", className="panel-title"),
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
            )
        ], className="table-container"),
       
    ], className="main-container")
])

# Callbacks
@app.callback(
    [Output(f"btn-{algo}", "disabled") for algo in algos.keys()] +
    [Output("btn-all", "disabled"), Output("server-config", "data"),
     Output('time-graph', 'figure'), Output('comparison-graph', 'figure'), Output('results-table', 'data'), Output('status-message', 'children')],
    [Input("btn-connect", "n_clicks")] +
    [Input(f"btn-{algo}", 'n_clicks') for algo in algos.keys()] +
    [Input('btn-all', 'n_clicks'), Input('btn-refresh', 'n_clicks')],
    State("input-ip", "value"),
    State("input-port", "value"),
    State("server-config", "data"),
    prevent_initial_call=True
)
def main_callback(connect_click, *args):
    # Separar los argumentos
    num_algos = len(algos)
    algo_clicks = args[:num_algos]
    all_click = args[num_algos]
    refresh_click = args[num_algos+1]
    ip = args[num_algos+2]
    port = args[num_algos+3]
    server_config = args[num_algos+4]

    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    # Por defecto, todo deshabilitado
    btn_states = [True]*num_algos
    btn_all_state = True
    server_data = dash.no_update
    status_msg = dash.no_update

    # Si el trigger es conectar
    if trigger == 'btn-connect':
        if ip and port:
            btn_states = [False]*num_algos
            btn_all_state = False
            server_data = {"ip": ip, "port": port}
            status_msg = f"Conectado a {ip}:{port}"
        else:
            status_msg = "Por favor ingresa una IP y un puerto válidos."
        # No actualizamos gráficos ni tabla
        return btn_states + [btn_all_state, server_data, dash.no_update, dash.no_update, dash.no_update, status_msg]

    # Si el trigger es algún botón de algoritmo, ejecutar el algoritmo correspondiente
    if trigger.startswith('btn-') and trigger != 'btn-all' and trigger != 'btn-refresh':
        algo = trigger.split('-')[1]
        if server_config and algo in algos:
            ip = server_config["ip"]
            port = int(server_config["port"])
            ejecutar_algoritmo(algo, ip, port)
            status_msg = f"Ejecutado {algo} en {ip}:{port}"

    # Si el trigger es btn-all, ejecutar todos
    if trigger == 'btn-all' and server_config:
        ip = server_config["ip"]
        port = int(server_config["port"])
        for algo in algos.keys():
            ejecutar_algoritmo(algo, ip, port)
            time.sleep(1)
        status_msg = f"Ejecutados todos los algoritmos en {ip}:{port}"

    # Si el trigger es btn-refresh, solo refresca
    if trigger == 'btn-refresh':
        status_msg = "Datos actualizados."

    # Cargar resultados
    try:
        with open("resultados.json", "r") as f:
            results = json.load(f)
    except:
        results = []

    df = pd.DataFrame(results)
    if not df.empty and 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'])
        df = df.sort_values('fecha',ascending=False)


    if not df.empty:
        avg_df = df.groupby('algoritmo', as_index=False)['tiempo'].mean()
        time_fig = px.bar(
            avg_df,
            x='algoritmo',
            y='tiempo',
            title='Promedio de Tiempo de Ejecución por Algoritmo',
            labels={'tiempo': 'Tiempo Promedio (segundos)', 'algoritmo': 'Algoritmo'},
            color='algoritmo',
            color_discrete_sequence=BLUES
        )
        time_fig.update_layout(
            xaxis_title="Algoritmo",
            yaxis_title="Tiempo Promedio (segundos)",
            showlegend=False
        )
    else:
        time_fig = {}

    if not df.empty:
        box_fig = px.box(
            df,
            x='algoritmo',
            y='tiempo',
            color='algoritmo',
            color_discrete_sequence=BLUES,
            points="all",
            notched=True
        )
        box_fig.update_layout(
            title='Distribución de Tiempos por Algoritmo',
            xaxis_title='Algoritmo',
            yaxis_title='Tiempo (segundos)',
            boxmode='group',
            showlegend=False
        )
    else:
        box_fig = {}

    return btn_states + [btn_all_state, dash.no_update, time_fig, box_fig, df.to_dict('records'), status_msg]

# Estilos CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Benchmark de Algoritmos</title>
        {%favicon%}
        {%css%}
        <style>
            .header {
                background: linear-gradient(90deg, #1565c0 0%, #42a5f5 100%);
                color: white;
                padding: 20px;
                text-align: center;
                margin-bottom: 20px;
                border-radius: 0 0 16px 16px;
                box-shadow: 0 4px 12px rgba(21,101,192,0.15);
            }
            .header-title {
                margin: 0;
                font-size: 2.5em;
                letter-spacing: 2px;
                color: #e3f2fd;
                text-shadow: 1px 1px 2px #0d47a1;
            }
            .header-description {
                margin: 10px 0 0 0;
                font-size: 1.2em;
                color: #bbdefb;
            }
            .main-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .control-panel {
                background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
                box-shadow: 0 2px 8px rgba(33,150,243,0.08);
            }
            .button-container {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
            }
            .algo-button, .all-button {
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-weight: bold;
                transition: background-color 0.3s;
            }
            .algo-button {
                background-color: #1976d2;
                color: white;
            }
            .all-button {
                background-color: #0d47a1;
                color: white;
            }
            .algo-button:hover, .all-button:hover {
                background-color: #1565c0;
                opacity: 0.95;
            }
            .graphs-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 20px;
            }
            .graph-container {
                background: #e3f2fd;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(21,101,192,0.08);
            }
            .table-container {
                background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(21,101,192,0.08);
            }
            .status-message {
                margin-top: 10px;
                color: #1976d2;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True,port=8050)