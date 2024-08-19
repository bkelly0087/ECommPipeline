SELECT
    p.*,
    CASE 
        WHEN p.total_revenue > 10000 THEN 'High Performing'
        WHEN p.total_revenue > 5000 THEN 'Medium Performing'
        ELSE 'Low Performing'
    END AS product_performance
FROM {{ ref('int_product_sales') }} p