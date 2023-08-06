/*
Name: Order QA
Data source: 30635
Created By: Jake Peterson
Last Update At: 2020-03-02T19:06:33.166Z
*/
with seg as (
    select 
        convert_timezone('US/Pacific', received_at)::date as day, 
        count(distinct order_id) as order_ids, 
        count(distinct user_id) as uniques
    from nac_production.order_created
    where convert_timezone('US/Pacific', received_at)::date >= '2020-02-01' 
    group by 1
),
db as (
    select 
        convert_timezone('US/Pacific', created_at)::date as day,
        count(distinct account_id) as aids,
        count(distinct user_id) as uids,
        count(distinct id) as order_ids,
        count(distinct shopify_order_id) as shop_order_ids
    from orders_service.orders
    where convert_timezone('US/Pacific', created_at)::date >= '2020-02-01'
    group by 1 
), 
daily as (
    select 
        seg.day,
        seg.uniques as seg_uniques,
        db.aids as db_accounts,
        db.uids as db_users,
        seg.order_ids as seg_orders,
        db.order_ids as db_orders,
        db.shop_order_ids as db_s_orders
    from seg
        inner join db on db.day=seg.day
)
select 
    day,
    seg_orders,
    db_orders,
    1.00*(seg_orders-db_orders)/db_orders*1.00 as diff,
    round(100.00*(seg_orders-db_orders)/db_orders*1.00, 2)::varchar||'%' as diff_pretty
from daily 
order by 1