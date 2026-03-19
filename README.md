# B.I. de RH — Dashboard de People Analytics

Dashboard interativo para analise de dados de Recursos Humanos, construido com Python, Dash e Plotly.

## Funcionalidades

- **6 KPIs** com variacao comparativa (setas delta vs media geral quando filtros estao ativos)
- **18 graficos** interativos com loading states
- **Tabela interativa** com 13 colunas, ordenavel, pesquisavel e paginada (15 por pagina)
- **5 filtros** na sidebar: Departamento, Genero, Status, Gestor, Periodo de Contratacao
- **Exportacao CSV** dos dados filtrados
- **Tema escuro** consistente em todos os componentes
- **Responsividade** com meta tags de viewport

## Requisitos

- Python 3.10+
- Dependencias listadas em `requirements.txt`

## Instalacao

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python app.py
```

Acesse [http://127.0.0.1:8050](http://127.0.0.1:8050) no navegador.

## Dataset

Utiliza o `HRDataset_v14.csv` (311 registros, 36 colunas) com dados ficticios de colaboradores incluindo informacoes demograficas, salariais, de performance e engajamento. O arquivo deve estar na raiz do projeto.

## Estrutura do Projeto

```
app.py                  # Ponto de entrada
config.py               # Cores, estilos, constantes
requirements.txt        # Dependencias com versoes fixas
HRDataset_v14.csv       # Dataset de RH
data/
  loader.py             # Carregamento, pre-processamento e filtragem
layouts/
  sidebar.py            # Sidebar com filtros e botao de exportacao
  main_content.py       # Layout principal com graficos e tabela
callbacks/
  dashboard.py          # Callbacks, builders de graficos e tabela
docs/
  analise-projeto-rh.md     # Relatorio de analise v1
  analise-projeto-rh-v2.md  # Relatorio de analise v2
  analise-projeto-rh-v3.md  # Auditoria de cobertura analitica
```

## Graficos Disponiveis

| # | Grafico | Tipo | Dados |
|---|---------|------|-------|
| 1 | Headcount por Departamento | Bar horizontal | Department |
| 2 | Distribuicao Salarial por Departamento | Box plot | Salary, Department |
| 3 | Distribuicao de Performance | Pie chart | PerformanceScore |
| 4 | Motivos de Desligamento | Bar horizontal | TermReason |
| 5 | Tendencia: Contratacoes vs Desligamentos | Linhas temporais | DateofHire, DateofTermination |
| 6 | Satisfacao vs Engagement | Scatter | EmpSatisfaction, EngagementSurvey, Termd |
| 7 | Turnover por Gestor | Bar horizontal | ManagerName, Termd |
| 8 | Distribuicao de Engagement | Histograma | EngagementSurvey |
| 9 | Diversidade — Raca e Genero | Bar agrupado | RaceDesc, Sex |
| 10 | Canais de Recrutamento | Bar horizontal | RecruitmentSource |
| 11 | Distribuicao Geografica por Estado | Bar horizontal | State |
| 12 | Benchmarking Salarial por Cargo | Box plot | Position, Salary |
| 13 | Atrasos vs Performance | Scatter | DaysLateLast30, PerformanceScore |
| 14 | Projetos Especiais vs Engagement | Scatter | SpecialProjectsCount, EngagementSurvey |
| 15 | Heatmap de Correlacoes | Matriz 6x6 | 6 variaveis numericas |
| 16 | Tempo de Permanencia (Desligados) | Histograma | TenureMonths |

## KPIs

| KPI | Descricao | Tooltip |
|-----|-----------|---------|
| Colaboradores | Total no filtro atual | Total de colaboradores no filtro atual |
| Turnover | % de desligamentos | Percentual de desligamentos sobre o total |
| Salario Medio | Media salarial | Media salarial dos colaboradores filtrados |
| Satisfacao | Media 1-5 | Media da pesquisa de satisfacao (1-5) |
| Engagement | Media da pesquisa | Media da pesquisa de engajamento |
| Absencias | Media de dias | Media de dias de ausencia por colaborador |

Quando filtros estao ativos, cada KPI exibe uma seta (verde/vermelha) indicando a variacao em relacao a media geral da empresa.

## Tecnologias

| Tecnologia | Versao | Uso |
|-----------|--------|-----|
| Dash | 4.0.0 | Framework web para dashboards |
| Plotly | 6.6.0 | Graficos interativos |
| Pandas | 3.0.1 | Manipulacao de dados |
| NumPy | 2.4.3 | Operacoes numericas |

## Solucao de Problemas

### Porta 8050 em uso

Encerrar o processo que usa a porta ou alterar no `app.py`:

```python
app.run(debug=True, port=8051)
```

### Arquivo de dados nao encontrado

O sistema espera `HRDataset_v14.csv` na raiz do projeto. Uma mensagem de erro sera exibida caso o arquivo nao exista.

## Cobertura do Dataset

O dashboard utiliza 22 das 36 colunas disponiveis (61%). As colunas restantes sao majoritariamente IDs redundantes (DeptID, GenderID, etc.) ou dados de baixo potencial analitico no contexto atual.

## Melhorias Futuras

- Configuracao de porta e dataset via variaveis de ambiente
- Testes automatizados para funcoes de carga e filtro
- Pipeline de lint/typecheck/test em CI
- Containerizacao com Docker
- Aba de detalhamento (drill-down) por departamento/gestor
