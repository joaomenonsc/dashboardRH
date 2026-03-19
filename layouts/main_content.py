"""Layout principal com KPIs e gráficos."""

from dash import dcc, html

from config import CARD_STYLE, COLORS


def create_main_content() -> html.Div:
    """Cria a área principal do dashboard.

    Returns:
        Container com KPIs, gráficos e tabela de dados.
    """
    return html.Div(
        style={"flex": "1", "padding": "24px 32px", "overflowY": "auto"},
        children=[
            # KPI cards
            html.Div(
                id="kpi-cards",
                style={
                    "display": "flex",
                    "gap": "16px",
                    "flexWrap": "wrap",
                    "marginBottom": "24px",
                },
            ),
            # Row 1: Headcount + Salary
            _graph_row(
                [
                    _graph_card("chart-headcount"),
                    _graph_card("chart-salary"),
                ],
            ),
            # Row 2: Performance + Turnover
            _graph_row(
                [
                    _graph_card("chart-performance"),
                    _graph_card("chart-turnover"),
                ],
            ),
            # Row 3: Tendência Temporal + Correlação
            _graph_row(
                [
                    _graph_card("chart-timeline"),
                    _graph_card("chart-correlation"),
                ],
            ),
            # Row 4: Manager Analysis + Engagement
            _graph_row(
                [
                    _graph_card("chart-manager"),
                    _graph_card("chart-engagement"),
                ],
            ),
            # Row 5: Diversidade + Recrutamento
            _graph_row(
                [
                    _graph_card("chart-diversity"),
                    _graph_card("chart-recruitment"),
                ],
            ),
            # Row 6: Estado + Benchmarking por Cargo
            _graph_row(
                [
                    _graph_card("chart-state"),
                    _graph_card("chart-position-salary"),
                ],
            ),
            # Row 7: Atrasos vs Performance + Projetos vs Engagement
            _graph_row(
                [
                    _graph_card("chart-lateness"),
                    _graph_card("chart-projects"),
                ],
            ),
            # Row 8: Heatmap + Tenure
            _graph_row(
                [
                    _graph_card("chart-heatmap"),
                    _graph_card("chart-tenure"),
                ],
            ),
            # Tabela de dados
            html.Div(
                style={**CARD_STYLE, "marginBottom": "20px"},
                children=[
                    html.H4(
                        "Dados dos Colaboradores",
                        style={"margin": "0 0 16px 0", "fontSize": "16px"},
                    ),
                    dcc.Loading(
                        type="circle",
                        color=COLORS["accent"],
                        children=html.Div(id="data-table-container"),
                    ),
                ],
            ),
        ],
    )


def _graph_row(children: list[html.Div]) -> html.Div:
    """Monta uma linha responsiva com cards de gráficos.

    Args:
        children: Lista de cards a serem exibidos na linha.

    Returns:
        Linha de layout em grid.
    """
    return html.Div(
        style={
            "display": "grid",
            "gridTemplateColumns": "1fr 1fr",
            "gap": "20px",
            "marginBottom": "20px",
        },
        children=children,
    )


def _graph_card(graph_id: str) -> html.Div:
    """Renderiza um card de gráfico com indicador de carregamento.

    Args:
        graph_id: Identificador do componente `dcc.Graph`.

    Returns:
        Card de layout contendo o gráfico.
    """
    return html.Div(
        style=CARD_STYLE,
        children=[
            dcc.Loading(
                type="circle",
                color=COLORS["accent"],
                children=dcc.Graph(id=graph_id),
            ),
        ],
    )
