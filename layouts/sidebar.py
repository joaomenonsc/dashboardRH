"""Sidebar com filtros do dashboard."""

from dash import dcc, html  # type: ignore
import pandas as pd  # type: ignore

from config import COLORS, SPACING, TYPE_SCALE  # type: ignore

# Estilo base para inputs nativos de data
_DATE_INPUT_STYLE = {
    "width": "100%",
    "padding": "7px 10px",
    "backgroundColor": "#0f1117",
    "color": "#e0e0e0",
    "border": "1px solid #2a2d3a",
    "borderRadius": "4px",
    "fontSize": "13px",
    "colorScheme": "dark",
}


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
        className="sidebar",
        style={
            "width": "260px",
            "backgroundColor": COLORS["sidebar"],
            "padding": f"{SPACING['lg']} {SPACING['md']}",
            "borderRight": f"1px solid {COLORS['border']}",
            "flexShrink": "0",
            "overflowY": "auto",
            "display": "flex",
            "flexDirection": "column",
        },
        children=[
            # --- Badge de filtros ativos + Botão Limpar (F3.1 / F3.2) ---
            html.Div(
                id="filter-badge-container",
                style={"marginBottom": SPACING["sm"], "display": "none"},
                children=[
                    html.Span(
                        id="filter-badge-text",
                        className="filter-badge",
                    ),
                    html.Button(
                        "Limpar",
                        id="btn-clear-filters",
                        n_clicks=0,
                        className="btn-ghost",
                        style={"marginLeft": SPACING["xs"]},
                    ),
                ],
            ),

            # --- Seção: Filtros ---
            _section_label("Filtros"),
            _filter_label("Departamento"),
            dcc.Dropdown(
                id="filter-dept",
                options=[{"label": d, "value": d} for d in sorted(df["Department"].unique())],
                multi=True,
                placeholder="Todos",
                style={"marginBottom": SPACING["md"]},
            ),
            _filter_label("Gênero"),
            dcc.Dropdown(
                id="filter-gender",
                options=[{"label": s, "value": s} for s in sorted(df["Sex"].unique())],
                placeholder="Todos",
                style={"marginBottom": SPACING["md"]},
            ),
            _filter_label("Status"),
            dcc.Dropdown(
                id="filter-status",
                options=[{"label": s, "value": s} for s in sorted(df["EmploymentStatus"].unique())],
                placeholder="Todos",
                style={"marginBottom": SPACING["md"]},
            ),
            _filter_label("Gestor"),
            dcc.Dropdown(
                id="filter-manager",
                options=[{"label": m, "value": m} for m in sorted(df["ManagerName"].unique())],
                placeholder="Todos",
                style={"marginBottom": SPACING["md"]},
            ),

            # --- Seção: Período ---
            _section_label("Período"),
            _filter_label("Data inicial (AAAA-MM-DD)"),
            dcc.Input(
                id="filter-date-start",
                type="text",
                placeholder="ex: 2005-01-01",
                debounce=True,
                style={**_DATE_INPUT_STYLE, "marginBottom": SPACING["sm"]},
            ),
            _filter_label("Data final (AAAA-MM-DD)"),
            dcc.Input(
                id="filter-date-end",
                type="text",
                placeholder="ex: 2024-12-31",
                debounce=True,
                style={**_DATE_INPUT_STYLE, "marginBottom": SPACING["sm"]},
            ),

            # Atalhos de data rápidos (F3.6)
            html.Div(
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "gap": SPACING["xs"],
                    "marginBottom": SPACING["md"],
                    "marginTop": SPACING["xs"],
                },
                children=[
                    _date_shortcut_btn("30d", "Últimos 30d"),
                    _date_shortcut_btn("90d", "Últimos 90d"),
                    _date_shortcut_btn("1y", "Último ano"),
                    _date_shortcut_btn("all", "Tudo"),
                ],
            ),

            # Espaço flexível para empurrar export para baixo
            html.Div(style={"flex": "1"}),

            # --- Seção: Ações (sticky no rodapé) ---
            html.Div(
                className="sidebar-export-footer",
                children=[
                    _section_label("Ações"),
                    html.Button(
                        "⬇ Exportar CSV",
                        id="btn-export",
                        n_clicks=0,
                        className="btn-primary",
                        style={
                            "width": "100%",
                            "padding": f"{SPACING['sm']} {SPACING['md']}",
                            "backgroundColor": COLORS["accent"],
                            "color": "#fff",
                            "border": "none",
                            "borderRadius": "6px",
                            "cursor": "pointer",
                            "fontSize": TYPE_SCALE["sm"],
                            "fontWeight": "600",
                        },
                    ),
                    dcc.Download(id="download-csv"),
                ],
            ),
        ],
    )


def _section_label(text: str) -> html.Span:
    """Rótulo de seção da sidebar."""
    return html.Span(text, className="sidebar-section-label")


def _date_shortcut_btn(btn_id: str, label: str) -> html.Button:
    """Botão de atalho de período para o DatePicker."""
    return html.Button(
        label,
        id=f"btn-date-{btn_id}",
        n_clicks=0,
        className="btn-ghost",
        style={"fontSize": "11px", "padding": "3px 7px"},
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
            "fontSize": TYPE_SCALE["sm"],
            "marginBottom": SPACING["xs"],
            "display": "block",
            "color": COLORS["text-secondary"],
        },
    )
