import json
from datetime import datetime, timezone
from pathlib import Path
import requests

# --- PARÂMETROS DO RECORTE ---
LOCALIDADE = "Cândido Mota, SP"
LATITUDE = -22.7464
LONGITUDE = -50.3869
DATA_INICIO = "2026-10-01"
DATA_FIM = "2026-10-30"  # 30 dias consecutivos
TIMEZONE = "America/Sao_Paulo"
VARIAVEIS = ["temperature_2m_min", "temperature_2m_max", "precipitation_sum"]

URL_API = "https://archive-api.open-meteo.com/v1/archive"
PASTA_DADOS = Path("dados")
ARQUIVO_JSON = PASTA_DADOS / "raw_open_meteo.json"


def coletar_dados():
    PASTA_DADOS.mkdir(parents=True, exist_ok=True)

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": DATA_INICIO,
        "end_date": DATA_FIM,
        "daily": ",".join(VARIAVEIS),
        "timezone": TIMEZONE,
    }

    print(f"Iniciando coleta para {LOCALIDADE} ({DATA_INICIO} a {DATA_FIM})...")
    resposta = requests.get(URL_API, params=params, timeout=30)
    resposta.raise_for_status()

    dados_brutos = resposta.json()

    # Preserva a resposta original da API com metadados da coleta
    payload_preservado = {
        "metadados_coleta": {
            "localidade": LOCALIDADE,
            "data_hora_coleta_utc": datetime.now(timezone.utc).isoformat(),
            "url_requisitada": resposta.url,
        },
        "resposta_api": dados_brutos,
    }

    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(payload_preservado, f, ensure_ascii=False, indent=2)

    print(f"Coleta concluída! JSON original salvo em: {ARQUIVO_JSON}")


if __name__ == "__main__":
    coletar_dados()
