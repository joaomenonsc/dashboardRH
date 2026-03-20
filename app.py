"""Dashboard B.I. de RH — Ponto de entrada."""

import dash
from dash import html
import pandas as pd

from config import COLORS
from data.loader import load_data
from layouts.header import create_header, create_context_bar
from layouts.sidebar import create_sidebar
from layouts.main_content import create_main_content
from callbacks.dashboard import register_callbacks

# --- Data ---
df: pd.DataFrame = load_data()

# --- App ---
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    suppress_callback_exceptions=True,
)
app.title = "B.I. de RH"

app.layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "minHeight": "100vh",
        "backgroundColor": COLORS["bg"],
        "fontFamily": "'Segoe UI', system-ui, sans-serif",
        "color": COLORS["text"],
    },
    children=[
        # Header fixo no topo (F1.1 / F1.2)
        create_header(df),
        # Barra de contexto com chips de filtros ativos (F3.3)
        create_context_bar(),
        # Body: sidebar + conteúdo principal
        html.Div(
            className="app-content",
            style={
                "display": "flex",
                "flex": "1",
            },
            children=[
                create_sidebar(df),
                create_main_content(),
            ],
        ),
    ],
)

register_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True)
