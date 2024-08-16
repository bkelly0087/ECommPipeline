
  create or replace   view ecommerce_db.public.stg_order_items
  
   as (
    SELECT
    order_item_id,
    order_id,
    product_id,
    quantity,
    price,
    total
FROM ecommerce_db.raw.order_items
  );

