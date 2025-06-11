🇺🇸 This README is also available in [English](README.md)

# Challenge DevOps 1 - Leon Denizard


## 📁 Estrutura esperada de pastas e arquivos
+
+> 📌 Os scripts devem ser executados a partir da pasta `scripts/`, pois os caminhos relativos assumem essa posição.

```
dev-ops-challenge-1/
├── applications/
│   ├── production/
│   │   └── app_config.yaml
│   ├── staging/
│   │   └── app_config.yaml
│   └── preprod/
│       └── app_config.yaml
├── output-check-health/
├── scripts/
├── README.md
└── README.pt-BR.md

```

## 📌 Migrates

Script responsável por migrar e sincronizar a versão de configuração de um ambiente base (ex: `production`) para um ambiente alvo (`staging`, `preprod`), verificando também outras diferenças entre os arquivos YAML.

---

### ⚙️ Destaques técnicos

* Utiliza a biblioteca **DeepDiff** para identificar divergências (sem aplicar além da chave `version`).
* Suporte à flag `--dry-run` para simular a execução sem alterar arquivos.
* Gera **logs detalhados** da operação, inclusive no modo dry-run.
* Os arquivos de log são salvos na **mesma pasta do ambiente de destino**.

---

### 🚀 Como rodar?

#### 1. Pré-requisitos

* Ter o **Python 3.8+** instalado.
  Caso não tenha, baixe e instale em: [https://www.python.org/downloads/](https://www.python.org/downloads/)

* Instalar a dependência necessária:

```bash
pip install deepdiff
```

---

#### 2. Navegue até o diretório `scripts/`

```bash
cd scripts
```

---

#### 3. 🔁 Execuções

Use o comando abaixo para visualizar a ajuda e opções via terminal:

```bash
python migrate.py -h
```

##### ✅ Execução normal (com atualização da versão):

```bash
python migrate.py production staging
```

##### 🔍 Execução em modo simulação (`--dry-run`):

```bash
python migrate.py production preprod --dry-run
```

---

### 📝 Logs

Ao final da execução, um arquivo de log será criado no mesmo diretório do `app_config.yaml` do ambiente alvo.
Exemplos:

* `applications/preprod/log_dry-run.txt` (modo simulação)
* `applications/staging/app_config.log` (execução real)

---

## 📌 Check Health

Script responsável por analisar se o ambiente segue boas práticas de resiliência e segurança.

---

### ⚙️ O que ele verifica?

* Se o número de **replicas** é suficiente para garantir alta disponibilidade.
* Se há definição de **recursos (CPU e memória)**.
* Se as **variáveis de ambiente** usam **secrets** via `valueFrom > secretKeyRef`.
* Se a estratégia de deploy utiliza **rolling update**, com `maxSurge` e `maxUnavailable` definidos.

---

### 🚀 Como rodar?

#### 1. Navegue até o diretório `scripts/`

```bash
cd scripts
```

#### 2. Execute o script informando o ambiente

```bash
python check_health.py staging
```

---

### 📄 Relatório gerado

* O resultado é exibido no terminal com os status de conformidade.
* Um arquivo é salvo em `output-check-health/health_report.txt` com os resultados formatados por ambiente analisado.

Exemplo:

```
Environmental health analysis: staging
----------------------------------------
❌ Insufficient replicas: 1 minimal replicas 2
❌ Resources not defined correctly CPU=400m, Memory=None
❌ Environment variable 'NODE_ENV' dont use secretKeyRef
✔️ Valid 'rolling' deployment strategy (maxUnavailable=1, maxSurge=1)
Report saved in output-check-health/health_report.txt
```

---

### ⚠️ Possíveis erros

* Arquivo `app_config.yaml` não encontrado para o ambiente informado.
* Ambiente não informado: use `python check_health.py <nome_do_ambiente>`

---

