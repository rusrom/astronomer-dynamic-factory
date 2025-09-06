from pathlib import Path

# from airflow.models.dag import DAG
from airflow.configuration import conf as airflow_conf
from dagfactory import load_yaml_dags

config_dir = Path(airflow_conf.get("core", "dags_folder")) / "configs"
config_file = str(config_dir / "example_dag_factory.yml")

# load_yaml_dags(globals_dict=globals(), dags_folder=config_dir)
load_yaml_dags(globals_dict=globals(), config_filepath=config_file)
# load_yaml_dags(globals_dict=globals(), dags_folder=airflow_conf.get("core", "dags_folder"), config_filepath=config_dir)


if __name__ == "__main__":
    print(config_dir)