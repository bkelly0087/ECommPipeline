-- Create database
CREATE DATABASE IF NOT EXISTS ecommerce_db;

-- Use the newly created database
USE DATABASE ecommerce_db;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS mart;

-- Create raw tables
CREATE OR REPLACE TABLE raw.customers (
    customer_id STRING,
    first_name STRING,
    last_name STRING,
    email STRING,
    phone_number STRING,
    address STRING,
    created_at TIMESTAMP_NTZ
);

CREATE OR REPLACE TABLE raw.products (
    product_id STRING,
    name STRING,
    category STRING,
    price FLOAT,
    description STRING,
    created_at TIMESTAMP_NTZ
);

CREATE OR REPLACE TABLE raw.orders (
    order_id STRING,
    customer_id STRING,
    order_date TIMESTAMP_NTZ,
    status STRING,
    total_amount FLOAT
);

CREATE OR REPLACE TABLE raw.order_items (
    order_item_id STRING,
    order_id STRING,
    product_id STRING,
    quantity INTEGER,
    price FLOAT,
    total FLOAT
);

-- Create file formats for CSV ingestion
CREATE OR REPLACE FILE FORMAT csv_format
    TYPE = CSV
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null')
    EMPTY_FIELD_AS_NULL = TRUE;

-- Create stages for data loading
CREATE OR REPLACE STAGE ecommerce_stage
    FILE_FORMAT = csv_format;

-- Grant necessary permissions (adjust as needed)
GRANT USAGE ON DATABASE ecommerce_db TO ROLE ACCOUNTADMIN;
GRANT USAGE ON SCHEMA raw TO ROLE ACCOUNTADMIN;
GRANT ALL ON ALL TABLES IN SCHEMA raw TO ROLE ACCOUNTADMIN;
GRANT USAGE ON STAGE ecommerce_stage TO ROLE ACCOUNTADMIN;