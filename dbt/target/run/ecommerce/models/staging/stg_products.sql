
  create or replace   view ecommerce_db.public.stg_products
  
   as (
    SELECT
    product_id,
    name,
    category,
    price,
    description,
    created_at
FROM ecommerce_db.raw.products
  );

