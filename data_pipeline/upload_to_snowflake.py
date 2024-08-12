import snowflake.connector
import os
from dotenv import load_dotenv
import toml

load_dotenv()

def get_snowflake_config():
    config_path = os.path.expanduser('~/Library/Application Support/snowflake/config.toml')
    with open(config_path, 'r') as f:
        config = toml.load(f)
    return config['connections']['my_ecomm_conn']

def upload_to_snowflake(file_path, table_name):
    config = get_snowflake_config()
    conn = snowflake.connector.connect(**config)
    
    cursor = conn.cursor()
    try:
        cursor.execute(f"PUT file://{file_path} @ecommerce_stage")
        cursor.execute(f"COPY INTO {table_name} FROM @ecommerce_stage/{os.path.basename(file_path)} FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1)")
        print(f"Uploaded {file_path} to {table_name}")
    finally:
        cursor.close()
        conn.close()

def main():
    files = {
        'customers.csv': 'customers',
        'products.csv': 'products',
        'orders.csv': 'orders',
        'order_items.csv': 'order_items'
    }
    
    for file, table in files.items():
        upload_to_snowflake(file, table)

if __name__ == "__main__":
    main()