from datetime import datetime, timedelta
import requests
import os

from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.providers.http.operators.http import SimpleHttpOperator
# from airflow.providers.mongo.hooks.mongo import MongoHook

API_URL = os.environ.get('API_URL')
AUTHORIZATION_KEY = os.environ.get('AUTHORIZATION_KEY')

def on_failure_callback(**context):
    print(f"Task {context['task_instance_key_str']} failed.")

default_args = {
    'owner': 'omar',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': on_failure_callback
}

def fetch_movies(ti):
    api_url = ti.xcom_pull(task_ids='something', key='api_url')
    authorization_key = ti.xcom_pull(task_ids='something', key='authorization_key')
    endpoint = ti.xcom_pull(task_ids='something', key='endpoint')
    page = ti.xcom_pull(task_ids='something', key='page')

    page_movies = []
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authorization_key}"
    }

    if page:
        page_url = f"{api_url}{endpoint}?language=en-US&page={page}"
    else:
        page_url = f"{api_url}{endpoint}"

    response = requests.get(page_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if endpoint == '/movie/latest':
            return [data]
        else:
            movies = data.get('results', [])
            page_movies.extend(movies)
            print(f"You fetched {page_movies}")
            return page_movies
    else:
        print(f"Failed to fetch page {page}: {response.status_code}")
        return []

def something(ti):
    ti.xcom_push(key='api_url', value=API_URL)
    ti.xcom_push(key='authorization_key', value=AUTHORIZATION_KEY)
    ti.xcom_push(key='endpoint', value='/movie/popular')
    ti.xcom_push(key='page', value=1)


with DAG(
    dag_id="movies_pipeline_v01",
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024,9,7),
    catchup=True,
    tags= ["fetch"]
) as dag:

    # fetching_task = SimpleHttpOperator(
    #     task_id='fetch_movies',
    #     method='GET',
    #     headers={"Content-Type": "application/json"},
    #     dag=dag
    # )
    setup_task = PythonOperator(
        task_id='something',
        python_callable=something,
        dag=dag
    )
    fetch_task = PythonOperator(
        task_id='fetch_movies',
        python_callable=fetch_movies,
        dag=dag
    )

    setup_task >> fetch_task
