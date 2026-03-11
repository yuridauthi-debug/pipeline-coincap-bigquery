# Pipeline de Dados: CoinCap para BigQuery

Este projeto automatiza a extração de dados de criptomoedas da API [CoinCap](https://pro.coincap.io/api-docs) e realiza a carga (ETL) diretamente para o Google BigQuery. O pipeline é seguro, utilizando o **Google Secret Manager** para gerenciar chaves de API e credenciais de conta de serviço.



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
2. **Crie um ambiente virtual e instale as dependências:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
3. **Configure as Variáveis de Ambiente:**
Crie um arquivo .env na raiz do projeto com as seguintes informações:

```Snippet de código

API_KEY_SECRET_NAME=projects/seu-projeto/secrets/NOME_DA_API_KEY/versions/latest
GCP_SA_KEY_SECRET_NAME=projects/seu-projeto/secrets/NOME_DA_SA/versions/latest
GCP_PROJECT_ID=seu-projeto-id
BIGQUERY_DATASET=seu_dataset_id
```
## 🚀 Como Executar
Após configurar o ambiente e as variáveis, execute o pipeline com:

```Bash

python3 main.py
```
## 📂 Estrutura do Banco de Dados
O script realiza a carga nas seguintes tabelas no BigQuery:
* `tb_criptomoedas_disponiveis`: Lista de todos os ativos.
* `tb_bitcoin_mercado`: Histórico de preços do Bitcoin.

```Script de criação

CREATE OR REPLACE TABLE `seu-projeto.seu_dataset.tb_criptomoedas_disponiveis` (
    id STRING OPTIONS(description="Identificador único da criptomoeda"),
    rank STRING OPTIONS(description="Posição no ranking de capitalização de mercado"),
    symbol STRING OPTIONS(description="Símbolo da criptomoeda (ex: BTC, ETH)"),
    name STRING OPTIONS(description="Nome completo da criptomoeda"),
    supply STRING OPTIONS(description="Quantidade circulante atual da moeda"),
    maxSupply STRING OPTIONS(description="Quantidade máxima que existirá da moeda"),
    marketCapUsd STRING OPTIONS(description="Capitalização de mercado em Dólares americanos"),
    volumeUsd24Hr STRING OPTIONS(description="Volume negociado nas últimas 24 horas em USD"),
    priceUsd STRING OPTIONS(description="Preço atual em Dólares americanos"),
    changePercent24Hr STRING OPTIONS(description="Percentual de variação nas últimas 24 horas"),
    vwap24Hr STRING OPTIONS(description="Preço médio ponderado pelo volume nas últimas 24 horas"),
    explorer STRING OPTIONS(description="Link para o explorador de blocos da moeda")
)
CLUSTER BY symbol;

CREATE OR REPLACE TABLE `seu-projeto.seu_dataset.tb_bitcoin_mercado` (
    circulatingSupply INTEGER OPTIONS(description="Quantidade em circulação no momento do registro"),
    priceUsd STRING OPTIONS(description="Preço em Dólares americanos no momento do registro"),
    time INTEGER OPTIONS(description="Timestamp (Unix epoch) do registro"),
    date TIMESTAMP OPTIONS(description="Data e hora do registro em formato ISO 8601")
)
PARTITION BY TIMESTAMP_TRUNC(date, MONTH)
CLUSTER BY date;
```

##🤝 Contribuições
Sinta-se à vontade para abrir Issues ou enviar Pull Requests para melhorias no pipeline!
