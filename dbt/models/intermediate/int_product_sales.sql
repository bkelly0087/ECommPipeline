SELECT
    p.*,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.total) AS total_revenue
FROM {{ ref('stg_products') }} p
LEFT JOIN {{ ref('stg_order_items') }} oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.category, p.price, p.description, p.created_at