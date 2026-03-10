# Pipeline de Dados: CoinCap para BigQuery

Este projeto automatiza a extração de dados de criptomoedas da API [CoinCap](https://coincap.io/) e realiza a carga (ETL) diretamente para o Google BigQuery. O pipeline é seguro, utilizando o **Google Secret Manager** para gerenciar chaves de API e credenciais de conta de serviço.



## 🚀 Funcionalidades
* **Extração Automatizada:** Busca dados de ativos e histórico de mercado do Bitcoin.
* **Segurança:** Gerencia credenciais via Google Secret Manager.
* **Limpeza de Dados:** Processamento dinâmico para remover campos desnecessários antes da carga.
* **Integridade:** Utiliza `TRUNCATE` no BigQuery para evitar duplicidade de dados em novas execuções.

## 🛠 Pré-requisitos
Antes de executar, certifique-se de ter:
* Python 3.9+ instalado.
* Um projeto no Google Cloud Platform (GCP).
* API habilitada: `BigQuery API` e `Secret Manager API`.
* Uma Conta de Serviço (Service Account) com permissões de `BigQuery Data Editor` e `Secret Manager Secret Accessor`.

## ⚙️ Configuração do Ambiente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
   cd seu-repositorio
Crie um ambiente virtual e instale as dependências:

Bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configure as Variáveis de Ambiente:
Crie um arquivo .env na raiz do projeto com as seguintes informações:

Snippet de código

API_KEY_SECRET_NAME=projects/seu-projeto/secrets/NOME_DA_API_KEY/versions/latest
GCP_SA_KEY_SECRET_NAME=projects/seu-projeto/secrets/NOME_DA_SA/versions/latest
GCP_PROJECT_ID=seu-projeto-id
BIGQUERY_DATASET=seu_dataset_id
🚀 Como Executar
Após configurar o ambiente e as variáveis, execute o pipeline com:

Bash

python3 main.py
📂 Estrutura do Banco de Dados
O script realiza a carga nas seguintes tabelas no BigQuery:

tb_criptomoedas_disponiveis: Lista de todos os ativos.

tb_bitcoin_mercado: Histórico de preços do Bitcoin.

Nota: Ambas as tabelas utilizam CLUSTER BY symbol para otimizar o custo e a performance das consultas.

🤝 Contribuições
Sinta-se à vontade para abrir Issues ou enviar Pull Requests para melhorias no pipeline!
