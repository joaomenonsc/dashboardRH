"""Carregamento e pré-processamento dos dados de RH."""

import sys
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "HRDataset_v14.csv"


def load_data() -> pd.DataFrame:
    """Carrega e pré-processa o dataset de RH.

    Returns:
        DataFrame pronto para consumo do dashboard.
    """
    if not DATA_PATH.exists():
        print(f"Erro: Arquivo de dados não encontrado em {DATA_PATH}")
        print("Certifique-se de que 'HRDataset_v14.csv' está na raiz do projeto.")
        sys.exit(1)

    try:
        df = pd.read_csv(DATA_PATH)
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        sys.exit(1)

    df["Department"] = df["Department"].str.strip()
    df["Sex"] = df["Sex"].str.strip()
    df["DateofHire"] = pd.to_datetime(df["DateofHire"], format="mixed")
    df["DateofTermination"] = pd.to_datetime(
        df["DateofTermination"], format="mixed", errors="coerce"
    )
    df["HireYear"] = df["DateofHire"].dt.year
    df["HireMonth"] = df["DateofHire"].dt.to_period("M").astype(str)

    # Tenure em meses
    end_date = df["DateofTermination"].fillna(pd.Timestamp.now())
    df["TenureMonths"] = ((end_date - df["DateofHire"]).dt.days / 30.44).round(1)

    # Tradução dos valores categóricos para Português
    df["Department"] = df["Department"].replace({
        "Production": "Produção",
        "IT/IS": "TI/SI",
        "Software Engineering": "Engenharia de Software",
        "Admin Offices": "Administração",
        "Executive Office": "Diretoria",
        "Sales": "Vendas"
    })
    
    df["Sex"] = df["Sex"].replace({
        "M": "Masculino",
        "F": "Feminino"
    })
    
    df["EmploymentStatus"] = df["EmploymentStatus"].replace({
        "Active": "Ativo",
        "Voluntarily Terminated": "Desligamento Voluntário",
        "Terminated for Cause": "Desligamento por Justa Causa",
        "Leave of Absence": "Licença",
        "Future Start": "Início Futuro"
    })
    
    df["TermReason"] = df["TermReason"].replace({
        "N/A-StillEmployed": "N/A - Ainda Empreg.",
        "career change": "Mudança de Carreira",
        "Another position": "Outra Posição",
        "unhappy": "Insatisfação",
        "hours": "Horário",
        "return to school": "Retorno Aos Estudos",
        "attendance": "Faltas",
        "performance": "Performance",
        "more money": "Salário Maior",
        "relocation out of area": "Mudança de Local",
        "maternity leave": "Licença Maternidade",
        "no-call, no-show": "Abandono de Emprego",
        "military": "Serviço Militar",
        "retiring": "Aposentadoria",
        "medical issues": "Problemas de Saúde",
        "gross misconduct": "Má Conduta Grave"
    })
    
    df["PerformanceScore"] = df["PerformanceScore"].replace({
        "Exceeds": "Excede Expectativas",
        "Fully Meets": "Atende Totalmente",
        "Needs Improvement": "Precisa Melhorar",
        "PIP": "Plano de Melhoria"
    })

    df["RecruitmentSource"] = df["RecruitmentSource"].replace({
        "Employee Referral": "Indicação",
        "Diversity Job Fair": "Feira de Diversidade",
        "On-line Web application": "Candidatura Online",
        "Google Search": "Google",
        "Website": "Site da Empresa"
        # Others like LinkedIn, Indeed, CareerBuilder keep their names
    })

    return df


def filter_data(
    df: pd.DataFrame,
    dept: list | None,
    gender: str | None,
    status: str | None,
    date_range: list | None,
    manager: str | None = None,
) -> pd.DataFrame:
    """Filtra o dataframe conforme os critérios selecionados na UI.

    Args:
        df: DataFrame completo de RH.
        dept: Lista de departamentos selecionados.
        gender: Gênero selecionado.
        status: Status de emprego selecionado.
        date_range: Intervalo de datas de contratação.
        manager: Nome do gestor selecionado.

    Returns:
        DataFrame filtrado.
    """
    filtered = df.copy()
    if dept:
        filtered = filtered[filtered["Department"].isin(dept)]
    if gender:
        filtered = filtered[filtered["Sex"] == gender]
    if status:
        filtered = filtered[filtered["EmploymentStatus"] == status]
    if manager:
        filtered = filtered[filtered["ManagerName"] == manager]
    if date_range and len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        filtered = filtered[
            (filtered["DateofHire"] >= start) & (filtered["DateofHire"] <= end)
        ]
    return filtered
