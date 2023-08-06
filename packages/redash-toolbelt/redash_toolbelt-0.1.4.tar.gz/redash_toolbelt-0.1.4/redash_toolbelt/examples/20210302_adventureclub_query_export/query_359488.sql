/*
Name: Orders by State
Data source: 30635
Created By: Jake Peterson
Last Update At: 2020-03-20T20:56:55.906Z
*/
--orders_service.orders has one row per order, no need to de-dupe 
with o as (
    select 
        id,
        user_id,
        account_id,
        json_extract_path_text(shipping_address, 'state', true) as state,
        json_extract_path_text(product, 'title', true) as product
    from orders_service.orders
    where convert_timezone('US/Pacific', created_at)::date between '{{ from_date }}' and '{{ to_date }}'
        and approved = true 
        and status <> 'cancelled'
),
pops as (
    select 'CA' as state, 39937489 as pop union all
    select 'TX' as state, 29472295 as pop union all
    select 'FL' as state, 21992985 as pop union all
    select 'NY' as state, 19440469 as pop union all
    select 'PA' as state, 12820878 as pop union all
    select 'IL' as state, 12659682 as pop union all
    select 'OH' as state, 11747694 as pop union all
    select 'GA' as state, 10736059 as pop union all
    select 'NC' as state, 10611862 as pop union all
    select 'MI' as state, 10045029 as pop union all
    select 'NJ' as state, 8936574 as pop union all
    select 'VA' as state, 8626207 as pop union all
    select 'WA' as state, 7797095 as pop union all
    select 'AZ' as state, 7378494 as pop union all
    select 'MA' as state, 6976597 as pop union all
    select 'TN' as state, 6897576 as pop union all
    select 'IN' as state, 6745354 as pop union all
    select 'MO' as state, 6169270 as pop union all
    select 'MD' as state, 6083116 as pop union all
    select 'WI' as state, 5851754 as pop union all
    select 'CO' as state, 5845526 as pop union all
    select 'MN' as state, 5700671 as pop union all
    select 'SC' as state, 5210095 as pop union all
    select 'AL' as state, 4908621 as pop union all
    select 'LA' as state, 4645184 as pop union all
    select 'KY' as state, 4499692 as pop union all
    select 'OR' as state, 4301089 as pop union all
    select 'OK' as state, 3954821 as pop union all
    select 'CT' as state, 3563077 as pop union all
    select 'UT' as state, 3282115 as pop union all
    select 'IA' as state, 3179849 as pop union all
    select 'NV' as state, 3139658 as pop union all
    select 'AR' as state, 3038999 as pop union all
    select 'PR' as state, 3032165 as pop union all
    select 'MS' as state, 2989260 as pop union all
    select 'KS' as state, 2910357 as pop union all
    select 'NM' as state, 2096640 as pop union all
    select 'NE' as state, 1952570 as pop union all
    select 'ID' as state, 1826156 as pop union all
    select 'WV' as state, 1778070 as pop union all
    select 'HI' as state, 1412687 as pop union all
    select 'NH' as state, 1371246 as pop union all
    select 'ME' as state, 1345790 as pop union all
    select 'MT' as state, 1086759 as pop union all
    select 'RI' as state, 1056161 as pop union all
    select 'DE' as state, 982895 as pop union all
    select 'SD' as state, 903027 as pop union all
    select 'ND' as state, 761723 as pop union all
    select 'AK' as state, 734002 as pop union all
    select 'DC' as state, 720687 as pop union all
    select 'VT' as state, 628061 as pop union all
    select 'WY' as state, 567025 as pop 
)

select 
    o.state,
    count(distinct id) as orders,
    1.00*count(distinct id)/(pops.pop/100000.00) as orders_per_100_thsnd_ppl,
    count(distinct user_id) as users,
    1.00*count(distinct id)/count(distinct user_id) as avg_orders_per_user,
    count(distinct account_id) as accounts,
    1.00*count(distinct account_id)/(pops.pop/100000.00) as accts_per_100_thsnd_ppl,
    1.00*count(distinct id)/count(distinct account_id) as avg_orders_per_account
from o 
    left join pops on pops.state = o.state
where lower(split_part(product, ' ', 1)) in ( {{brand}} )
    and o.state <> 'ZZ'
group by 1, pops.state, pops.pop
order by 2 desc 