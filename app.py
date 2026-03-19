"""Dashboard B.I. de RH — Ponto de entrada."""

import dash
from dash import html

from config import COLORS
from data.loader import load_data
from layouts.sidebar import create_sidebar
from layouts.main_content import create_main_content
from callbacks.dashboard import register_callbacks

# --- Data ---
df = load_data()

# --- App ---
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "B.I. de RH"

app.layout = html.Div(
    style={
        "display": "flex",
        "minHeight": "100vh",
        "backgroundColor": COLORS["bg"],
        "fontFamily": "'Segoe UI', sans-serif",
        "color": COLORS["text"],
    },
    children=[
        create_sidebar(df),
        create_main_content(),
    ],
)

register_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True)
