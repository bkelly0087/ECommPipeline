SELECT
    product_id,
    name,
    category,
    price,
    description,
    created_at
FROM {{ source('raw', 'products') }}