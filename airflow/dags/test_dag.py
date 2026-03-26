from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import psycopg2
import requests


def test_env():
    required_vars = [
        "POSTGRES_USER",
        "POSTGRES_DB", 
        "OPENSEARCH_HOST",
        "OLLAMA_HOST"
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        raise ValueError(f"❌ Missing environment variables: {missing}")
    
    print("✅ All environment variables are set") 


def test_postgres():
    print("🔍 Testing PostgreSQL connection...")

    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="postgres",
        port=5432
    )

    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    result = cursor.fetchone()

    print("✅ Connected to Postgres:", result)

    cursor.close()
    conn.close()


def test_opensearch():
    print("🔍 Testing OpenSearch connection...")

    host = os.getenv("OPENSEARCH_HOST")

    response = requests.get(f"{host}")

    if response.status_code == 200:
        print("✅ OpenSearch is reachable")
        print("Cluster Info:", response.json())
    else:
        raise Exception("❌ OpenSearch connection failed")


def test_file_system():
    print("🔍 Testing file system...")

    path = "/opt/airflow/logs/test_file.txt"

    with open(path, "w") as f:
        f.write("Airflow FS test successful")

    print(f"✅ File written to {path}")


default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}


with DAG(
    dag_id="infrastructure_test_pipeline",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["test", "infra"],
) as dag:

    env_task = PythonOperator(
        task_id="test_env",
        python_callable=test_env
    )

    postgres_task = PythonOperator(
        task_id="test_postgres",
        python_callable=test_postgres
    )

    opensearch_task = PythonOperator(
        task_id="test_opensearch",
        python_callable=test_opensearch
    )

    fs_task = PythonOperator(
        task_id="test_file_system",
        python_callable=test_file_system
    )

    # Execution order
    env_task >> postgres_task >> opensearch_task >> fs_task



