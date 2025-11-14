from datetime import datetime, timedelta
import os
import sys
import glob
import shutil
from airflow import DAG
from airflow.operators.python import PythonOperator

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from etl.extract import extract_csv_data, extract_multiple_csvs
from etl.transform import transform_dataframe
from etl.load import load_to_database, validate_database_connection

# Default arguments for the DAG
default_args = {
    'owner': 'dataflowhub',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='ETL Pipeline for Data Flow Hub',
    schedule_interval=timedelta(hours=1),  # Run every hour
    catchup=False,
    tags=['etl', 'dataflowhub'],
)

# Define the data directory path
data_dir = os.path.join(project_root, 'data')

# Define the processed directory path
processed_dir = os.path.join(project_root, 'processed')

def extract_task():
    """Extract data from CSV files"""
    try:
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Extract data from all CSV files in the data directory
        dataframes = extract_multiple_csvs(data_dir)
        
        if dataframes is None or dataframes.empty:
            print("No data extracted from CSV files")
            return None
        
        print(f"Successfully extracted data from {len(dataframes)} CSV files")
        return dataframes
    except Exception as e:
        print(f"Error in extract task: {str(e)}")
        raise

def transform_task(**context):
    """Transform the extracted data"""
    try:
        # Get the dataframe from the previous task
        df = context['task_instance'].xcom_pull(task_ids='extract_data')
        
        if df is None or df.empty:
            print("No data to transform")
            return None
        
        # Transform the data
        transformed_df = transform_dataframe(df)
        
        print(f"Successfully transformed {len(transformed_df)} records")
        return transformed_df
        
    except Exception as e:
        print(f"Error in transform task: {str(e)}")
        raise

def load_task(**context):
    """Load the transformed data into the database"""
    try:
        # Get the transformed dataframe from the previous task
        df = context['task_instance'].xcom_pull(task_ids='transform_data')
        
        if df is None or df.empty:
            print("No data to load")
            return
        
        # Validate database connection
        if not validate_database_connection():
            raise Exception("Database connection validation failed")
        
        # Load data to database
        success = load_to_database(df, clear_existing=False)
        
        if success:
            print("Successfully loaded data into database")
        else:
            raise Exception("Failed to load data into database")
        
    except Exception as e:
        print(f"Error in load task: {str(e)}")
        raise

def move_to_processed_task():
    """Move CSV files from data directory to processed directory"""
    try:
        # Create processed directory if it doesn't exist
        os.makedirs(processed_dir, exist_ok=True)
        
        # Find all CSV files in data directory
        csv_pattern = os.path.join(data_dir, '*.csv')
        csv_files = glob.glob(csv_pattern)
        
        if not csv_files:
            print(f"No CSV files found in {data_dir}. Skipping move operation.")
            return
        
        print(f"Found {len(csv_files)} CSV file(s) to move")
        
        # Move each CSV file to processed directory
        moved_count = 0
        for csv_file in csv_files:
            filename = os.path.basename(csv_file)
            dest_path = os.path.join(processed_dir, filename)
            shutil.move(csv_file, dest_path)
            moved_count += 1
            print(f"Moved {filename} to {processed_dir}")
        
        print(f"Successfully moved {moved_count} CSV file(s) to {processed_dir}")
        
    except Exception as e:
        print(f"Error moving files to processed directory: {str(e)}")
        raise

# Define tasks
validate_db = PythonOperator(
    task_id='validate_database',
    python_callable=lambda: validate_database_connection(),
    dag=dag,
)

extract_data = PythonOperator(
    task_id='extract_data',
    python_callable=extract_task,
    dag=dag,
)

transform_data = PythonOperator(
    task_id='transform_data',
    python_callable=transform_task,
    dag=dag,
)

load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_task,
    dag=dag,
)

move_to_processed = PythonOperator(
    task_id='move_to_processed',
    python_callable=move_to_processed_task,
    dag=dag,
)

# Define task dependencies
validate_db >> extract_data >> transform_data >> load_data >> move_to_processed

