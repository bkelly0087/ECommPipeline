SELECT
    c.*,
    CASE 
        WHEN c.total_spent > 1000 THEN 'High Value'
        WHEN c.total_spent > 500 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment
FROM {{ ref('int_customer_orders') }} c