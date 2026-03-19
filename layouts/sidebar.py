"""Sidebar com filtros do dashboard."""

from dash import dcc, html
import pandas as pd

from config import COLORS


def create_sidebar(df: pd.DataFrame) -> html.Div:
    """Cria a barra lateral com filtros e ação de exportação.

    Args:
        df: DataFrame já tratado com os dados de RH.

    Returns:
        Componente de layout da barra lateral.
    """
    min_date = df["DateofHire"].min()
    max_date = df["DateofHire"].max()

    return html.Div(
        style={
            "width": "260px",
            "backgroundColor": COLORS["sidebar"],
            "padding": "24px 20px",
            "borderRight": f"1px solid {COLORS['border']}",
            "flexShrink": "0",
            "overflowY": "auto",
        },
        children=[
            html.H2(
                "B.I. de RH",
                style={
                    "color": COLORS["accent"],
                    "marginBottom": "8px",
                    "fontSize": "22px",
                },
            ),
            html.P(
                "Dashboard de People Analytics",
                style={"color": COLORS["muted"], "fontSize": "13px", "marginBottom": "32px"},
            ),
            # Filtro Departamento
            _filter_label("Departamento"),
            dcc.Dropdown(
                id="filter-dept",
                options=[{"label": d, "value": d} for d in sorted(df["Department"].unique())],
                multi=True,
                placeholder="Todos",
                style={"marginBottom": "20px"},
            ),
            # Filtro Gênero
            _filter_label("Gênero"),
            dcc.Dropdown(
                id="filter-gender",
                options=[{"label": s, "value": s} for s in sorted(df["Sex"].unique())],
                placeholder="Todos",
                style={"marginBottom": "20px"},
            ),
            # Filtro Status
            _filter_label("Status"),
            dcc.Dropdown(
                id="filter-status",
                options=[{"label": s, "value": s} for s in sorted(df["EmploymentStatus"].unique())],
                placeholder="Todos",
                style={"marginBottom": "20px"},
            ),
            # Filtro Gestor
            _filter_label("Gestor"),
            dcc.Dropdown(
                id="filter-manager",
                options=[{"label": m, "value": m} for m in sorted(df["ManagerName"].unique())],
                placeholder="Todos",
                style={"marginBottom": "20px"},
            ),
            # Filtro Período
            _filter_label("Período de Contratação"),
            dcc.DatePickerRange(
                id="filter-date-range",
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                display_format="DD/MM/YYYY",
                style={"marginBottom": "20px"},
            ),
            # Botão de export
            html.Hr(style={"borderColor": COLORS["border"], "margin": "20px 0"}),
            html.Button(
                "Exportar CSV",
                id="btn-export",
                n_clicks=0,
                style={
                    "width": "100%",
                    "padding": "10px",
                    "backgroundColor": COLORS["accent"],
                    "color": "#fff",
                    "border": "none",
                    "borderRadius": "6px",
                    "cursor": "pointer",
                    "fontSize": "13px",
                    "fontWeight": "600",
                },
            ),
            dcc.Download(id="download-csv"),
        ],
    )


def _filter_label(text: str) -> html.Label:
    """Renderiza o rótulo padrão usado nos filtros.

    Args:
        text: Texto exibido no rótulo.

    Returns:
        Componente de rótulo formatado.
    """
    return html.Label(
        text,
        style={
            "fontWeight": "600",
            "fontSize": "13px",
            "marginBottom": "6px",
            "display": "block",
        },
    )
