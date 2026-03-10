# main.py
import os
import json
import requests
from dotenv import load_dotenv
from google.cloud import bigquery
from google.cloud import secretmanager
from google.cloud.exceptions import GoogleCloudError
from google.oauth2 import service_account

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configuração ---
API_KEY_SECRET_NAME = os.getenv("API_KEY_SECRET_NAME")
GCP_SA_KEY_SECRET_NAME = os.getenv("GCP_SA_KEY_SECRET_NAME")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BIGQUERY_DATASET = os.getenv("BIGQUERY_DATASET")

# A URL base da API REST da CoinCap.
API_BASE_URL = "https://rest.coincap.io/v3/"

def get_secret(secret_name: str) -> str | None:
    """Busca o valor de um segredo no Google Secret Manager."""
    if not secret_name:
        print("O nome do segredo não está configurado.")
        return None
    try:
        print(f"Buscando segredo: {secret_name.split('/')[-3]}...")
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(name=secret_name)
        return response.payload.data.decode("UTF-8")
    except (GoogleCloudError, Exception) as e:
        print(f"Erro ao buscar o segredo '{secret_name}': {e}")
        return None

def get_credentials_from_secret_manager() -> service_account.Credentials | None:
    """
    Busca as credenciais da conta de serviço no Google Secret Manager.
    """
    secret_payload = get_secret(GCP_SA_KEY_SECRET_NAME)
    if not secret_payload:
        print("Não foi possível buscar as credenciais da conta de serviço.")
        return None

    try:
        # Carrega a string do segredo como um objeto JSON
        credentials_info = json.loads(secret_payload)
        # Cria as credenciais a partir das informações
        return service_account.Credentials.from_service_account_info(credentials_info)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Erro ao processar as credenciais do Secret Manager: {e}")
        return None

def fetch_from_coincap(endpoint: str, api_key: str) -> list[dict]:
    """Busca dados da CoinCap usando um endpoint específico e chave de API."""
    if not api_key:
        print("Chave da API ausente.")
        return []

    # Aqui montamos a URL dinâmica
    full_url = f"{API_BASE_URL}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        print(f"Buscando dados em: {full_url}")
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        return response.json().get("data", [])
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar {endpoint}: {e}")
        return []

def remove_tokens_field(data_list: list[dict]) -> list[dict]:
    """Remove o campo 'tokens' de cada registro da lista."""
    for row in data_list:
        # O pop remove a chave se ela existir, sem causar erro se não existir
        row.pop('tokens', None)
    return data_list

def load_data_to_bigquery(data: list[dict], credentials, table_name: str):
    if not data or not credentials:
        return

    try:
        client = bigquery.Client(project=GCP_PROJECT_ID, credentials=credentials)
        # O table_name agora vem por parâmetro
        table_id = f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{table_name}"

        print(f"Limpando dados existentes na tabela {table_name}...")
        query_delete = f"TRUNCATE TABLE `{table_id}`"
        query_job = client.query(query_delete)
        query_job.result()  # Aguarda a conclusão da limpeza

        print(f"Enviando {len(data)} linhas para a tabela: {table_id}...")
        errors = client.insert_rows_json(table_id, data)

        if not errors:
            print(f"Sucesso na carga da tabela {table_name}.")
        else:
            print(f"Erros encontrados: {errors}")
    except Exception as e:
        print(f"Erro ao interagir com BigQuery: {e}")

def main():
    """Main function to run the data pipeline."""
    api_key = get_secret(API_KEY_SECRET_NAME)
    credentials = get_credentials_from_secret_manager()
    if not credentials:
        print("Falha na autenticação.")
        return

    # 1. Busca os dados
    assets_data = fetch_from_coincap("assets", api_key)
    
    if assets_data:
        # 2. Remove o campo indesejado
        assets_limpos = remove_tokens_field(assets_data)
        
        # 3. Faz a carga com os dados já filtrados
        load_data_to_bigquery(assets_limpos, credentials, "tb_criptomoedas_disponiveis")

    # CARGA 2: Mercados do Bitcoin
    bitcoin_markets = fetch_from_coincap("assets/bitcoin/history?interval=m5", api_key)
    load_data_to_bigquery(bitcoin_markets, credentials, "tb_bitcoin_mercado")

if __name__ == "__main__":
    main()
