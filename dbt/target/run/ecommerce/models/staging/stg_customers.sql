
  create or replace   view ecommerce_db.public.stg_customers
  
   as (
    SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone_number,
    address,
    created_at
FROM ecommerce_db.raw.customers
  );

