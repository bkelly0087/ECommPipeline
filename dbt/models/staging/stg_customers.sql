SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone_number,
    address,
    created_at
FROM {{ source('raw', 'customers') }}