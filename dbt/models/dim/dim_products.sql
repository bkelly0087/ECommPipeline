WITH source AS (
    SELECT * FROM {{ source('ecommerce', 'products') }}
)
SELECT
    product_id,
    name AS product_name,
    category,
    price,
    created_at AS product_created_at
FROM source