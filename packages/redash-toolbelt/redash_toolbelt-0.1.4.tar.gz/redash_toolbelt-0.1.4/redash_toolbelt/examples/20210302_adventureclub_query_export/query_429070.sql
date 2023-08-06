/*
Name: Orders By Month - Cohort by Plan name and Sub Start Date
Data source: 30635
Created By: Jeremy Bueler
Last Update At: 2020-08-20T22:23:59.391Z
*/
with orders as (SELECT 
    convert_timezone('US/Pacific', orders.created_at)::date AS order_create_date,
    orders.id,
    orders.shopify_order_number as order_number,
    orders.user_id,
    orders.account_id,
    orders.type,
    json_extract_path_text(orders.product, 'title', TRUE) AS product
FROM orders_service.orders orders
WHERE convert_timezone('US/Pacific', orders.created_at)::date BETWEEN '{{ from_date }}' AND '{{ to_date }}'
    AND orders.approved = TRUE
    AND orders.status <> 'cancelled'),

 member_vas as (
    SELECT mvi.order_id, mvi.vas_index, mvi.vas_item_id FROM orders_service.member_vas_items mvi WHERE mvi.order_id IN (
        SELECT orders.id FROM orders
    )
    GROUP BY 1, 2, 3
 ),
 
 oldest_sub as (
    SELECT 
        convert_timezone('US/Pacific', subs.created_at)::date as created_at,
        subs.user_id,
        subs.plan
    FROM (
        SELECT user_id, MIN(created_at) as created_at FROM accounts_service.subscriptions GROUP BY user_id
    ) as first_subs
    INNER JOIN 
        accounts_service.subscriptions as subs
    ON
        subs.user_id = first_subs.user_id AND
        subs.created_at = first_subs.created_at
 ),
 
 newest_sub as (
    SELECT 
        subs.*
    FROM (
        SELECT user_id, MAX(created_at) as created_at FROM accounts_service.subscriptions GROUP BY user_id
    ) as last_subs
    INNER JOIN 
        accounts_service.subscriptions as subs
    ON
        subs.user_id = last_subs.user_id AND
        subs.created_at = last_subs.created_at
 )


-- SELECT COUNT(orders.id) FROM orders

SELECT 
    date_trunc('month', orders.order_create_date) as order_month, 
    orders.id as order_id,
    count(distinct orders.id) as order_count,
    orders.product,
    orders.order_number,
    orders.type,
    newest_sub.status,
    date_trunc('month', oldest_sub.created_at) as subscription_started_at,
    -- json_extract_path_text(oldest_sub.plan, 'name', TRUE) AS original_plan_name,
    json_extract_path_text(newest_sub.plan, 'name', TRUE) AS current_plan_name
FROM
    orders
INNER JOIN
    oldest_sub
    ON
     oldest_sub.user_id = orders.user_id
INNER JOIN
    newest_sub
    ON
     newest_sub.user_id = orders.user_id
GROUP BY
    1, 2, 4, 5, 6, 7, 8, 9
ORDER BY order_month ASC
;