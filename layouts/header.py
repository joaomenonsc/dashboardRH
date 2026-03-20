"""Header fixo do dashboard B.I. de RH."""

from dash import html  # type: ignore
import pandas as pd  # type: ignore

from config import COLORS, SPACING, TYPE_SCALE  # type: ignore


def create_header(df: pd.DataFrame) -> html.Header:
    """Cria o header fixo no topo do dashboard.

    Args:
        df: DataFrame com os dados de RH para exibir total e data.

    Returns:
        Componente de header com título, subtítulo e info contextual.
    """
    total = len(df)
    last_date = df["DateofHire"].max().strftime("%d/%m/%Y") if len(df) > 0 else "—"

    return html.Header(
        className="app-header",
        children=[
            # --- Identidade ---
            html.Div(
                children=[
                    html.H1(
                        "B.I. de RH",
                        style={
                            "margin": "0",
                            "fontSize": TYPE_SCALE["xl"],
                            "color": COLORS["accent"],
                            "fontWeight": "700",
                            "letterSpacing": "-0.5px",
                        },
                    ),
                    html.P(
                        "People Analytics Dashboard",
                        style={
                            "margin": "2px 0 0 0",
                            "fontSize": TYPE_SCALE["sm"],
                            "color": COLORS["muted"],
                        },
                    ),
                ]
            ),
            # --- Info contextual ---
            html.Div(
                style={"textAlign": "right"},
                children=[
                    html.P(
                        f"👥 {total} colaboradores",
                        style={
                            "margin": "0",
                            "fontSize": TYPE_SCALE["sm"],
                            "color": COLORS["text-secondary"],
                            "fontWeight": "600",
                        },
                    ),
                    html.P(
                        f"Última contratação: {last_date}",
                        style={
                            "margin": "2px 0 0 0",
                            "fontSize": TYPE_SCALE["xs"],
                            "color": COLORS["muted"],
                        },
                    ),
                ],
            ),
        ],
    )


def create_context_bar() -> html.Div:
    """Cria a barra de contexto com chips informativos dos filtros ativos.

    Returns:
        Barra de contexto que é atualizada por callback.
    """
    return html.Div(
        id="context-bar",
        className="context-bar",
        style={"display": "none"},  # oculta quando não há filtros
        children=[
            html.Span(
                "Filtros ativos:",
                style={
                    "fontSize": TYPE_SCALE["xs"],
                    "color": COLORS["muted"],
                    "marginRight": SPACING["xs"],
                    "whiteSpace": "nowrap",
                },
            ),
            html.Div(id="context-chips", style={"display": "flex", "flexWrap": "wrap", "gap": SPACING["xs"]}),
        ],
    )
