from airflow.sensors.external_task import ExternalTaskSensor, ExternalTaskMarker

def task_name(parent_id, child_id):
    parent_name = ".".join(parent_id.split(".")[-2:])
    child_name = ".".join(child_id.split(".")[-2:])
    return f"{parent_name}--TO--{child_name}"

def subscribe_to(dag_id, parent_dag_ids, timeout=600, allowed_states=['success'], failed_states=['failed', 'skipped'],
                mode="reschedule"):
    tasks = []
    for parent_id in parent_dag_ids:
        tasks.append(ExternalTaskSensor(
            task_id=task_name(parent_id, dag_id),
            external_dag_id=parent_id,
            external_task_id=task_name(parent_id, dag_id),
            timeout=timeout,
            allowed_states=allowed_states,
            failed_states=failed_states,
            mode=mode,
        ))
    return tasks


def notify(dag_id, child_dag_ids):
    tasks = []
    for child_id in child_dag_ids:
        tasks.append(ExternalTaskMarker(
            task_id=task_name(dag_id, child_id),
            external_dag_id=child_id,
            external_task_id=task_name(dag_id, child_id),
        ))
    return tasks
