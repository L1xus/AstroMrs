from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

api_url = os.environ.get("API_URL")
authorization_key = os.environ.get("AUTHORIZATION_KEY")


def on_failure_callback(**context):
    print(f"Task {context['task_instance_key_str']} failed.")


default_args = {
    "owner": "omar",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": on_failure_callback,
}

with DAG(
    dag_id="movies_pipeline_v06",
    default_args=default_args,
    schedule_interval="0 15 * * 1",
    start_date=datetime(2024, 10, 5),
    tags=["etl"],
) as dag:
    spark_task = SparkSubmitOperator(
        task_id="movies_etl",
        application="/opt/airflow/AstroMRS/movies.py",
        conn_id="spark_conn",
        dag=dag,
    )

    spark_task
