/*
Name: Orders Created with Different Member Names per account
Data source: 30635
Created By: Jeremy Bueler
Last Update At: 2020-05-28T17:07:52.517Z
*/
with orders_created as (
    SELECT 
        COUNT(orders_created.id),
        orders_created.member_id,
        orders_created.user_id,
        orders_created.member_first_name
    FROM nac_production.order_created orders_created 
    GROUP BY orders_created.member_id, orders_created.member_first_name, orders_created.user_id
),
member_changes as (
    SELECT COUNT(member_id) as member_counts, member_id, user_id FROM orders_created GROUP BY member_id, user_id ORDER BY member_counts DESC
)

select member_changes.*, orders_created.member_first_name from member_changes LEFT JOIN orders_created on orders_created.member_id = member_changes.member_id where member_counts > 1 ORDER BY member_counts DESC, user_id DESC ;