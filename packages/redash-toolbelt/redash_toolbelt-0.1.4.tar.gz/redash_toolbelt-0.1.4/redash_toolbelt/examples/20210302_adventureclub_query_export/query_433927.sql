/*
Name: Fulfillment times by month
Data source: 30635
Created By: Jeremy Bueler
Last Update At: 2020-07-30T15:40:09.136Z
*/
with orders as (
    SELECT 
        orders.id,
        orders.created_at,
        orders.approved_at,
        orders.delivered_at,
        orders.sent_to_fulfillment_at,
        EXTRACT(EPOCH from (orders.delivered_at -orders.created_at)) as total_time,
        EXTRACT(EPOCH from (orders.approved_at -orders.created_at)) as time_to_approve,
        EXTRACT(EPOCH from (orders.sent_to_fulfillment_at - orders.approved_at)) as time_to_ql,
        EXTRACT(EPOCH from (orders.delivered_at - orders.sent_to_fulfillment_at)) as time_to_fulfill
    FROM orders_service.orders orders
    WHERE orders.created_at::TIMESTAMP >= '{{ created_by }}'::DATE
    AND orders.approved_at is not null
    AND orders.delivered_at is not null
)

SELECT 
    date_trunc('month', orders.created_at) as order_month,
    count(distinct orders.id) as order_count,
    AVG((time_to_approve || ' second')::interval) as approval_time, 
    AVG((time_to_ql || ' second')::interval) as ql_time,
    AVG((time_to_fulfill || ' second')::interval) as ql_received_to_delivered,
    AVG((total_time || ' second')::interval) as created_to_delivered
FROM orders
GROUP BY 1
ORDER BY order_month ASC;