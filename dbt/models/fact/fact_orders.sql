WITH orders AS (
    SELECT * FROM {{ source('ecommerce', 'orders') }}
),
dim_dates AS (
    SELECT * FROM {{ ref('dim_dates') }}
)
SELECT
    o.order_id,
    o.customer_id,
    d.date_id,
    o.status,
    o.total_amount,
    o.order_date
FROM orders o
LEFT JOIN dim_dates d ON DATE(o.order_date) = d.date