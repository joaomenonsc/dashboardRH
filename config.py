"""Configurações globais do dashboard de RH."""

COLORS = {
    "bg": "#0f1117",
    "card": "#1a1c25",
    "sidebar": "#151720",
    "text": "#e0e0e0",
    "accent": "#636efa",
    "accent2": "#ee553b",
    "accent3": "#00cc96",
    "border": "#2a2d3a",
    "muted": "#888",
}

CARD_STYLE = {
    "backgroundColor": COLORS["card"],
    "borderRadius": "8px",
    "padding": "20px",
    "border": f"1px solid {COLORS['border']}",
}

KPI_STYLE = {
    **CARD_STYLE,
    "textAlign": "center",
    "flex": "1",
    "minWidth": "160px",
}

GRAPH_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color=COLORS["text"],
    margin=dict(l=40, r=20, t=40, b=40),
)
