SELECT
    order_id,
    customer_id,
    order_date,
    status,
    total_amount
FROM {{ source('raw', 'orders') }}