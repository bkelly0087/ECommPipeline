SELECT
    o.order_id,
    o.customer_id,
    c.customer_segment,
    o.order_date,
    o.total_amount,
    p.product_id,
    p.name AS product_name,
    p.category AS product_category,
    oi.quantity,
    oi.price AS unit_price,
    oi.total AS item_total
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('customer_mart') }} c ON o.customer_id = c.customer_id
JOIN {{ ref('stg_order_items') }} oi ON o.order_id = oi.order_id
JOIN {{ ref('product_mart') }} p ON oi.product_id = p.product_id