import inspect
from typing import List

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from pandasdb.io import TableSchema
from pandasdb.scheduling import subscribe_to, notify
from datetime import datetime, timedelta


class DAGDefinition:
    dag_id: str
    description: str
    start_date: datetime = days_ago(2)
    catchup: bool = False
    default_args: dict = {
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 5,
        'retry_delay': timedelta(minutes=5)
    }

    def __init__(self, **spec):
        self.spec = spec

        required = ["dag_id", "description", "start_date", "catchup", "default_args", "tags"]
        for key in required:
            if key not in self.spec:
                try:
                    self.spec[key] = getattr(self, key)
                except:
                    raise ValueError(f"{key} not provided")

    def extraction(self):
        raise NotImplementedError()

    def transformation(self, *args, **kawrgs):
        raise NotImplementedError()

    def output_table(self) -> TableSchema:
        raise NotImplementedError()

    def create(self):
        @dag(**self.spec)
        def generate_dag():
            @task(multiple_outputs=True)
            def extract_input_tables():
                return self.extraction()

            @task()
            def generate_table(tables):
                table_args = list(inspect.signature(self.transformation).parameters.keys())
                input_tables = {name: tables[name] for name in table_args}
                return self.transformation(**input_tables)

            @task()
            def store_table(table):
                self.output_table().replace_with(table)

            input_tables = extract_input_tables()
            output_table = generate_table(input_tables)
            stored_table = store_table(output_table)

            if hasattr(self, "dependencies"):
                subscribe_to(self.spec["dag_id"], self.dependencies) >> input_tables

            if hasattr(self, "notify"):
                stored_table >> notify(self.spec["dag_id"], self.notify)

        return generate_dag()
