from airflow import DAG
from datetime import datetime
import os
import sys
from airflow.operators.python import PythonOperator
# from airflow.operators.bash_operator import BashOperator
# from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
# from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator

# To Avoid insertion Error (Running Airflow on Docker), # To Avoid imports error #This must stay above the file imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # moved back twice to get the root directory
# C:\\Users\\HP\\Desktop\\Data_Eng_3\\reddit-data-eng  #root dir

from pipelines.reddit_pipeline import reddit_pipeline
from pipelines.aws_s3_pipeline import upload_s3_pipeline

default_args = {
    'owner': 'Ataime Benson',
    'start_date': datetime(2024, 6, 3)
}

file_postfix = datetime.now().strftime("%Y%m%d")

dag = DAG(
    dag_id='etl_reddit_pipeline', 
    default_args=default_args, 
    schedule_interval='@daily', 
    catchup=False,
    tags=['reddit', 'etl', 'pipeline']
    )

#extraction from reddit #dag
extract = PythonOperator(
    task_id = 'reddit_extraction',
    python_callable=reddit_pipeline,
    op_kwargs={
        'file_name': f'reddit_{file_postfix}',
        'subreddit': 'dataengineering',
        'time_filter': 'day',
        'limit': 100
    },
    dag=dag
)

# Upload to S3 #dag
upload_s3 = PythonOperator(
    task_id = 's3_upload',
    python_callable=upload_s3_pipeline,
    dag=dag
)

extract >> upload_s3