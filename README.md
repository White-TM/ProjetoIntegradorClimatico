# Observatório Climático Local — Cândido Mota/SP

Projeto extensionista focado na coleta, tratamento, armazenamento e análise inicial de dados meteorológicos históricos para apoio à tomada de decisão na agricultura familiar e horticultura de Cândido Mota/SP.

## Objetivo e Público-Alvo
- **Objetivo:** Consolidar uma base histórica confiável de 30 dias para identificar padrões de estresse térmico, regime de chuvas e janelas críticas de calor seco, oferecendo subsídios técnicos para o manejo preventivo de lavouras e planejamento de irrigação.
- **Público-alvo:** Pequenos produtores rurais, agricultores familiares e horticultores do município de Cândido Mota/SP.

## Fonte, Localidade, Período e Variáveis
- **Fonte dos dados:** API Histórica Open-Meteo (`https://archive-api.open-meteo.com/v1/archive`), baseada em modelos de reanálise meteorológica.
- **Localidade:** Cândido Mota, SP (Latitude: `-22.7464`, Longitude: `-50.3869`, Fuso horário: `America/Sao_Paulo`).
- **Período analisado:** `2026-10-01` a `2026-10-30` (30 dias consecutivos).
- **Variáveis coletadas:**
  - `temperature_2m_min`: Temperatura mínima diária a 2 metros (°C).
  - `temperature_2m_max`: Temperatura máxima diária a 2 metros (°C).
  - `precipitation_sum`: Precipitação diária acumulada (mm).

## Estrutura dos Arquivos
```text
├── dados/
│   ├── raw_open_meteo.json       # Resposta original da API preservada
│   └── clima_local.duckdb        # Banco de dados analítico DuckDB
├── docs/
│   └── escopo-1/
│       └── AE2/
│           └── relatorio_ae2.pdf # Relatório técnico e analítico (AE2)
├── .gitignore                    # Arquivos e pastas ignorados no versionamento
├── README.md                     # Documentação do projeto
├── requirements.txt              # Dependências Python
├── coleta.py                     # Script de extração via API e salvamento do JSON
├── banco.py                      # Script de tratamento (pandas) e carga no DuckDB
└── consultas.sql                 # Consultas SQL dos indicadores/KPIs
