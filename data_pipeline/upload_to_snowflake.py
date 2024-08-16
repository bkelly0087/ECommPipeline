import snowflake.connector
import os
from dotenv import load_dotenv
import logging
import shutil
from datetime import datetime

load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_snowflake_connection():
    logger.info("Attempting to connect to Snowflake with the following details:")
    logger.info(f"Account: {os.environ.get('SNOWFLAKE_ACCOUNT')}")
    logger.info(f"User: {os.environ.get('SNOWFLAKE_USER')}")
    logger.info(f"Warehouse: {os.environ.get('SNOWFLAKE_WAREHOUSE')}")
    logger.info(f"Database: {os.environ.get('SNOWFLAKE_DATABASE')}")
    logger.info(f"Schema: {os.environ.get('SNOWFLAKE_SCHEMA')}")
    
    try:
        conn = snowflake.connector.connect(
            account=os.environ['SNOWFLAKE_ACCOUNT'],
            user=os.environ['SNOWFLAKE_USER'],
            password=os.environ['SNOWFLAKE_PASSWORD'],
            warehouse=os.environ['SNOWFLAKE_WAREHOUSE'],
            database=os.environ['SNOWFLAKE_DATABASE'],
            schema=os.environ['SNOWFLAKE_SCHEMA']
        )
        logger.info(f"Connected to Snowflake - Database: {os.environ['SNOWFLAKE_DATABASE']}, Schema: {os.environ['SNOWFLAKE_SCHEMA']}")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to Snowflake: {str(e)}")
        raise
    
def get_latest_file(file_prefix):
    data_dir = '/opt/airflow/data_generation/generated_data'
    files = [f for f in os.listdir(data_dir) if f.startswith(file_prefix) and f.endswith('.csv')]
    if not files:
        raise FileNotFoundError(f"No files found with prefix {file_prefix}")
    
    def safe_parse_date(filename):
        try:
            # Try to parse the full timestamp
            return datetime.strptime(filename.split('_')[-1].split('.')[0], "%Y%m%d_%H%M%S")
        except ValueError:
            try:
                # If that fails, try parsing just the date part
                return datetime.strptime(filename.split('_')[-1].split('.')[0], "%Y%m%d")
            except ValueError:
                # If all parsing fails, return a minimum date to sort it last
                return datetime.min

    latest_file = max(files, key=safe_parse_date)
    return os.path.join(data_dir, latest_file)

def move_file(file_path):
    processed_dir = 'data_generation/processed_data'
    os.makedirs(processed_dir, exist_ok=True)
    new_path = os.path.join(processed_dir, os.path.basename(file_path))
    shutil.move(file_path, new_path)
    logger.info(f"Moved {file_path} to {new_path}")
    
def upload_to_snowflake(file_path, table_name):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    
    try:        
        cursor.execute(f"SHOW TABLES LIKE'{table_name}'")
        if not cursor.fetchone():
            logger.error(f"Table {table_name} does not exist in schema {os.environ['SNOWFLAKE_SCHEMA']}")
            return False

        stage_name = f"{os.environ['SNOWFLAKE_DATABASE']}.{os.environ['SNOWFLAKE_SCHEMA']}.ecommerce_stage"
        cursor.execute(f"PUT file://{file_path} @{stage_name}")

        copy_query = f"""
        COPY INTO {os.environ['SNOWFLAKE_DATABASE']}.{os.environ['SNOWFLAKE_SCHEMA']}.{table_name}
        FROM @{stage_name}/{os.path.basename(file_path)}
        FILE_FORMAT = (
            TYPE = CSV 
            FIELD_DELIMITER = ',' 
            SKIP_HEADER = 1
            FIELD_OPTIONALLY_ENCLOSED_BY = '"'
        )
        """
        
        cursor.execute(copy_query)
        logger.info(f"Successfully uploaded {file_path} to {os.environ['SNOWFLAKE_DATABASE']}.{os.environ['SNOWFLAKE_SCHEMA']}.{table_name}")
        return True 
    except Exception as e:
        logger.error(f"Error uploading to Snowflake: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

def main():
    files = {
        'customers': 'customers',
        'products': 'products',
        'orders': 'orders',
        'order_items': 'order_items'
    }
    
    for file_prefix, table in files.items():
        try:
            latest_file = get_latest_file(file_prefix)
            if upload_to_snowflake(latest_file, table):
                move_file(latest_file)
            else:
                logger.error(f"Failed to upload {latest_file} to {table}")
        except FileNotFoundError as e:
            logger.error(str(e))
        except Exception as e:
            logger.error(f"Unexpected error processing {file_prefix}: {str(e)}")

if __name__ == "__main__":
    main()