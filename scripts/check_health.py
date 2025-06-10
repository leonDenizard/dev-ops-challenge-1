import yaml
import os
import sys
from pathlib import Path  # Adicione isso

# le o yaml e retorna o conteudo em chave valor (object in js)
def load_yaml(path):
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML file at {path}: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ File not found: {path}")
        sys.exit(1)


# funçao responsavel por validar se existe resiliência do ambiente (replica, recurso, env seguro, estrategia de deploy)
def check_config(config):
    results = []

    #Testa se possui o minimo aceitavel de replicas para garantir a alta disponibilidade
    replicas = config.get('deployment', {}).get('replicas', 0)
    if replicas >= 2:
        results.append(f"✔️ Enough replicas: {replicas}")
    else:
        results.append(f"❌ Insufficient replicas: {replicas} minimal replicas 2")

    #Verifica se tem recursos cpu e memoria no arquivo de configuração
    resources = config.get('deployment', {}).get('resources', {})
    cpu = resources.get('cpu')
    memory = resources.get('memory')
    if cpu and memory:
        results.append(f"✔️ Defined Resources: CPU={cpu}, Memory={memory}")
    else:
        results.append(f"❌ Resources not defined correctly CPU={cpu}, Memory={memory}")

    # Verifica se as variaveis de ambiente possuem a estrutura de secret valueForm > secretKeyRef
    env = config.get('deployment', {}).get('env', [])
    all_env_ok = True
    
    for var in env:
        if 'valueFrom' not in var or 'secretKeyRef' not in var['valueFrom']:
            all_env_ok = False
            results.append(f"❌ Environment variable '{var.get('name')}' dont use secretKeyRef")
    if all_env_ok:
        results.append("✔️ All environment variables use secrets")

    #Armazena a estrategia de deploy utilizada
    strategy = config.get('deploy_strategy', {})
    strategy_type = strategy.get('type')
    max_unavailable = strategy.get('maxUnavailable')
    max_surge = strategy.get('maxSurge')
    
    # Verifica se e utilizada a estrategia 'rolling'
    if strategy_type == 'rolling':
        if max_unavailable is not None and max_surge is not None:
            results.append(f"✔️ Valid 'rolling' deployment strategy (maxUnavailable={max_unavailable}, maxSurge={max_surge})")
        else:
            results.append("⚠️ 'Rolling' strategy defined, but maxUnavailable or maxSurge missing")
    else:
        results.append(f"❌ Deployment strategy not recommended: '{strategy_type}', recommended 'rolling'")
    
    return results

#Funçao responsavel por gerar o relatorio das conformidades esperadas
def generate_health_report(env_name, file_path):
    
    #Tratamento de erro durante execuçao das funçoes
    try:
        #Armazena em config o conteudo chave valor
        config = load_yaml(file_path)
        
        #Envia a config via parametro para 'checks'
        checks = check_config(config)

        #Cabeçalho terminal
        print(f"\n Environmental health analysis: {env_name}")
        #Add 40 caracter - (formataçao) terminal
        print("-" * 40)
        
        #Exibe o resultado de cada validaçao da funcao "check_config"
        for check in checks:
            print(check)

        os.makedirs('../output-check-health', exist_ok=True)
        with open('../output-check-health/health_report.txt', 'a', encoding='utf-8') as f:
            #Dentro do report escreve cabeçalho 'estilizado'
            f.write(f"\n Health report : {env_name}\n")
            f.write("-" * 40 + "\n")
            #Percorre cada validaçao da função check_config pulando uma linha
            for check in checks:
                f.write(check + "\n")
        print("Report saved in output-check-health/health_report.txt\n")
    except Exception as e:
        print(f"Error in process {env_name}: {e}")

if __name__ == "__main__":
    #Valida se esta sendo informado os 2 argumentos validos no terminal app e environment
    if len(sys.argv) != 2:
        print("Use: python check_health.py <environment_name>")
        sys.exit(1)

    #Armazena o ambiente digitado em minuscula
    env_name = sys.argv[1].lower()
    
    #Monta o path ate config.yamel com base no environment
    file_path = f"../applications/{env_name}/app_config.yaml"

    if not Path(file_path).exists():
        print(f"Configuration file not found for environment: {env_name}")
        sys.exit(1)

    generate_health_report(env_name, file_path)
