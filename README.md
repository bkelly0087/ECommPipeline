# EcommPipeline

An e-commerce data pipeline project using Airflow, Snowflake, and Python.

## Project Structure

```
EcommPipeline/
├── data_generation/
│   ├── generate_data.py
│   └── generated_data/
├── data_pipeline/
│   └── upload_to_snowflake.py
├── dags/
│   └── ecommerce_pipeline.py
├── ecomm_pipeline_env/
├── .gitignore
└── README.md
```

## Setup

1. Create and activate the virtual environment:
   ```
   python -m venv ecomm_pipeline_env
   source ecomm_pipeline_env/bin/activate
   ```

2. Install dependencies:
   ```
   pip install apache-airflow snowflake-connector-python
   ```

3. Set up Snowflake connection in `~/Library/Application Support/snowflake/config.toml`

4. Initialize Airflow:
   ```
   airflow db init
   ```

## Usage

1. Generate data:
   ```
   python data_generation/generate_data.py
   ```

2. Start Airflow:
   ```
   airflow scheduler
   airflow webserver
   ```

3. Trigger the DAG:
   ```
   airflow dags trigger ecommerce_pipeline
   ```

## Features

- Generates timestamped e-commerce data (customers, products, orders, order items)
- Uploads latest data files to Snowflake
- Airflow DAG for orchestration
