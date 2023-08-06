/*
Name: Monthly Order Activity
Data source: 30635
Created By: Jake Peterson
Last Update At: 2020-07-08T19:47:17.665Z
*/
--orders_service.orders has one row per order, no need to de-dupe 
with o as (
    select
        convert_timezone('US/Pacific', created_at)::date as order_create_date,
        id,
        user_id,
        account_id,
        json_extract_path_text(shipping_address, 'state', true) as state,
        json_extract_path_text(product, 'title', true) as product
    from orders_service.orders
    where convert_timezone('US/Pacific', created_at)::date between '{{ from_date }}' and '{{ to_date }}'
        and approved = true 
        and status <> 'cancelled'
)

select 
    date_trunc('month', order_create_date) as order_month,
    count(distinct id) as orders,
    count(distinct user_id) as users,
    1.00*count(distinct id)/count(distinct user_id) as avg_orders_per_user,
    count(distinct account_id) as accounts,
    1.00*count(distinct id)/count(distinct account_id) as avg_orders_per_account
from o 
where lower(split_part(product, ' ', 1)) in ( {{brand}} )
--and order_create_date>'2020-01-01'
group by 1
order by 1 