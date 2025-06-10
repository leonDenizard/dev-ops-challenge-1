import yaml
import sys
from deepdiff import DeepDiff
from pathlib import Path
import argparse

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


#Funçao responsavel por salvar data em yaml
def save_yaml(path, data):
    with open(path, 'w') as f:
        #chaves do yaml não sejam ordenadas, mantendo originalidade do que foi recebido data
        yaml.dump(data, f, sort_keys=False)

#Função responsável por receber uma lista de logs e um caminho do arquivo e salvar os logs no arquivo, cada item da lista em uma nova linha.
def write_log(lines, log_path):
    with open(log_path, 'w', encoding='utf-8') as log_file:
        for line in lines:
            log_file.write(line + '\n')

#Funcao responsavel por receber o environment e montar o path
def get_env_file_path(env_name):
    return Path(f"../applications/{env_name}/app_config.yaml")

# Função responsavel por comparar e migrar configs do ambiente base (production)
# para o target (staging, preprod). se dry_run for False, aplica a migração da versao.
# Também registra diferenças encontradas entre os arquivos
def migrate_config(base_path, target_path, dry_run=False):
    base = load_yaml(base_path)
    target = load_yaml(target_path)

    #Inicializa a lista de logs
    logs = []

    old_version = target.get('version')
    new_version = base.get('version')

    #Compara as versoes da aplicacao entre os ambientes
    if old_version != new_version:
        #Adiciona mensagem de atualizaçao ao log
        logs.append(f"✅ Update 'version': {old_version} → {new_version}")
        #Se não estiver em modo --dry-run realiza update no target
        if not dry_run:
            target['version'] = new_version
    else:
        logs.append(f"✔️ 'version' is already updated.")

    #Utilizando a lib DeepDiff para comparar as diferenças entre target e o base sem levar em consideraçao a ordem dos elementos
    diff = DeepDiff(target, base, ignore_order=True)

    if diff:
        logs.append("\n🔍 Other differences found (not applied):")
        for diff_type, changes in diff.items():
            if isinstance(changes, dict):
                for change_key, change_value in changes.items():
                    logs.append(f"  - [{diff_type}] {change_key} → {change_value}")
            elif isinstance(changes, list):
                for item in changes:
                    logs.append(f"  - [{diff_type}] {item}")
            else:
                logs.append(f"  - [{diff_type}] {changes}")
    else:
        logs.append("🎉 No other differences found.")

    if dry_run:
        logs.append("\n🚫 [Dry-run] No changes saved.")
        dry_log_path = Path(target_path).parent / "log_dry-run.txt"
        write_log(logs, dry_log_path)
        logs.append(f"💾 Log saved in: {dry_log_path.resolve()}")
    else:
        save_yaml(target_path, target)
        logs.append("💾 File updated with new version.")
        log_path = Path(target_path).with_suffix('.log')
        write_log(logs, log_path)

    print("\n".join(logs))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Configuration migration script.")
    parser.add_argument("base_env", help="Base environment(ex: production)")
    parser.add_argument("target_env", help="Base target (ex: staging or preprod)")
    parser.add_argument("--dry-run", action="store_true", help="Simulates migration without saving changes")
    args = parser.parse_args()

    base_path = get_env_file_path(args.base_env)
    target_path = get_env_file_path(args.target_env)

    if not base_path.exists():
        print(f"❌ File base not found: {base_path}")
        sys.exit(1)
    if not target_path.exists():
        print(f"❌ File saved not found: {target_path}")
        sys.exit(1)

    migrate_config(base_path, target_path, dry_run=args.dry_run)
