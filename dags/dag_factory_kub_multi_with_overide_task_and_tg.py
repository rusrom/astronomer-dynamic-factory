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
    ("dag_overide_task_and_task_grop_1", "print('Hello from multi 1!')"),
    ("dag_overide_task_and_task_grop_2", "print('Hello from multi 2!')"),
    ("dag_overide_task_and_task_grop_3", "print('Hello from multi 3!')"),
    ("dag_overide_task_and_task_grop_4", "print('Hello from multi 4!')"),
]

extra_task = {
    "task_id": "extra-pod-task",
    "operator": "airflow.providers.cncf.kubernetes.operators.pod.KubernetesPodOperator",
    "config_file": "/home/rusrom/.kube/config",
    "image": "python:3.12-slim",
    "cmds": ["python", "-c"],
    "arguments": ["print('Hello from KubernetesPodOperator!')"],
    "name": "example-pod-task",
    "namespace": "default",
    "get_logs": True,
    "container_resources": {
        "__type__": "kubernetes.client.models.V1ResourceRequirements",
        "limits": {"cpu": "1", "memory": "1024Mi"},
        "requests": {"cpu": "0.5", "memory": "512Mi"},
    },
    "dependencies": ["hello-world-pod"]
}

for dag_id, print_stmt in dag_variants:
    # Deep copy the base config
    dag_config = copy.deepcopy(base_config)

    if dag_id in (
        "dag_overide_task_and_task_grop_2",
        "dag_overide_task_and_task_grop_4",
    ):
        # dag_config["kubernetes_pod_dag"]["schedule"] = "0 12 * * *"
        dag_config["kubernetes_pod_dag"]["schedule"] = "@daily"
        dag_config["kubernetes_pod_dag"]["tasks"].append(extra_task)

        tags = dag_config["default"]["tags"] + ["overide"]
        dag_config["kubernetes_pod_dag"]["tags"] = tags
        # dag_config["kubernetes_pod_dag"]["tags"] = ["overide", "kubernetes", "multi_dag"]

    # Change the DAG id and arguments
    dag_config[dag_id] = dag_config.pop("kubernetes_pod_dag")
    dag_config[dag_id]["tasks"][0]["arguments"] = [print_stmt]
    # Optionally, set a unique description
    dag_config[dag_id]["description"] = f"A DAG that prints: {print_stmt}"
    # Load the DAG into Airflow
    load_yaml_dags(globals_dict=globals(), config_dict=dag_config)
