"""Callbacks do dashboard de RH."""

import dash
from dash import Input, Output, State, html, dash_table
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from config import COLORS, GRAPH_LAYOUT, KPI_STYLE
from data.loader import filter_data

FILTER_INPUTS = [
    Input("filter-dept", "value"),
    Input("filter-gender", "value"),
    Input("filter-status", "value"),
    Input("filter-manager", "value"),
    Input("filter-date-range", "start_date"),
    Input("filter-date-range", "end_date"),
]


def _get_filter_args(dept, gender, status, manager, start_date, end_date):
    date_range = [start_date, end_date] if start_date and end_date else None
    return dept, gender, status, date_range, manager


def register_callbacks(app, df):
    """Registra todos os callbacks do dashboard."""

    @app.callback(
        Output("kpi-cards", "children"),
        Output("chart-headcount", "figure"),
        Output("chart-salary", "figure"),
        Output("chart-performance", "figure"),
        Output("chart-turnover", "figure"),
        Output("chart-timeline", "figure"),
        Output("chart-correlation", "figure"),
        Output("chart-manager", "figure"),
        Output("chart-engagement", "figure"),
        Output("chart-diversity", "figure"),
        Output("chart-recruitment", "figure"),
        Output("chart-state", "figure"),
        Output("chart-position-salary", "figure"),
        Output("chart-lateness", "figure"),
        Output("chart-projects", "figure"),
        Output("chart-heatmap", "figure"),
        Output("chart-tenure", "figure"),
        Output("data-table-container", "children"),
        *FILTER_INPUTS,
    )
    def update_dashboard(dept, gender, status, manager, start_date, end_date):
        dept, gender, status, date_range, manager = _get_filter_args(
            dept, gender, status, manager, start_date, end_date
        )
        filtered = filter_data(df, dept, gender, status, date_range, manager)

        has_filters = any([dept, gender, status, manager, date_range])
        kpis = _build_kpis(filtered, df if has_filters else None)

        return (
            kpis,
            _chart_headcount(filtered),
            _chart_salary(filtered),
            _chart_performance(filtered),
            _chart_turnover(filtered),
            _chart_timeline(filtered),
            _chart_correlation(filtered),
            _chart_manager(filtered),
            _chart_engagement(filtered),
            _chart_diversity(filtered),
            _chart_recruitment(filtered),
            _chart_state(filtered),
            _chart_position_salary(filtered),
            _chart_lateness(filtered),
            _chart_projects(filtered),
            _chart_heatmap(filtered),
            _chart_tenure(filtered),
            _build_data_table(filtered),
        )

    @app.callback(
        Output("download-csv", "data"),
        Input("btn-export", "n_clicks"),
        State("filter-dept", "value"),
        State("filter-gender", "value"),
        State("filter-status", "value"),
        State("filter-manager", "value"),
        State("filter-date-range", "start_date"),
        State("filter-date-range", "end_date"),
        prevent_initial_call=True,
    )
    def export_csv(n_clicks, dept, gender, status, manager, start_date, end_date):
        if not n_clicks or dash.ctx.triggered_id != "btn-export":
            return dash.no_update
        dept, gender, status, date_range, manager = _get_filter_args(
            dept, gender, status, manager, start_date, end_date
        )
        filtered = filter_data(df, dept, gender, status, date_range, manager)
        return dict(content=filtered.to_csv(index=False), filename="dados_rh_filtrados.csv")


# --- KPIs ---

def _kpi_card(title, value, tooltip=None, delta=None):
    children = [
        html.P(
            title,
            style={
                "color": COLORS["muted"],
                "fontSize": "12px",
                "margin": "0 0 8px 0",
                "textTransform": "uppercase",
                "letterSpacing": "0.5px",
            },
            title=tooltip,
        ),
        html.H3(
            value,
            style={"margin": "0", "fontSize": "24px", "color": COLORS["accent"]},
        ),
    ]
    if delta is not None:
        is_positive = delta > 0
        arrow = "▲" if is_positive else "▼" if delta < 0 else "–"
        color = COLORS["accent2"] if is_positive else COLORS["accent3"] if delta < 0 else COLORS["muted"]
        children.append(
            html.P(
                f"{arrow} {abs(delta):.1f} vs geral",
                style={"color": color, "fontSize": "11px", "margin": "6px 0 0 0"},
            )
        )
    return html.Div(style=KPI_STYLE, children=children)


def _build_kpis(filtered, full_df=None):
    total = len(filtered)
    terminated = filtered["Termd"].sum()
    turnover = (terminated / total * 100) if total > 0 else 0
    avg_salary = filtered["Salary"].mean() if total > 0 else 0
    avg_satisfaction = filtered["EmpSatisfaction"].mean() if total > 0 else 0
    avg_engagement = filtered["EngagementSurvey"].mean() if total > 0 else 0
    avg_absences = filtered["Absences"].mean() if total > 0 else 0

    # Deltas comparativos com a base completa
    if full_df is not None and len(full_df) > 0:
        g_total = len(full_df)
        g_turnover = (full_df["Termd"].sum() / g_total * 100)
        g_salary = full_df["Salary"].mean()
        g_satisfaction = full_df["EmpSatisfaction"].mean()
        g_engagement = full_df["EngagementSurvey"].mean()
        g_absences = full_df["Absences"].mean()

        d_turnover = turnover - g_turnover
        d_salary = avg_salary - g_salary
        d_satisfaction = avg_satisfaction - g_satisfaction
        d_engagement = avg_engagement - g_engagement
        d_absences = avg_absences - g_absences
    else:
        d_turnover = d_salary = d_satisfaction = d_engagement = d_absences = None

    return [
        _kpi_card("Colaboradores", f"{total}", "Total de colaboradores no filtro atual"),
        _kpi_card("Turnover", f"{turnover:.1f}%", "Percentual de desligamentos sobre o total", d_turnover),
        _kpi_card("Salário Médio", f"${avg_salary:,.0f}", "Média salarial dos colaboradores filtrados", d_salary),
        _kpi_card("Satisfação", f"{avg_satisfaction:.1f}/5", "Média da pesquisa de satisfação (1-5)", d_satisfaction),
        _kpi_card("Engagement", f"{avg_engagement:.2f}", "Média da pesquisa de engajamento", d_engagement),
        _kpi_card("Absências", f"{avg_absences:.1f}", "Média de dias de ausência por colaborador", d_absences),
    ]


# --- Charts ---

def _chart_headcount(filtered):
    dept_counts = (
        filtered.groupby("Department").size().reset_index(name="count").sort_values("count")
    )
    fig = px.bar(
        dept_counts, x="count", y="Department", orientation="h",
        color_discrete_sequence=[COLORS["accent"]],
    )
    fig.update_layout(**GRAPH_LAYOUT, title="Headcount por Departamento", yaxis_title="", xaxis_title="Colaboradores")
    return fig


def _chart_salary(filtered):
    fig = px.box(
        filtered, x="Department", y="Salary",
        color_discrete_sequence=[COLORS["accent"]],
    )
    fig.update_layout(**GRAPH_LAYOUT, title="Distribuição Salarial por Departamento", xaxis_title="", yaxis_title="Salário (USD)")
    return fig


def _chart_performance(filtered):
    perf_counts = filtered.groupby("PerformanceScore").size().reset_index(name="count")
    fig = px.pie(
        perf_counts, values="count", names="PerformanceScore",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(**GRAPH_LAYOUT, title="Distribuição de Performance")
    return fig


def _chart_turnover(filtered):
    termed = filtered[filtered["Termd"] == 1]
    if len(termed) > 0:
        reasons = termed.groupby("TermReason").size().reset_index(name="count").sort_values("count")
        fig = px.bar(
            reasons, x="count", y="TermReason", orientation="h",
            color_discrete_sequence=[COLORS["accent2"]],
        )
    else:
        fig = go.Figure()
        fig.add_annotation(text="Sem dados de desligamento", showarrow=False, font=dict(size=16, color=COLORS["muted"]))
    fig.update_layout(**GRAPH_LAYOUT, title="Motivos de Desligamento", yaxis_title="", xaxis_title="Quantidade")
    return fig


def _chart_timeline(filtered):
    hires = filtered.groupby("HireMonth").size().reset_index(name="Contratações")
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
        mode="lines+markers", name="Contratações", line=dict(color=COLORS["accent"]),
    ))
    fig.add_trace(go.Scatter(
        x=merged["HireMonth"], y=merged["Desligamentos"],
        mode="lines+markers", name="Desligamentos", line=dict(color=COLORS["accent2"]),
    ))
    fig.update_layout(**GRAPH_LAYOUT, title="Tendência: Contratações vs Desligamentos", xaxis_title="Período", yaxis_title="Quantidade")
    return fig


def _chart_correlation(filtered):
    fig = px.scatter(
        filtered, x="EmpSatisfaction", y="EngagementSurvey",
        color=filtered["Termd"].map({0: "Ativo", 1: "Desligado"}),
        color_discrete_map={"Ativo": COLORS["accent"], "Desligado": COLORS["accent2"]},
        opacity=0.7,
    )
    fig.update_layout(**GRAPH_LAYOUT, title="Satisfação vs Engagement (por Status)", xaxis_title="Satisfação", yaxis_title="Engagement Survey")
    return fig


def _chart_manager(filtered):
    manager_stats = (
        filtered.groupby("ManagerName")
        .agg(total=("Termd", "size"), desligados=("Termd", "sum"))
        .reset_index()
    )
    manager_stats["turnover"] = (manager_stats["desligados"] / manager_stats["total"] * 100).round(1)
    manager_stats = manager_stats[manager_stats["total"] >= 3].sort_values("turnover", ascending=True)

    fig = px.bar(
        manager_stats, x="turnover", y="ManagerName", orientation="h",
        color_discrete_sequence=[COLORS["accent2"]], hover_data=["total", "desligados"],
    )
    fig.update_layout(**GRAPH_LAYOUT, title="Taxa de Turnover por Gestor (min. 3 liderados)", yaxis_title="", xaxis_title="Turnover (%)")
    return fig


def _chart_engagement(filtered):
    fig = px.histogram(
        filtered, x="EngagementSurvey", nbins=20,
        color_discrete_sequence=[COLORS["accent3"]],
    )
    fig.update_layout(**GRAPH_LAYOUT, title="Distribuição de Engagement Survey", xaxis_title="Score de Engagement", yaxis_title="Frequência")
    return fig


def _chart_diversity(filtered):
    diversity = filtered.groupby(["RaceDesc", "Sex"]).size().reset_index(name="count")
    fig = px.bar(
        diversity, x="RaceDesc", y="count", color="Sex", barmode="group",
        color_discrete_sequence=[COLORS["accent"], COLORS["accent2"]],
    )
    fig.update_layout(**GRAPH_LAYOUT, title="Diversidade — Raça e Gênero", xaxis_title="", yaxis_title="Colaboradores")
    return fig


def _chart_recruitment(filtered):
    source_counts = filtered.groupby("RecruitmentSource").size().reset_index(name="count").sort_values("count")
    fig = px.bar(
        source_counts, x="count", y="RecruitmentSource", orientation="h",
        color_discrete_sequence=[COLORS["accent3"]],
    )
    fig.update_layout(**GRAPH_LAYOUT, title="Canais de Recrutamento", yaxis_title="", xaxis_title="Colaboradores")
    return fig


def _chart_state(filtered):
    state_stats = (
        filtered.groupby("State")
        .agg(total=("Termd", "size"), desligados=("Termd", "sum"))
        .reset_index()
    )
    state_stats["turnover"] = (state_stats["desligados"] / state_stats["total"] * 100).round(1)
    state_stats = state_stats.sort_values("total")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=state_stats["total"], y=state_stats["State"],
        orientation="h", name="Headcount",
        marker_color=COLORS["accent"],
    ))
    fig.update_layout(
        **GRAPH_LAYOUT,
        title="Distribuição Geográfica por Estado",
        yaxis_title="", xaxis_title="Colaboradores",
    )
    return fig


def _chart_position_salary(filtered):
    position_counts = filtered.groupby("Position").size().reset_index(name="count")
    top_positions = position_counts[position_counts["count"] >= 3]["Position"].tolist()

    if top_positions:
        subset = filtered[filtered["Position"].isin(top_positions)]
        fig = px.box(
            subset, x="Position", y="Salary",
            color_discrete_sequence=[COLORS["accent3"]],
        )
        fig.update_layout(**GRAPH_LAYOUT, title="Benchmarking Salarial por Cargo (min. 3)", xaxis_title="", yaxis_title="Salário (USD)")
    else:
        fig = go.Figure()
        fig.add_annotation(text="Dados insuficientes", showarrow=False, font=dict(size=16, color=COLORS["muted"]))
        fig.update_layout(**GRAPH_LAYOUT, title="Benchmarking Salarial por Cargo")
    return fig


def _chart_lateness(filtered):
    fig = px.scatter(
        filtered, x="DaysLateLast30", y="PerformanceScore",
        color="Department", opacity=0.7,
        hover_data=["Employee_Name", "Salary"],
    )
    fig.update_layout(**GRAPH_LAYOUT, title="Atrasos vs Performance (por Departamento)", xaxis_title="Dias Atrasado (últimos 30d)", yaxis_title="Score de Performance")
    return fig


def _chart_projects(filtered):
    fig = px.scatter(
        filtered, x="SpecialProjectsCount", y="EngagementSurvey",
        color=filtered["Termd"].map({0: "Ativo", 1: "Desligado"}),
        color_discrete_map={"Ativo": COLORS["accent"], "Desligado": COLORS["accent2"]},
        opacity=0.7,
        hover_data=["Employee_Name", "Department"],
    )
    fig.update_layout(**GRAPH_LAYOUT, title="Projetos Especiais vs Engagement", xaxis_title="Qtd. Projetos Especiais", yaxis_title="Engagement Survey")
    return fig


def _chart_heatmap(filtered):
    numeric_cols = ["Salary", "EmpSatisfaction", "EngagementSurvey", "Absences", "DaysLateLast30", "SpecialProjectsCount"]
    available = [c for c in numeric_cols if c in filtered.columns]
    if len(available) < 2 or len(filtered) < 2:
        fig = go.Figure()
        fig.add_annotation(text="Dados insuficientes", showarrow=False, font=dict(size=16, color=COLORS["muted"]))
    else:
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
    fig.update_layout(**GRAPH_LAYOUT, title="Correlações entre Variáveis")
    return fig


def _chart_tenure(filtered):
    termed = filtered[filtered["Termd"] == 1]
    if len(termed) > 0:
        fig = px.histogram(
            termed, x="TenureMonths", nbins=20,
            color_discrete_sequence=[COLORS["accent"]],
            labels={"TenureMonths": "Meses de Permanência"},
        )
        fig.update_layout(**GRAPH_LAYOUT, title="Tempo de Permanência (Desligados)", xaxis_title="Meses", yaxis_title="Frequência")
    else:
        fig = go.Figure()
        fig.add_annotation(text="Sem dados de desligamento", showarrow=False, font=dict(size=16, color=COLORS["muted"]))
        fig.update_layout(**GRAPH_LAYOUT, title="Tempo de Permanência (Desligados)")
    return fig


def _build_data_table(filtered):
    display_cols = [
        "Employee_Name", "Department", "Position", "State", "ManagerName",
        "Salary", "EmpSatisfaction", "EngagementSurvey",
        "PerformanceScore", "EmploymentStatus", "DaysLateLast30",
        "SpecialProjectsCount", "TenureMonths",
    ]
    available = [c for c in display_cols if c in filtered.columns]
    table_df = filtered[available].copy()

    col_labels = {
        "Employee_Name": "Nome", "Department": "Departamento",
        "Position": "Cargo", "State": "Estado", "ManagerName": "Gestor",
        "Salary": "Salário", "EmpSatisfaction": "Satisfação",
        "EngagementSurvey": "Engagement", "PerformanceScore": "Performance",
        "EmploymentStatus": "Status", "DaysLateLast30": "Atrasos 30d",
        "SpecialProjectsCount": "Proj. Especiais", "TenureMonths": "Tenure (meses)",
    }

    columns = [{"name": col_labels.get(c, c), "id": c} for c in available]

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
            "fontWeight": "600",
            "border": f"1px solid {COLORS['border']}",
        },
        style_cell={
            "backgroundColor": COLORS["bg"],
            "color": COLORS["text"],
            "border": f"1px solid {COLORS['border']}",
            "fontSize": "13px",
            "padding": "8px 12px",
            "textAlign": "left",
        },
        style_filter={
            "backgroundColor": COLORS["card"],
            "color": COLORS["text"],
        },
    )
