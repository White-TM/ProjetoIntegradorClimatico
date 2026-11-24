import json
from pathlib import Path
import duckdb
import pandas as pd

ARQUIVO_JSON = Path("dados/raw_open_meteo.json")
ARQUIVO_DB = Path("dados/clima_local.duckdb")


def tratar_e_carregar():
    if not ARQUIVO_JSON.exists():
        raise FileNotFoundError(f"Arquivo {ARQUIVO_JSON} não encontrado. Execute coleta.py primeiro.")

    with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
        conteudo = json.load(f)

    meta = conteudo["metadados_coleta"]
    api_data = conteudo["resposta_api"]
    diario = api_data["daily"]

    # 1. Criação do DataFrame e padronização dos nomes das colunas
    df = pd.DataFrame({
        "data": diario["time"],
        "temp_min_c": diario["temperature_2m_min"],
        "temp_max_c": diario["temperature_2m_max"],
        "precipitacao_mm": diario["precipitation_sum"],
    })

    df["localidade"] = meta["localidade"]
    df["latitude"] = float(api_data["latitude"])
    df["longitude"] = float(api_data["longitude"])

    # 2. Conversão e validação de datas e tipos numéricos
    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="raise").dt.date
    for col in ["temp_min_c", "temp_max_c", "precipitacao_mm"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 3. Verificação de qualidade: duplicidades, ausentes, cobertura e inconsistências
    duplicados = df.duplicated(subset=["data"]).sum()
    if duplicados > 0:
        print(f"Aviso: {duplicados} registros duplicados removidos.")
        df = df.drop_duplicates(subset=["data"], keep="last")

    # Ordenação cronológica e conferência de cobertura (30 dias)
    df = df.sort_values("data").reset_index(drop=True)
    qtd_registros = len(df)
    dias_esperados = (df["data"].max() - df["data"].min()).days + 1

    # Validação de consistência física (temp_min não pode ser maior que temp_max)
    inconsistencias_temp = df[df["temp_min_c"] > df["temp_max_c"]]
    if not inconsistencias_temp.empty:
        raise ValueError(f"Inconsistência encontrada: temp_min > temp_max em {len(inconsistencias_temp)} dias.")

    # Relatório de valores ausentes (NÃO substitui por zero sem justificativa)
    ausentes = df[["temp_min_c", "temp_max_c", "precipitacao_mm"]].isna().sum().to_dict()

    print("=== RELATÓRIO DE QUALIDADE DOS DADOS ===")
    print(f"Registros carregados: {qtd_registros} (Cobertura do intervalo: {dias_esperados} dias)")
    print(f"Período: {df['data'].min()} até {df['data'].max()}")
    print(f"Valores ausentes por variável: {ausentes}")
    print(f"Duplicidades encontradas: {duplicados}")

    # 4. Carga no DuckDB (Idempotente: recria/substitui sem duplicar registros)
    con = duckdb.connect(str(ARQUIVO_DB))
    con.execute("""
        CREATE OR REPLACE TABLE clima_diario (
            data DATE PRIMARY KEY,
            localidade VARCHAR,
            latitude DOUBLE,
            longitude DOUBLE,
            temp_min_c DOUBLE,
            temp_max_c DOUBLE,
            precipitacao_mm DOUBLE
        );
    """)

    con.execute("INSERT INTO clima_diario SELECT data, localidade, latitude, longitude, temp_min_c, temp_max_c, precipitacao_mm FROM df;")

    total_banco = con.execute("SELECT COUNT(*) FROM clima_diario;").fetchone()[0]
    print(f"Carga no DuckDB concluída com sucesso! Total de registros na tabela 'clima_diario': {total_banco}")
    con.close()


if __name__ == "__main__":
    tratar_e_carregar()
