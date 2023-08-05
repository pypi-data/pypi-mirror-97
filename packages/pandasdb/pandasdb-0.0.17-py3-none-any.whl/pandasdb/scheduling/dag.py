import inspect

from airflow import DAG
from airflow.utils.dates import days_ago
from pandasdb import Async
from pandasdb.io import TableSchema
from pandasdb.scheduling import subscribe_to, notify
from datetime import datetime, timedelta


class DAGDefinition:
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

        for required in ["dag_id", "description", "start_date", "catchup", "default_args", "tags"]:
            if required not in self.spec:
                try:
                    self.spec[required] = getattr(self, required)
                except:
                    raise ValueError(f"{required} not provided")

    def extraction(self):
        raise NotImplementedError()

    def transformation(self, *args, **kawrgs):
        raise NotImplementedError()

    def output_table(self) -> TableSchema:
        raise NotImplementedError()

    def create(self):

        DagDef = DAG(**self.spec)

        with DagDef as dag:
            @dag.task(multiple_outputs=True)
            def extract_input_tables():
                tables = self.extraction()
                assert isinstance(tables, dict), "The input tables should be a dictionary"

                tables = {name: table.df if hasattr(table, "df") else table for name, table in tables.items()}

                jobs = {name: job for name, job in tables.items() if callable(job)}
                tables.update(Async.handle(**jobs))

                return tables

            @dag.task
            def generate_table(tables):
                table_args = list(inspect.signature(self.transformation).parameters.keys())
                input_tables = {name: tables[name] for name in table_args}
                return self.transformation(**input_tables)

            @dag.task
            def store_table(table):
                self.output_table().replace_with(table)

            input_tables = extract_input_tables()
            output_table = generate_table(input_tables)
            stored_table = store_table(output_table)

            if hasattr(self, "dependencies"):
                subscribe_to(self.spec["dag_id"], self.dependencies) >> input_tables

            if hasattr(self, "notify"):
                stored_table >> notify(self.spec["dag_id"], self.notify)

        return DagDef
