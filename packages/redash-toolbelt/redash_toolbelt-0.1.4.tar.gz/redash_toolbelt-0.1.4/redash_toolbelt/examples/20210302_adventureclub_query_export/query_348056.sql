/*
Name: Order Attribution QA
Data source: 30635
Created By: Jake Peterson
Last Update At: 2020-03-09T15:52:16.562Z
*/
with 

custs as (
    select 
        user_id, 
        min(received_at) as first_order_at
    from nac_production.order_created
    group by 1
),

first_id as (
    select 
        anonymous_id, 
        min(received_at) as first_id_at
    from nac_production.identifies 
    where anonymous_id is not null
    group by anonymous_id
),

id_map as (
    select 
        i.anonymous_id, 
        i.user_id
    from nac_production.identifies i
        inner join first_id 
            on first_id.anonymous_id = i.anonymous_id
            and first_id.first_id_at = i.received_at
    where i.anonymous_id is not null
        and i.user_id is not null
    group by 1,2
)

select 
    count(distinct custs.user_id) as unique_customers, 
    count(distinct id_map.user_id) as unique_customers_with_identify,
    count(distinct p.anonymous_id) as unique_visitors_linked_to_customers
from custs 
    left join id_map 
        on id_map.user_id = custs.user_id
    left join nac_production.pages p 
        on p.anonymous_id = id_map.anonymous_id
        and p.received_at < custs.first_order_at