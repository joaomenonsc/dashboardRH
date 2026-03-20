"""Configurações globais do dashboard de RH."""

# --- Spacing Scale (base 4px) --- F0.1
SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px",
    "2xl": "48px",
}

# --- Type Scale (ratio 1.25 - Major Third) --- F0.2
TYPE_SCALE = {
    "xs": "11px",   # labels, captions
    "sm": "13px",   # body small, filter labels
    "md": "15px",   # body default
    "lg": "18px",   # section titles
    "xl": "22px",   # page titles
    "2xl": "28px",  # KPI values
    "3xl": "34px",  # hero numbers
}

# --- Semantic Colors --- F0.3
COLORS = {
    # Surface
    "bg": "#0f1117",
    "card": "#1a1c25",
    "card-hover": "#22252f",
    "sidebar": "#151720",
    "border": "#2a2d3a",
    # Text
    "text": "#e0e0e0",
    "text-secondary": "#a0a0a0",
    "muted": "#888",
    # Brand
    "accent": "#636efa",
    "accent-hover": "#7b83fb",
    # Semantic
    "success": "#00cc96",
    "warning": "#ffa15a",
    "danger": "#ee553b",
    "info": "#19d3f3",
    # Aliases para compatibilidade com código existente
    "accent2": "#ee553b",
    "accent3": "#00cc96",
}

# --- Chart Color Palette (Plotly-style, WCAG AA on dark bg) --- F0.4
CHART_COLORS = [
    "#636efa",  # azul (accent principal)
    "#ee553b",  # vermelho
    "#00cc96",  # verde
    "#ab63fa",  # roxo
    "#ffa15a",  # laranja
    "#19d3f3",  # ciano
    "#ff6692",  # rosa
    "#b6e880",  # verde claro
    "#ff97ff",  # magenta
    "#fecb52",  # amarelo
]

# --- Card / Graph Styles ---
CARD_STYLE = {
    "backgroundColor": COLORS["card"],
    "borderRadius": "8px",
    "padding": SPACING["lg"],
    "border": f"1px solid {COLORS['border']}",
}

KPI_STYLE = {
    **CARD_STYLE,
    "textAlign": "center",
    "flex": "1",
    "minWidth": "160px",
}

GRAPH_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font_color": COLORS["text"],
    "margin": {"l": 40, "r": 20, "t": 40, "b": 40},
}
