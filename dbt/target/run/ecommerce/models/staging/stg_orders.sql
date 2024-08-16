
  create or replace   view ecommerce_db.public.stg_orders
  
   as (
    SELECT
    order_id,
    customer_id,
    order_date,
    status,
    total_amount
FROM ecommerce_db.raw.orders
  );

