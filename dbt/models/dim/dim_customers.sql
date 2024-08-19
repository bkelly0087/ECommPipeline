WITH source AS (
    SELECT * FROM {{ source('ecommerce', 'customers') }}
)
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    address,
    created_at AS customer_created_at
FROM source