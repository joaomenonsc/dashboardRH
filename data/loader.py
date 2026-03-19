"""Carregamento e pré-processamento dos dados de RH."""

import sys
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "HRDataset_v14.csv"


def load_data() -> pd.DataFrame:
    """Carrega e pré-processa o dataset de RH."""
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

    return df


def filter_data(
    df: pd.DataFrame,
    dept: list | None,
    gender: str | None,
    status: str | None,
    date_range: list | None,
    manager: str | None = None,
) -> pd.DataFrame:
    """Filtra o dataframe com base nos filtros selecionados."""
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
