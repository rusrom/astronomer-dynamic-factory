import copy
import yaml
from pathlib import Path
from airflow.configuration import conf as airflow_conf
from dagfactory import load_yaml_dags

config_dir = Path(airflow_conf.get("core", "dags_folder")) / "configs"
config_file = str(config_dir / "example_kub_dag.yml")

# Load the base YAML config
with open(config_file) as f:
    base_config = yaml.safe_load(f)

# List of (dag_id, print_statement)
dag_variants = [
    ("kubernetes_pod_dag_hello", "print('Hello from KubernetesPodOperator!')"),
    ("kubernetes_pod_dag_elvis", "print('Hello from Elvis!')"),
    ("kubernetes_pod_dag_tomjones", "print('Hello from Tom Jones!')"),
    ("kubernetes_pod_dag_snap", "print('Hello from Snap!')"),
]

for dag_id, print_stmt in dag_variants:
    # Deep copy the base config
    dag_config = copy.deepcopy(base_config)
    # Change the DAG id and arguments
    dag_config[dag_id] = dag_config.pop("kubernetes_pod_dag")
    dag_config[dag_id]["tasks"][0]["arguments"] = [print_stmt]
    # Optionally, set a unique description
    dag_config[dag_id]["description"] = f"A DAG that prints: {print_stmt}"
    # Load the DAG into Airflow
    load_yaml_dags(globals_dict=globals(), config_dict=dag_config)
