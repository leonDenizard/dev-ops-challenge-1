🇧🇷 Este README também está disponível em [Português](README.pt-BR.md)

# Challenge DevOps 1 - Leon Denizard

## 📁 Expected folder and file structure
+
+> 📌 Scripts must be run from the `scripts/` folder, as relative paths assume that position.

```
applications/
├── production/
│ └── app_config.yaml
├── staging/
│ └── app_config.yaml
├── preprod/
│ └── app_config.yaml
```

## 📌 Migrates

Script responsible for migrating and synchronizing the configuration version from a base environment (e.g., `production`) to a target environment (`staging`, `preprod`), also checking for other differences between YAML files.

---

### ⚙️ Technical Highlights

* Uses the **DeepDiff** library to identify divergences (only applies changes to the `version` key).
* Supports the `--dry-run` flag to simulate execution without altering files.
* Generates **detailed logs** of the operation, including in dry-run mode.
* Log files are saved in the **same directory as the target environment**.

---

### 🚀 How to run it?

#### 1. Prerequisites

* Have **Python 3.8+** installed.  
  CIf not, download and install it from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

* Install the required dependency:

```bash
pip install deepdiff
```

---

#### 2. Navigate to the `scripts/` directory

```bash
cd scripts
```

---

#### 3. 🔁 Executions

Use the command below to view CLI help and options:

```bash
python migrate.py -h
```

##### ✅ Standard execution (updates the version):

```bash
python migrate.py production staging
```

##### 🔍 Simulation mode execution (`--dry-run`):

```bash
python migrate.py production preprod --dry-run
```

---

### 📝 Logs

At the end of the execution, a log file will be created in the same directory as the target environment’s `app_config.yaml`

Examples:

* `applications/preprod/log_dry-run.txt` (simulation mode)
* `applications/staging/app_config.log` (real execution)

---

## 📌 Check Health

Script responsible for analyzing whether the environment follows best practices for resilience and security.

---

### ⚙️ What does it check?

* If the number of **replicas** s sufficient to ensure high availability.
* If resources  **recursos (CPU e memória)** are defined.
* If **environment variables** use **secrets** via `valueFrom > secretKeyRef`.
* If the deployment strategy uses **rolling update**, with `maxSurge` and `maxUnavailable` properly defined.

---

### 🚀  How to run it?

#### 1.  Navigate to the `scripts/` directory

```bash
cd scripts
```

#### 2. Run the script by specifying the environment

```bash
python check_health.py staging
```

---

### 📄 Generated Report

* The result is displayed in the terminal with compliance status.
* A file is saved in `output-check-health/health_report.txt` cwith the results formatted by analyzed environment.

Example:

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

### ⚠️ Possible Errors

* `app_config.yaml` file not found for the specified environment.
* Environment not provided: use `python check_health.py <nome_do_ambiente>`

---

