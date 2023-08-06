/*
Name: Missing Order Numbers
Data source: 30635
Created By: Nolan Miller
Last Update At: 2020-10-13T23:52:14.836Z
*/
-- -- select shopify_order_id from orders_service.orders where shopify_order_number is null;
--  -- select cast (id as varchar), cast (order_number as varchar) from easykicks_shopify_prod.orders  where id in (select shopify_order_id from orders_service.orders where shopify_order_number is null);
--  -- select count(*) from easykicks_shopify_prod.orders;
 
 
--  SELECT *
--   FROM orders_service.orders
--   WHERE shopify_order_number IS NULL;
 
 
-- -- select *, cast(id as varchar) as id_string, cast(order_number as varchar) as order_string from easykicks_shopify_prod.orders where id_string in (select shopify_order_id from orders_service.orders where shopify_order_number is null);
 
--  /** orders in Db with no order number **/ 
-- -- select shopify_order_id from orders_service.orders where shopify_order_number is null;

-- /** orders in shopify **/
-- -- select order_number from easykicks_shopify_prod.orders;

-- select * from easykicks_shopify_prod.orders where id = 5174619598;
-- select * from easykicks_shopify_prod.orders where contact_email = 'paul39011@gmail.com';


-- -- with missing_orders as (select shopify_order_id from orders_service.orders where shopify_order_number is null)
-- -- select *, cast(id as varchar) as id_string, cast(order_number as varchar) as order_string from easykicks_shopify_prod.orders where id_string in missing_orders;


-- -- select shopify_order_id from orders_service.orders
-- -- join easykicks_shopify_prod.orders on cast(easykicks_shopify_prod.orders.id as varchar) = orders_service.orders.shopify_order_id
-- -- where orders_service.orders.shopify_order_number is null;

-- /* This is the query that should work */
-- select easykicks_shopify_prod.orders.id, easykicks_shopify_prod.orders.order_number from easykicks_shopify_prod.orders
-- join orders_service.orders on easykicks_shopify_prod.orders.id = cast(orders_service.orders.shopify_order_id as bigint)
-- where orders_service.orders.shopify_order_number is null;


-- select order_number, created_at, id from easykicks_shopify_prod.orders order by created_at asc limit 20;


-- -- select count(*) from easykicks_shopify_prod.orders;

SELECT
	orders.id,
	orders.shopify_order_id,
	oe.number
FROM
	orders_service.orders orders
	LEFT JOIN easykicks_shopify_prod.orders_export_1 oe ON oe.id = orders.shopify_order_id
WHERE
	orders.shopify_order_number IS NULL;