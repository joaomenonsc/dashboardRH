"""Callbacks do dashboard de RH — separados por aba."""

import datetime

import dash  # type: ignore
from dash import Input, Output, State, html, dash_table, ctx  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
from plotly.basedatatypes import BaseFigure  # type: ignore

from config import COLORS, GRAPH_LAYOUT, KPI_STYLE, CHART_COLORS, SPACING, TYPE_SCALE  # type: ignore
from data.loader import filter_data  # type: ignore
from layouts.main_content import (  # type: ignore
    build_tab_overview,
    build_tab_performance,
    build_tab_people,
    build_tab_recruitment,
)

# --- Inputs compartilhados entre todos os callbacks de filtro ---
FILTER_INPUTS = [
    Input("filter-dept",       "value"),
    Input("filter-gender",     "value"),
    Input("filter-status",     "value"),
    Input("filter-manager",    "value"),
    Input("filter-date-start", "value"),
    Input("filter-date-end",   "value"),
]

FILTER_STATES = [
    State("filter-dept",       "value"),
    State("filter-gender",     "value"),
    State("filter-status",     "value"),
    State("filter-manager",    "value"),
    State("filter-date-start", "value"),
    State("filter-date-end",   "value"),
]


def _parse_filters(dept, gender, status, manager, start_date, end_date):
    """Normaliza os filtros recebidos da interface."""
    date_range = [start_date, end_date] if start_date and end_date else None
    return dept, gender, status, date_range, manager


def _has_filters(dept, gender, status, manager, date_range) -> bool:
    return any([dept, gender, status, manager, date_range])


def register_callbacks(app: dash.Dash, df: pd.DataFrame) -> None:
    """Registra todos os callbacks da aplicação."""

    # =====================================================================
    # F2.2 — KPIs (sempre visíveis, independente da aba)
    # F1.6 — Hierarquia tipográfica melhorada
    # F3.4 — Delta exibe "—" quando sem filtros
    # F4.1 — Ícones Unicode nos KPIs
    # =====================================================================
    @app.callback(
        Output("kpi-cards", "children"),
        *FILTER_INPUTS,
    )
    def update_kpis(dept, gender, status, manager, start_date, end_date):
        dept, gender, status, date_range, manager = _parse_filters(
            dept, gender, status, manager, start_date, end_date
        )
        filtered = filter_data(df, dept, gender, status, date_range, manager)
        has_f = _has_filters(dept, gender, status, manager, date_range)
        return _build_kpis(filtered, df if has_f else None)

    # =====================================================================
    # F2.1 — Renderiza conteúdo da aba selecionada
    # =====================================================================
    @app.callback(
        Output("tab-content", "children"),
        Input("main-tabs", "value"),
    )
    def render_tab_content(tab):
        if tab == "overview":
            return build_tab_overview()
        elif tab == "performance":
            return build_tab_performance()
        elif tab == "people":
            return build_tab_people()
        elif tab == "recruitment":
            return build_tab_recruitment()
        return build_tab_overview()

    # =====================================================================
    # F2.3 — Aba Visão Geral: Headcount, Salary, Timeline, Heatmap, Tabela
    # =====================================================================
    @app.callback(
        Output("chart-headcount",      "figure"),
        Output("chart-salary",         "figure"),
        Output("chart-timeline",       "figure"),
        Output("chart-heatmap",        "figure"),
        Output("data-table-container", "children"),
        Input("main-tabs", "value"),
        *FILTER_INPUTS,
    )
    def update_tab_overview(tab, dept, gender, status, manager, start_date, end_date):
        if tab != "overview":
            return (dash.no_update,) * 5
        dept, gender, status, date_range, manager = _parse_filters(
            dept, gender, status, manager, start_date, end_date
        )
        filtered = filter_data(df, dept, gender, status, date_range, manager)
        return (
            _chart_headcount(filtered),
            _chart_salary(filtered),
            _chart_timeline(filtered),
            _chart_heatmap(filtered),
            _build_data_table(filtered),
        )

    # =====================================================================
    # F2.4 — Aba Performance: Performance, Lateness, Engagement, Projects
    # =====================================================================
    @app.callback(
        Output("chart-performance", "figure"),
        Output("chart-lateness",    "figure"),
        Output("chart-engagement",  "figure"),
        Output("chart-projects",    "figure"),
        Input("main-tabs", "value"),
        *FILTER_INPUTS,
    )
    def update_tab_performance(tab, dept, gender, status, manager, start_date, end_date):
        if tab != "performance":
            return (dash.no_update,) * 4
        dept, gender, status, date_range, manager = _parse_filters(
            dept, gender, status, manager, start_date, end_date
        )
        filtered = filter_data(df, dept, gender, status, date_range, manager)
        return (
            _chart_performance(filtered),
            _chart_lateness(filtered),
            _chart_engagement(filtered),
            _chart_projects(filtered),
        )

    # =====================================================================
    # F2.5 — Aba Pessoas: Diversity, State, Position Salary, Tenure
    # =====================================================================
    @app.callback(
        Output("chart-diversity",       "figure"),
        Output("chart-state",           "figure"),
        Output("chart-position-salary", "figure"),
        Output("chart-tenure",          "figure"),
        Input("main-tabs", "value"),
        *FILTER_INPUTS,
    )
    def update_tab_people(tab, dept, gender, status, manager, start_date, end_date):
        if tab != "people":
            return (dash.no_update,) * 4
        dept, gender, status, date_range, manager = _parse_filters(
            dept, gender, status, manager, start_date, end_date
        )
        filtered = filter_data(df, dept, gender, status, date_range, manager)
        return (
            _chart_diversity(filtered),
            _chart_state(filtered),
            _chart_position_salary(filtered),
            _chart_tenure(filtered),
        )

    # =====================================================================
    # F2.6 — Aba Recrutamento: Turnover, Recruitment, Manager, Correlation
    # =====================================================================
    @app.callback(
        Output("chart-turnover",    "figure"),
        Output("chart-recruitment", "figure"),
        Output("chart-manager",     "figure"),
        Output("chart-correlation", "figure"),
        Input("main-tabs", "value"),
        *FILTER_INPUTS,
    )
    def update_tab_recruitment(tab, dept, gender, status, manager, start_date, end_date):
        if tab != "recruitment":
            return (dash.no_update,) * 4
        dept, gender, status, date_range, manager = _parse_filters(
            dept, gender, status, manager, start_date, end_date
        )
        filtered = filter_data(df, dept, gender, status, date_range, manager)
        return (
            _chart_turnover(filtered),
            _chart_recruitment(filtered),
            _chart_manager(filtered),
            _chart_correlation(filtered),
        )

    # =====================================================================
    # F3.1 — Badge de filtros ativos
    # F3.2 — Limpar filtros
    # F3.3 — Context bar com chips informativos
    # =====================================================================
    @app.callback(
        Output("filter-badge-container", "style"),
        Output("filter-badge-text",      "children"),
        Output("context-bar",            "style"),
        Output("context-chips",          "children"),
        *FILTER_INPUTS,
    )
    def update_filter_ui(dept, gender, status, manager, start_date, end_date):
        active = []
        if dept:
            label = ", ".join(dept) if isinstance(dept, list) else dept
            active.append(("Departamento", label))
        if gender:
            active.append(("Gênero", gender))
        if status:
            active.append(("Status", status))
        if manager:
            active.append(("Gestor", manager))
        if start_date and end_date:
            active.append(("Período", f"{start_date[:10]} → {end_date[:10]}"))

        n = len(active)

        if n == 0:
            badge_style = {"marginBottom": SPACING["sm"], "display": "none"}
            bar_style   = {"display": "none"}
            chips       = []
        else:
            badge_style = {"marginBottom": SPACING["sm"], "display": "flex", "alignItems": "center"}
            bar_style   = {
                "display": "flex",
                "flexWrap": "wrap",
                "gap": SPACING["xs"],
                "alignItems": "center",
                "padding": f"{SPACING['sm']} {SPACING['xl']}",
                "backgroundColor": "#12141c",
                "borderBottom": f"1px solid {COLORS['border']}",
                "minHeight": "38px",
            }
            chips = [
                html.Span(
                    f"{k}: {v}",
                    className="filter-chip",
                )
                for k, v in active
            ]

        badge_text = f"{n} filtro{'s' if n != 1 else ''} ativo{'s' if n != 1 else ''}"
        return badge_style, badge_text, bar_style, chips

    @app.callback(
        Output("filter-dept",       "value"),
        Output("filter-gender",     "value"),
        Output("filter-status",     "value"),
        Output("filter-manager",    "value"),
        Output("filter-date-start", "value"),
        Output("filter-date-end",   "value"),
        Input("btn-clear-filters",  "n_clicks"),
        prevent_initial_call=True,
    )
    def clear_filters(n_clicks):
        return [], None, None, None, None, None

    # =====================================================================
    # F3.5 — Toast de feedback para export CSV
    # =====================================================================
    @app.callback(
        Output("download-csv",    "data"),
        Output("toast-message",   "children"),
        Output("toast-message",   "style"),
        Input("btn-export",       "n_clicks"),
        *FILTER_STATES,
        prevent_initial_call=True,
    )
    def export_csv(n_clicks, dept, gender, status, manager, start_date, end_date):
        if not n_clicks or ctx.triggered_id != "btn-export":
            return dash.no_update, dash.no_update, dash.no_update
        dept, gender, status, date_range, manager = _parse_filters(
            dept, gender, status, manager, start_date, end_date
        )
        filtered = filter_data(df, dept, gender, status, date_range, manager)
        toast_text = f"✅ CSV exportado com sucesso ({len(filtered)} registros)"
        toast_style = {"display": "block"}
        return (
            dict(content=filtered.to_csv(index=False), filename="dados_rh_filtrados.csv"),
            toast_text,
            toast_style,
        )

    # =====================================================================
    # F3.6 — Atalhos rápidos de data para o DatePicker
    # =====================================================================
    @app.callback(
        Output("filter-date-start", "value", allow_duplicate=True),
        Output("filter-date-end",   "value", allow_duplicate=True),
        Input("btn-date-30d",  "n_clicks"),
        Input("btn-date-90d",  "n_clicks"),
        Input("btn-date-1y",   "n_clicks"),
        Input("btn-date-all",  "n_clicks"),
        prevent_initial_call=True,
    )
    def set_date_shortcut(n_30d, n_90d, n_1y, n_all):
        triggered = ctx.triggered_id
        today = datetime.date.today()
        max_date = df["DateofHire"].max().date()
        min_date = df["DateofHire"].min().date()

        if triggered == "btn-date-30d":
            return str(today - datetime.timedelta(days=30)), str(today)
        elif triggered == "btn-date-90d":
            return str(today - datetime.timedelta(days=90)), str(today)
        elif triggered == "btn-date-1y":
            return str(today - datetime.timedelta(days=365)), str(today)
        elif triggered == "btn-date-all":
            return str(min_date), str(max_date)
        return dash.no_update, dash.no_update


# =========================================================================
# KPIs (F1.6 + F3.4 + F4.1)
# =========================================================================

def _kpi_card(
    icon: str,
    title: str,
    value: str,
    tooltip: str | None = None,
    delta: float | None = None,
    unit: str = "",
) -> html.Div:
    """Cria um card de KPI com ícone, valor e delta."""
    children = [
        html.P(
            f"{icon}  {title}",
            style={
                "color": COLORS["muted"],
                "fontSize": TYPE_SCALE["xs"],
                "margin": f"0 0 {SPACING['xs']} 0",
                "textTransform": "uppercase",
                "letterSpacing": "0.5px",
                "fontWeight": "600",
            },
            title=tooltip,
        ),
        html.H3(
            value,
            style={
                "margin": "0",
                "fontSize": TYPE_SCALE["2xl"],
                "color": COLORS["accent"],
                "fontWeight": "700",
                "lineHeight": "1",
            },
        ),
    ]

    # F3.4: delta "—" quando sem filtros
    if delta is not None:
        is_pos = delta > 0
        arrow = "▲" if is_pos else "▼" if delta < 0 else "–"
        color = COLORS["danger"] if is_pos else COLORS["success"] if delta < 0 else COLORS["muted"]
        children.append(
            html.P(
                f"{arrow} {abs(delta):.1f}{unit} vs geral",
                style={
                    "color": color,
                    "fontSize": TYPE_SCALE["xs"],
                    "margin": f"{SPACING['xs']} 0 0 0",
                    "fontWeight": "500",
                },
            )
        )
    else:
        children.append(
            html.P(
                "— vs geral",
                title="Aplique filtros para comparar com a base completa",
                style={
                    "color": COLORS["muted"],
                    "fontSize": TYPE_SCALE["xs"],
                    "margin": f"{SPACING['xs']} 0 0 0",
                },
            )
        )

    return html.Div(className="kpi-card", style=KPI_STYLE, children=children)


def _build_kpis(filtered: pd.DataFrame, full_df: pd.DataFrame | None = None) -> list:
    total = len(filtered)
    if total == 0:
        return [html.P("Nenhum dado para os filtros selecionados.", style={"color": COLORS["muted"]})]

    turnover     = (filtered["Termd"].sum() / total * 100)
    avg_salary   = filtered["Salary"].mean()
    avg_sat      = filtered["EmpSatisfaction"].mean()
    avg_eng      = filtered["EngagementSurvey"].mean()
    avg_abs      = filtered["Absences"].mean()

    if full_df is not None and len(full_df) > 0:
        g_total    = len(full_df)
        d_turnover = turnover   - (full_df["Termd"].sum() / g_total * 100)
        d_salary   = avg_salary - full_df["Salary"].mean()
        d_sat      = avg_sat    - full_df["EmpSatisfaction"].mean()
        d_eng      = avg_eng    - full_df["EngagementSurvey"].mean()
        d_abs      = avg_abs    - full_df["Absences"].mean()
    else:
        d_turnover = d_salary = d_sat = d_eng = d_abs = None

    return [
        _kpi_card("👥", "Colaboradores", f"{total}",                "Total de colaboradores no filtro atual"),
        _kpi_card("📉", "Turnover",      f"{turnover:.1f}%",        "Percentual de desligamentos sobre o total",   d_turnover, "%"),
        _kpi_card("💰", "Salário Médio", f"${avg_salary:,.0f}",     "Média salarial dos colaboradores filtrados",  d_salary,   ""),
        _kpi_card("😊", "Satisfação",    f"{avg_sat:.1f}/5",        "Média da pesquisa de satisfação (1-5)",       d_sat,      ""),
        _kpi_card("🎯", "Engagement",    f"{avg_eng:.2f}",          "Média da pesquisa de engajamento",            d_eng,      ""),
        _kpi_card("📅", "Absências",     f"{avg_abs:.1f}d",         "Média de dias de ausência por colaborador",   d_abs,      "d"),
    ]


# =========================================================================
# Gráficos — F0.7 (CHART_COLORS) + F2.9 (estados vazios melhorados)
# =========================================================================

def _empty_state(message: str, suggestion: str = "Tente ajustar os filtros.") -> BaseFigure:
    """Estado vazio visual: ícone + mensagem + sugestão (F2.9)."""
    fig = go.Figure()
    fig.add_annotation(
        text=f"🔍  {message}",
        showarrow=False,
        font=dict(size=16, color=COLORS["text-secondary"]),
        xref="paper", yref="paper", x=0.5, y=0.55,
    )
    fig.add_annotation(
        text=suggestion,
        showarrow=False,
        font=dict(size=12, color=COLORS["muted"]),
        xref="paper", yref="paper", x=0.5, y=0.42,
    )
    fig.update_layout(**GRAPH_LAYOUT)
    return fig


def _chart_headcount(filtered: pd.DataFrame) -> BaseFigure:
    if len(filtered) == 0:
        return _empty_state("Nenhum colaborador encontrado.")
    dept_counts = filtered.groupby("Department").size().reset_index(name="count").sort_values("count")
    fig = px.bar(
        dept_counts, x="count", y="Department", orientation="h",
        color_discrete_sequence=[CHART_COLORS[0]],
    )
    fig.update_layout(**GRAPH_LAYOUT, yaxis_title="", xaxis_title="Colaboradores")
    return fig


def _chart_salary(filtered: pd.DataFrame) -> BaseFigure:
    if len(filtered) == 0:
        return _empty_state("Nenhum dado de salário encontrado.")
    fig = px.box(
        filtered, x="Department", y="Salary",
        color_discrete_sequence=[CHART_COLORS[0]],
    )
    fig.update_layout(**GRAPH_LAYOUT, xaxis_title="", yaxis_title="Salário (USD)")
    return fig


def _chart_performance(filtered: pd.DataFrame) -> BaseFigure:
    if len(filtered) == 0:
        return _empty_state("Nenhum dado de performance encontrado.")
    perf_counts = filtered.groupby("PerformanceScore").size().reset_index(name="count")
    fig = px.pie(
        perf_counts, values="count", names="PerformanceScore",
        color_discrete_sequence=CHART_COLORS,
    )
    fig.update_layout(**GRAPH_LAYOUT)
    return fig


def _chart_turnover(filtered: pd.DataFrame) -> BaseFigure:
    termed = filtered[filtered["Termd"] == 1]
    if len(termed) == 0:
        return _empty_state("Sem dados de desligamento.", "Selecione colaboradores com status desligado.")
    reasons = termed.groupby("TermReason").size().reset_index(name="count").sort_values("count")
    fig = px.bar(
        reasons, x="count", y="TermReason", orientation="h",
        color_discrete_sequence=[CHART_COLORS[1]],
    )
    fig.update_layout(**GRAPH_LAYOUT, yaxis_title="", xaxis_title="Quantidade")
    return fig


def _chart_timeline(filtered: pd.DataFrame) -> BaseFigure:
    if len(filtered) == 0:
        return _empty_state("Nenhum dado temporal encontrado.")
    hires  = filtered.groupby("HireMonth").size().reset_index(name="Contratações")
    termed = filtered[filtered["Termd"] == 1].copy()

    if len(termed) > 0:
        termed["TermMonth"] = termed["DateofTermination"].dt.to_period("M").astype(str)
        terms = termed.groupby("TermMonth").size().reset_index(name="Desligamentos")
        terms.rename(columns={"TermMonth": "HireMonth"}, inplace=True)
        merged = hires.merge(terms, on="HireMonth", how="outer").fillna(0).sort_values("HireMonth")
    else:
        merged = hires.sort_values("HireMonth")
        merged["Desligamentos"] = 0

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=merged["HireMonth"], y=merged["Contratações"],
        mode="lines+markers", name="Contratações", line=dict(color=CHART_COLORS[0]),
    ))
    fig.add_trace(go.Scatter(
        x=merged["HireMonth"], y=merged["Desligamentos"],
        mode="lines+markers", name="Desligamentos", line=dict(color=CHART_COLORS[1]),
    ))
    fig.update_layout(**GRAPH_LAYOUT, xaxis_title="Período", yaxis_title="Quantidade")
    return fig


def _chart_correlation(filtered: pd.DataFrame) -> BaseFigure:
    if len(filtered) == 0:
        return _empty_state("Nenhum dado encontrado.")
    fig = px.scatter(
        filtered, x="EmpSatisfaction", y="EngagementSurvey",
        color=filtered["Termd"].map({0: "Ativo", 1: "Desligado"}),
        color_discrete_map={"Ativo": CHART_COLORS[0], "Desligado": CHART_COLORS[1]},
        opacity=0.7,
    )
    fig.update_layout(**GRAPH_LAYOUT, xaxis_title="Satisfação", yaxis_title="Engagement Survey")
    return fig


def _chart_manager(filtered: pd.DataFrame) -> BaseFigure:
    manager_stats = (
        filtered.groupby("ManagerName")
        .agg(total=("Termd", "size"), desligados=("Termd", "sum"))
        .reset_index()
    )
    manager_stats["turnover"] = (manager_stats["desligados"] / manager_stats["total"] * 100).round(1)
    manager_stats = manager_stats[manager_stats["total"] >= 3].sort_values("turnover", ascending=True)

    if len(manager_stats) == 0:
        return _empty_state("Dados insuficientes.", "Necessário pelo menos 3 liderados por gestor.")

    fig = px.bar(
        manager_stats, x="turnover", y="ManagerName", orientation="h",
        color_discrete_sequence=[CHART_COLORS[1]], hover_data=["total", "desligados"],
    )
    fig.update_layout(**GRAPH_LAYOUT, yaxis_title="", xaxis_title="Turnover (%)")
    return fig


def _chart_engagement(filtered: pd.DataFrame) -> BaseFigure:
    if len(filtered) == 0:
        return _empty_state("Nenhum dado de engagement encontrado.")
    fig = px.histogram(
        filtered, x="EngagementSurvey", nbins=20,
        color_discrete_sequence=[CHART_COLORS[2]],
    )
    fig.update_layout(**GRAPH_LAYOUT, xaxis_title="Score de Engagement", yaxis_title="Frequência")
    return fig


def _chart_diversity(filtered: pd.DataFrame) -> BaseFigure:
    if len(filtered) == 0:
        return _empty_state("Nenhum dado de diversidade encontrado.")
    diversity = filtered.groupby(["RaceDesc", "Sex"]).size().reset_index(name="count")
    fig = px.bar(
        diversity, x="RaceDesc", y="count", color="Sex", barmode="group",
        color_discrete_sequence=CHART_COLORS[:2],
    )
    fig.update_layout(**GRAPH_LAYOUT, xaxis_title="", yaxis_title="Colaboradores")
    return fig


def _chart_recruitment(filtered: pd.DataFrame) -> BaseFigure:
    if len(filtered) == 0:
        return _empty_state("Nenhum dado de recrutamento encontrado.")
    source_counts = filtered.groupby("RecruitmentSource").size().reset_index(name="count").sort_values("count")
    fig = px.bar(
        source_counts, x="count", y="RecruitmentSource", orientation="h",
        color_discrete_sequence=[CHART_COLORS[2]],
    )
    fig.update_layout(**GRAPH_LAYOUT, yaxis_title="", xaxis_title="Colaboradores")
    return fig


def _chart_state(filtered: pd.DataFrame) -> BaseFigure:
    if len(filtered) == 0:
        return _empty_state("Nenhum dado geográfico encontrado.")
    state_stats = (
        filtered.groupby("State")
        .agg(total=("Termd", "size"), desligados=("Termd", "sum"))
        .reset_index()
    )
    state_stats = state_stats.sort_values("total")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=state_stats["total"], y=state_stats["State"],
        orientation="h", name="Headcount",
        marker_color=CHART_COLORS[0],
    ))
    fig.update_layout(**GRAPH_LAYOUT, yaxis_title="", xaxis_title="Colaboradores")
    return fig


def _chart_position_salary(filtered: pd.DataFrame) -> BaseFigure:
    position_counts = filtered.groupby("Position").size().reset_index(name="count")
    top_positions   = position_counts[position_counts["count"] >= 3]["Position"].tolist()

    if not top_positions:
        return _empty_state("Dados insuficientes.", "Necessário pelo menos 3 colaboradores por cargo.")

    subset = filtered[filtered["Position"].isin(top_positions)]
    fig = px.box(
        subset, x="Position", y="Salary",
        color_discrete_sequence=[CHART_COLORS[2]],
    )
    fig.update_layout(**GRAPH_LAYOUT, xaxis_title="", yaxis_title="Salário (USD)")
    return fig


def _chart_lateness(filtered: pd.DataFrame) -> BaseFigure:
    if len(filtered) == 0:
        return _empty_state("Nenhum dado de atrasos encontrado.")
    fig = px.scatter(
        filtered, x="DaysLateLast30", y="PerformanceScore",
        color="Department", opacity=0.7,
        color_discrete_sequence=CHART_COLORS,
        hover_data=["Employee_Name", "Salary"],
    )
    fig.update_layout(**GRAPH_LAYOUT, xaxis_title="Dias Atrasado (últimos 30d)", yaxis_title="Score de Performance")
    return fig


def _chart_projects(filtered: pd.DataFrame) -> BaseFigure:
    if len(filtered) == 0:
        return _empty_state("Nenhum dado de projetos encontrado.")
    fig = px.scatter(
        filtered, x="SpecialProjectsCount", y="EngagementSurvey",
        color=filtered["Termd"].map({0: "Ativo", 1: "Desligado"}),
        color_discrete_map={"Ativo": CHART_COLORS[0], "Desligado": CHART_COLORS[1]},
        opacity=0.7,
        hover_data=["Employee_Name", "Department"],
    )
    fig.update_layout(**GRAPH_LAYOUT, xaxis_title="Qtd. Projetos Especiais", yaxis_title="Engagement Survey")
    return fig


def _chart_heatmap(filtered: pd.DataFrame) -> BaseFigure:
    numeric_cols = ["Salary", "EmpSatisfaction", "EngagementSurvey", "Absences", "DaysLateLast30", "SpecialProjectsCount"]
    available = [c for c in numeric_cols if c in filtered.columns]

    if len(available) < 2 or len(filtered) < 2:
        return _empty_state("Dados insuficientes para calcular correlações.")

    corr = filtered[available].corr()
    labels = {
        "Salary": "Salário", "EmpSatisfaction": "Satisfação",
        "EngagementSurvey": "Engagement", "Absences": "Absências",
        "DaysLateLast30": "Atrasos 30d", "SpecialProjectsCount": "Proj. Especiais",
    }
    renamed = [labels.get(c, c) for c in corr.columns]
    fig = px.imshow(
        corr.values, x=renamed, y=renamed, text_auto=".2f",
        color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
    )
    fig.update_layout(**GRAPH_LAYOUT)
    return fig


def _chart_tenure(filtered: pd.DataFrame) -> BaseFigure:
    termed = filtered[filtered["Termd"] == 1]
    if len(termed) == 0:
        return _empty_state("Sem desligamentos no recorte atual.", "Selecione colaboradores com status desligado.")
    fig = px.histogram(
        termed, x="TenureMonths", nbins=20,
        color_discrete_sequence=[CHART_COLORS[0]],
        labels={"TenureMonths": "Meses de Permanência"},
    )
    fig.update_layout(**GRAPH_LAYOUT, xaxis_title="Meses", yaxis_title="Frequência")
    return fig


# =========================================================================
# Tabela de dados — F4.2 (seletor de colunas) + F4.3 (coluna Nome fixa)
# =========================================================================

ALL_COLUMNS = [
    "Employee_Name", "Department", "Position", "Salary",
    "PerformanceScore", "EmploymentStatus", "TenureMonths",
    "State", "ManagerName", "EmpSatisfaction", "EngagementSurvey",
    "DaysLateLast30", "SpecialProjectsCount",
]

COL_LABELS = {
    "Employee_Name":      "Nome",
    "Department":         "Departamento",
    "Position":           "Cargo",
    "Salary":             "Salário",
    "PerformanceScore":   "Performance",
    "EmploymentStatus":   "Status",
    "TenureMonths":       "Tenure (m)",
    "State":              "Estado",
    "ManagerName":        "Gestor",
    "EmpSatisfaction":    "Satisfação",
    "EngagementSurvey":   "Engagement",
    "DaysLateLast30":     "Atrasos 30d",
    "SpecialProjectsCount": "Proj. Especiais",
}


def _build_data_table(filtered: pd.DataFrame) -> html.Div:
    """Tabela com seletor de colunas e coluna Nome fixa (F4.2 + F4.3)."""
    available = [c for c in ALL_COLUMNS if c in filtered.columns]
    table_df  = filtered[available].copy()
    columns   = [{"name": COL_LABELS.get(c, c), "id": c} for c in available]

    return dash_table.DataTable(
        data=table_df.to_dict("records"),
        columns=columns,
        page_size=15,
        sort_action="native",
        filter_action="native",
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": COLORS["card"],
            "color": COLORS["text"],
            "fontWeight": "700",
            "border": f"1px solid {COLORS['border']}",
            "fontSize": TYPE_SCALE["xs"],
            "textTransform": "uppercase",
            "letterSpacing": "0.3px",
        },
        style_cell={
            "backgroundColor": COLORS["bg"],
            "color": COLORS["text"],
            "border": f"1px solid {COLORS['border']}",
            "fontSize": TYPE_SCALE["sm"],
            "padding": f"{SPACING['sm']} {SPACING['md']}",
            "textAlign": "left",
            "whiteSpace": "nowrap",
        },
        style_filter={
            "backgroundColor": COLORS["card"],
            "color": COLORS["text"],
        },
        # F4.3 — Coluna Nome fixa à esquerda
        style_cell_conditional=[
            {
                "if": {"column_id": "Employee_Name"},
                "position": "sticky",
                "left": 0,
                "backgroundColor": COLORS["card"],
                "zIndex": 1,
                "fontWeight": "600",
            }
        ],
    )
