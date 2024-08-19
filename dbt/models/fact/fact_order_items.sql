WITH order_items AS (
    SELECT * FROM {{ source('ecommerce', 'order_items') }}
)
SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    price,
    total
FROM order_items