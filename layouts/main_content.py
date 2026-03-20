"""Layout principal com KPIs, tabs e gráficos."""

from dash import dcc, html

from config import CARD_STYLE, COLORS, SPACING, TYPE_SCALE


# --- Subtítulos por gráfico (F2.8) ---
GRAPH_SUBTITLES = {
    "chart-headcount":      ("Headcount por Departamento",          "Distribuição de colaboradores por área"),
    "chart-salary":         ("Distribuição Salarial",               "Faixas salariais e outliers por departamento"),
    "chart-timeline":       ("Tendência: Contratações vs Saídas",   "Evolução mensal de entradas e desligamentos"),
    "chart-heatmap":        ("Correlações entre Variáveis",         "Intensidade das correlações entre 6 variáveis-chave"),
    "chart-performance":    ("Distribuição de Performance",         "Proporção de scores de avaliação"),
    "chart-lateness":       ("Atrasos vs Performance",              "Impacto dos atrasos no score de performance"),
    "chart-engagement":     ("Distribuição de Engagement",          "Frequência de scores da pesquisa de engajamento"),
    "chart-projects":       ("Projetos Especiais vs Engagement",    "Relação entre projetos especiais e engajamento"),
    "chart-diversity":      ("Diversidade — Raça e Gênero",        "Composição étnica e de gênero da organização"),
    "chart-state":          ("Distribuição Geográfica",             "Presença regional e concentração por estado"),
    "chart-position-salary":("Benchmarking Salarial por Cargo",    "Comparativo salarial entre posições (min. 3 ocupantes)"),
    "chart-tenure":         ("Tempo de Permanência",                "Tempo médio até desligamento — identificar riscos"),
    "chart-turnover":       ("Motivos de Desligamento",             "Principais causas de saída voluntária e involuntária"),
    "chart-recruitment":    ("Canais de Recrutamento",              "Volume de contratações por canal de origem"),
    "chart-manager":        ("Turnover por Gestor",                 "Taxa de desligamento por líder (min. 3 liderados)"),
    "chart-correlation":    ("Satisfação vs Engagement",            "Relação entre satisfação e engajamento por status"),
}


def create_main_content() -> html.Div:
    """Cria a área principal do dashboard com tabs temáticas.

    Returns:
        Container com KPIs sempre visíveis e 4 abas de conteúdo.
    """
    return html.Div(
        style={"flex": "1", "overflowY": "auto", "display": "flex", "flexDirection": "column"},
        children=[
            # --- KPI Cards (sempre visíveis, acima das tabs) ---
            html.Div(
                id="kpi-cards",
                style={
                    "display": "flex",
                    "gap": SPACING["md"],
                    "flexWrap": "wrap",
                    "padding": f"{SPACING['lg']} {SPACING['xl']}",
                    "borderBottom": f"1px solid {COLORS['border']}",
                    "backgroundColor": COLORS["bg"],
                },
            ),

            # --- Toast de notificação (F3.5) ---
            html.Div(
                id="toast-container",
                className="toast-container",
                children=[
                    html.Div(id="toast-message", className="toast", style={"display": "none"}),
                ],
            ),

            # --- Tabs Temáticas (F2.1) ---
            html.Div(
                style={"flex": "1", "padding": f"0 {SPACING['xl']} {SPACING['xl']}"},
                children=[
                    dcc.Tabs(
                        id="main-tabs",
                        value="overview",
                        className="custom-tabs",
                        style={"marginTop": SPACING["md"]},
                        colors={
                            "border": COLORS["border"],
                            "primary": COLORS["accent"],
                            "background": COLORS["sidebar"],
                        },
                        children=[
                            dcc.Tab(label="🏠 Visão Geral",          value="overview",    className="tab"),
                            dcc.Tab(label="🎯 Performance",           value="performance", className="tab"),
                            dcc.Tab(label="👥 Pessoas",               value="people",      className="tab"),
                            dcc.Tab(label="📋 Recrutamento & Turnover", value="recruitment", className="tab"),
                        ],
                    ),

                    # --- Conteúdo das Abas ---
                    html.Div(id="tab-content"),
                ],
            ),
        ],
    )


# ---------- Conteúdo das abas (chamado pelos callbacks) ----------

def build_tab_overview() -> html.Div:
    """Aba Visão Geral: Headcount, Salário, Tendência, Heatmap, Tabela."""
    return html.Div(
        style={"marginTop": SPACING["md"]},
        children=[
            _graph_row([
                _graph_card("chart-headcount"),
                _graph_card("chart-salary"),
            ]),
            _graph_row([
                _graph_card("chart-timeline"),
                _graph_card("chart-heatmap"),
            ]),
            # Tabela sempre na visão geral
            html.Div(
                style={**CARD_STYLE, "marginTop": SPACING["md"]},
                children=[
                    html.H4(
                        "Dados dos Colaboradores",
                        style={
                            "margin": f"0 0 {SPACING['md']} 0",
                            "fontSize": TYPE_SCALE["lg"],
                            "color": COLORS["text"],
                        },
                    ),
                    html.P(
                        "Tabela completa com todos os colaboradores do recorte atual.",
                        style={"color": COLORS["muted"], "fontSize": TYPE_SCALE["xs"], "margin": f"0 0 {SPACING['md']} 0"},
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


def build_tab_performance() -> html.Div:
    """Aba Performance: Performance Score, Atrasos, Engagement, Projetos."""
    return html.Div(
        style={"marginTop": SPACING["md"]},
        children=[
            _graph_row([
                _graph_card("chart-performance"),
                _graph_card("chart-lateness"),
            ]),
            _graph_row([
                _graph_card("chart-engagement"),
                _graph_card("chart-projects"),
            ]),
        ],
    )


def build_tab_people() -> html.Div:
    """Aba Pessoas: Diversidade, Geográfico, Benchmarking, Tenure."""
    return html.Div(
        style={"marginTop": SPACING["md"]},
        children=[
            _graph_row([
                _graph_card("chart-diversity"),
                _graph_card("chart-state"),
            ]),
            _graph_row([
                _graph_card("chart-position-salary"),
                _graph_card("chart-tenure"),
            ]),
        ],
    )


def build_tab_recruitment() -> html.Div:
    """Aba Recrutamento & Turnover: Motivos, Canais, Gestor, Correlação."""
    return html.Div(
        style={"marginTop": SPACING["md"]},
        children=[
            _graph_row([
                _graph_card("chart-turnover"),
                _graph_card("chart-recruitment"),
            ]),
            _graph_row([
                _graph_card("chart-manager"),
                _graph_card("chart-correlation"),
            ]),
        ],
    )


# ---------- Helpers privados ----------

def _graph_row(children: list) -> html.Div:
    """Linha responsiva de 2 cards de gráfico."""
    return html.Div(
        className="graph-grid",
        style={
            "display": "grid",
            "gridTemplateColumns": "1fr 1fr",
            "gap": SPACING["md"],
            "marginBottom": SPACING["md"],
        },
        children=children,
    )


def _graph_card(graph_id: str) -> html.Div:
    """Card de gráfico com título, subtítulo e indicador de loading."""
    title, subtitle = GRAPH_SUBTITLES.get(graph_id, (graph_id, ""))
    return html.Div(
        className="graph-card",
        style=CARD_STYLE,
        children=[
            html.H4(
                title,
                style={
                    "margin": f"0 0 {SPACING['xs']} 0",
                    "fontSize": TYPE_SCALE["md"],
                    "color": COLORS["text"],
                    "fontWeight": "600",
                },
            ),
            html.P(
                subtitle,
                style={
                    "margin": f"0 0 {SPACING['sm']} 0",
                    "fontSize": TYPE_SCALE["xs"],
                    "color": COLORS["muted"],
                },
            ),
            dcc.Loading(
                type="circle",
                color=COLORS["accent"],
                children=dcc.Graph(
                    id=graph_id,
                    config={"displayModeBar": False},
                ),
            ),
        ],
    )
