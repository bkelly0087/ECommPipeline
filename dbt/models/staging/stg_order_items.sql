SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    price,
    total
FROM {{ source('raw', 'order_items') }}