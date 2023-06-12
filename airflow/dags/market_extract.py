import pendulum
from src.configs.config import MARKET_CATEGORIES
from src.market_patterns import WorldMarketDataStrategy

from airflow.decorators import dag, task
from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.timetables.trigger import CronTriggerTimetable

DEVELOPER = "Wes"
PROCESS_NAME = "market_extract"


# Default arguments that will be passed to every task
DAG_ARGS = {
    "owner": DEVELOPER,
    "retries": 1,
    "retry_delay": pendulum.duration(seconds=10),
}


# DAG definition
@dag(
    start_date=pendulum.datetime(year=2023, month=1, day=1, tz="America/New_York"),
    schedule=CronTriggerTimetable("*/15 * * * *", timezone="UTC"),
    description=None,
    catchup=False,
    max_active_runs=1,
    tags=["bdo", "market_data"],
    default_args=DAG_ARGS,
)
def market_extract() -> DAG:  # noqa: C901, RUF100
    """
    Extracts market data from the BDO Market Websites for each country-region.\n
    This data is then stored in a Postgres database for later use.\n
    This DAG is scheduled to run on every 15th minute interval.
    """

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    @task
    def get_market_data() -> None:
        strategy = WorldMarketDataStrategy()
        strategy.update_market_data(main_categories=MARKET_CATEGORIES)

    update_pg_with_market_data = get_market_data()

    start >> update_pg_with_market_data >> end


run_dag = market_extract()
