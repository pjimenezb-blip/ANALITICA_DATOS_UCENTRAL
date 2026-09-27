"""Dashboard interactivo de retrasos de vuelos (tarea).

Ejecutar en desarrollo:
    python dashboard.py        ->  http://127.0.0.1:8050

Ejecutar en produccion (lo hace la plataforma de despliegue):
    gunicorn dashboard:server  ->  usa el objeto WSGI `server` de este modulo
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from plotly.graph_objects import Figure

# --------------------------------------------------------------------- datos
# Los datos viajan CON el repositorio y se leen desde la carpeta del archivo.
# NO uses rutas absolutas: en el servidor las rutas son distintas.
DATA_FILE = Path(__file__).with_name("airline_data.csv")

df = pd.read_csv(
    DATA_FILE,
    encoding="ISO-8859-1",
    # Estos campos traen ceros a la izquierda: deben leerse como texto.
    dtype={
        "Div1Airport": str,
        "Div1TailNum": str,
        "Div2Airport": str,
        "Div2TailNum": str,
    },
)

CAUSAS = [
    ("CarrierDelay", "Retraso por transportista (carrier)", "carrier-plot"),
    ("WeatherDelay", "Retraso por clima", "weather-plot"),
    ("NASDelay", "Retraso por sistema aéreo nacional (NAS)", "nas-plot"),
    ("SecurityDelay", "Retraso por seguridad", "security-plot"),
    ("LateAircraftDelay", "Retraso por aeronave tardía (late aircraft)", "late-plot"),
]

PALETA = px.colors.qualitative.Dark24

ESTILO_PAGINA = {
    "fontFamily": "Segoe UI, Helvetica, Arial, sans-serif",
    "backgroundColor": "#f4f6f8",
    "color": "#1f2933",
    "minHeight": "100vh",
    "padding": "24px 32px 40px",
}

ESTILO_FILA = {
    "display": "flex",
    "flexWrap": "wrap",
    "gap": "16px",
    "marginBottom": "16px",
}

ESTILO_TARJETA = {
    "flex": "1 1 420px",
    "backgroundColor": "#ffffff",
    "borderRadius": "12px",
    "boxShadow": "0 1px 4px rgba(15, 23, 42, 0.08)",
    "padding": "8px",
}

app = Dash(__name__)

# -------------------------------------------------------------------- layout
app.layout = html.Div(
    style=ESTILO_PAGINA,
    children=[
        html.H1(
            "Operaciones aéreas: causas de retraso de vuelos",
            style={"marginBottom": "8px", "fontSize": "1.9rem"},
        ),
        html.P(
            "Consulta el retraso promedio (en minutos) por aerolínea y por mes. "
            "Elige un año para actualizar los cinco gráficos.",
            style={"marginTop": 0, "color": "#52606d"},
        ),
        html.Div(
            style={
                "display": "flex",
                "alignItems": "center",
                "gap": "12px",
                "margin": "16px 0 24px",
                "flexWrap": "wrap",
            },
            children=[
                html.Label("Año:", htmlFor="input-year", style={"fontWeight": 600}),
                dcc.Input(
                    id="input-year",
                    type="number",
                    value=2010,
                    min=1987,
                    max=2020,
                    step=1,
                    debounce=True,
                    placeholder="Ej. 2010",
                    style={"padding": "8px 12px", "fontSize": "1rem", "width": "140px"},
                ),
            ],
        ),
        html.Div(
            style=ESTILO_FILA,
            children=[
                html.Div(dcc.Graph(id="carrier-plot"), style=ESTILO_TARJETA),
                html.Div(dcc.Graph(id="weather-plot"), style=ESTILO_TARJETA),
            ],
        ),
        html.Div(
            style=ESTILO_FILA,
            children=[
                html.Div(dcc.Graph(id="nas-plot"), style=ESTILO_TARJETA),
                html.Div(dcc.Graph(id="security-plot"), style=ESTILO_TARJETA),
            ],
        ),
        html.Div(
            style=ESTILO_FILA,
            children=[
                html.Div(dcc.Graph(id="late-plot"), style=ESTILO_TARJETA),
            ],
        ),
    ],
)


# ------------------------------------------------------------------ calculos
def compute_info(datos, entered_year):
    """Devuelve 5 tablas (una por causa de retraso) para el ano pedido.

    Cada tabla debe tener las columnas: Month, Reporting_Airline y el
    promedio de la causa correspondiente.
    """
    anio = int(entered_year)
    df_anio = datos[datos["Year"] == anio]
    columnas_grupo = ["Month", "Reporting_Airline"]
    columnas_delay = [causa for causa, _, _ in CAUSAS]
    agrupado = (
        df_anio.groupby(columnas_grupo, as_index=False)[columnas_delay]
        .mean(numeric_only=True)
        .sort_values(columnas_grupo)
    )
    return tuple(agrupado[columnas_grupo + [causa]] for causa, _, _ in CAUSAS)


def figura_vacia(titulo, mensaje):
    """Figura sin series, con un aviso visible (RF5 y RF7)."""
    fig = Figure()
    fig.update_layout(
        title=titulo,
        xaxis_title="Mes",
        yaxis_title="Retraso promedio (minutos)",
        template="plotly_white",
        annotations=[
            {
                "text": mensaje,
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
                "font": {"size": 14, "color": "#52606d"},
            }
        ],
    )
    return fig


def figura_linea(tabla, columna_y, titulo):
    fig = px.line(
        tabla,
        x="Month",
        y=columna_y,
        color="Reporting_Airline",
        markers=True,
        color_discrete_sequence=PALETA,
        title=titulo,
        labels={
            "Month": "Mes",
            columna_y: "Retraso promedio (minutos)",
            "Reporting_Airline": "Aerolínea",
        },
    )
    fig.update_layout(
        template="plotly_white",
        legend_title_text="Aerolínea",
        hovermode="x unified",
    )
    fig.update_xaxes(dtick=1)
    return fig


# ------------------------------------------------------------------ callback
@app.callback(
    [
        Output("carrier-plot", "figure"),
        Output("weather-plot", "figure"),
        Output("nas-plot", "figure"),
        Output("security-plot", "figure"),
        Output("late-plot", "figure"),
    ],
    Input("input-year", "value"),
)
def get_graph(entered_year):
    try:
        anio = int(entered_year)
    except (TypeError, ValueError):
        mensaje = "Escribe un año válido (1987–2020) para ver los gráficos."
        return tuple(
            figura_vacia(f"{titulo} — año no válido", mensaje) for _, titulo, _ in CAUSAS
        )

    tablas = compute_info(df, anio)
    figuras = []
    for tabla, (columna_y, titulo, _) in zip(tablas, CAUSAS):
        titulo_anio = f"{titulo} — {anio}"
        if tabla.empty or tabla[columna_y].dropna().empty:
            figuras.append(
                figura_vacia(
                    titulo_anio,
                    f"No hay datos de retraso para el año {anio}.",
                )
            )
        else:
            figuras.append(figura_linea(tabla, columna_y, titulo_anio))
    return tuple(figuras)


# --------------------------------------------------------------- produccion
# RF9: objeto WSGI que consumira gunicorn. gunicorn IMPORTA este modulo y
# busca una variable llamada `server`; nunca ejecuta el bloque __main__.
server = app.server

if __name__ == "__main__":
    # debug=True recarga el servidor al guardar: comodo en desarrollo,
    # y NUNCA se usa en produccion.
    app.run(debug=True, port=8050)
