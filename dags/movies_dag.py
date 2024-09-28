from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from src.fetch_movies import fetch_movies
from src.transform_movies import validation_aka_transformation

api_url = os.environ.get('API_URL')
authorization_key = os.environ.get('AUTHORIZATION_KEY')

def on_failure_callback(**context):
    print(f"Task {context['task_instance_key_str']} failed.")

default_args = {
    'owner': 'omar',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': on_failure_callback
}

# def fetch_movies_task(**kwargs):
#     page = 1
#     endpoint = '/movie/popular'
#     movies = fetch_movies(api_url, authorization_key, endpoint, page)
#     return movies
#
# def transform_movies_task(**kwargs):
#     ti = kwargs['ti']
#     fetched_movies = ti.xcom_pull(task_ids='fetch_movies')
#     transform_movies=validation_aka_transformation(fetched_movies)
#     return transform_movies

with DAG(
    dag_id="movies_pipeline_v05",
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024,9,26),
    tags= ["fetch"]
) as dag:

    # fetch_task = PythonOperator(
    #     task_id='fetch_movies',
    #     python_callable=fetch_movies_task,
    #     provide_context=True,
    #     dag=dag
    # )
    #
    # transform_task = PythonOperator(
    #     task_id='transform_movies',
    #     python_callable=transform_movies_task,
    #     provide_context=True,
    #     dag=dag
    # )

    spark_task = SparkSubmitOperator(
        task_id='movies_etl',
        application='/opt/airflow/AstroMRS/movies.py',
        conn_id='spark_conn',
        dag=dag
    )

    # fetch_task >> transform_task
    spark_task
