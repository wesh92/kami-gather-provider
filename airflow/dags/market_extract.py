import pendulum

from airflow.decorators import dag
from airflow.models import DAG
from airflow.operators.empty import EmptyOperator

DEVELOPER = "Wes"
PROCESS_NAME = "market_extract"


# Default arguments that will be passed to every task
DAG_ARGS = {
    "owner": DEVELOPER,
    "retries": 1,
    "retry_delay": pendulum.duration(minutes=2),
}


# DAG definition
@dag(
    start_date=pendulum.datetime(year=2023, month=1, day=1, tz="America/New_York"),
    schedule_interval=None,
    description=None,
    catchup=False,
    max_active_runs=1,
    tags=["bdo", "market_data"],
    default_args=DAG_ARGS,
)
def boilerplate_dag() -> DAG:  # noqa: C901, RUF100
    """
    Put your description of the dag here (including any params it takes).
    This docstring will appear at the top of the UI within the specific DAG's page.
    """

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    start >> end


run_dag = boilerplate_dag()
