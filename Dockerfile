FROM apache/airflow:2.6.3

USER root

# Install system dependencies if any
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python packages
RUN pip install --no-cache-dir faker snowflake-connector-python dbt-core dbt-snowflake

# At the end of your Dockerfile
COPY --chown=airflow:root ./dbt /opt/airflow/dbt