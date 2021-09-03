from datetime import timedelta # YYYY-MM-DD
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from scrape_to_s3 import scrape_import_to_s3

default_args

default_args = {
                'owner': '',
                'start_date': datetime(2021, 9, 1),
                'depends_on_past': False,
                'email': ['bobbyhuck@gmail.com']
                'email_on_failure': False,
                'email_on_retry': False,
                'retries': 5,
                'retry_delay': timedelta(minutes=1)
                }

dag = DAG(
         'scrap_to_s3_dag',
         default_args=default_args,
         description='My first DAG',
         schedule_interval=timedelta(days=1)
         )

def just_a_function():
    print("I'm going to show you something :)")


# run_etl = PythonOperator(
#     task_id='whole_spotify_etl',
#     python_callable=run_spotify_etl,
#     dag=dag,
# )

# run_etl

run_scrape_to_s3_dag = PythonOperator(
                                      task_id='scraping_to_s3',
                                      python_callable=scrape_import_to_s3,
                                      dag=dag
                                     )

run_scrape_to_s3_dag