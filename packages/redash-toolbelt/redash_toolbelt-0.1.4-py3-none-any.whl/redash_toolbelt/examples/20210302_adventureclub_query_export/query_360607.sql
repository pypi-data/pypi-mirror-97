/*
Name: Daily Subscription Metrics
Data source: 30635
Created By: Jake Peterson
Last Update At: 2020-03-23T21:00:14.331Z
*/
with 

payments as (
    select 
        i.id as invoice_id,
        il.plan_id,
        il.type,
        il.currency,
        il.period_start::date as period_start_date,
        il.period_end::date as period_end_date,
        i.subtotal as invoice_subtotal,
        i.total as invoice_total,
        il.amount as line_amount,
        il.subscription_id,
        i.date as invoice_time,
        i.customer_id,
        i.charge_id,
        c.status as charge_status,
        s.status as sub_status,
        s.metadata_user_id as user_id,
        s.metadata_account_id as account_id
    from stripe.invoices i 
        left join stripe.invoice_lines il on il.invoice_id = i.id 
        left join stripe.subscriptions s on s.id = il.subscription_id
        left join stripe.charges c on c.id = i.charge_id
            and c.status = 'succeeded'
    where il.period_start::date >= '2019-01-01'
        and i.paid = true 
        and il.plan_id = 'pathfinder'
),

subs as (
    select 
        subscription_id,
        min(period_start_date) as first_period_start_date,
        min(period_end_date) as first_period_end_date,
        max(period_start_date) as last_period_start_date
    from payments 
    group by 1 
),

nums as (
--generate a numbers table so we can generate a dates table in the next CTE
    select 
        p0.n 
        + p1.n*2 
        + p2.n * POWER(2,2) 
        + p3.n * POWER(2,3)
        + p4.n * POWER(2,4)
        + p5.n * POWER(2,5)
        + p6.n * POWER(2,6)
        + p7.n * POWER(2,7) 
        + p8.n * POWER(2,8) 
        as number
      FROM 
        (SELECT 0 as n UNION SELECT 1) p0,
        (SELECT 0 as n UNION SELECT 1) p1,
        (SELECT 0 as n UNION SELECT 1) p2,
        (SELECT 0 as n UNION SELECT 1) p3,
        (SELECT 0 as n UNION SELECT 1) p4,
        (SELECT 0 as n UNION SELECT 1) p5,
        (SELECT 0 as n UNION SELECT 1) p6,
        (SELECT 0 as n UNION SELECT 1) p7,
        (SELECT 0 as n UNION SELECT 1) p8
),

cal as (
--generate a dates table
    select (getdate()::date - nums.number::integer)::date as day
    from nums
    where day > '2020-01-01'

),

daily_matrix as (
--cross join subscription with days so we get one row per day that a subscription is active or recently churned
    select
        cal.day,
        subs.subscription_id,
        subs.first_period_start_date,
        subs.last_period_start_date,
        subs.first_period_end_date
    from cal
        cross join subs
    where cal.day >= subs.first_period_start_date --only add rows for subs starting on their first active day
),

daily_status as (
--join in payments to get status each day for each subscription
    select
        d.day,
        d.subscription_id,
        d.first_period_start_date,
        d.last_period_start_date,
        case when d.day <= d.first_period_end_date then true else false end as is_first_period,
        min(datediff(day, p.period_start_date, d.day)) as days_since_sub_start
    from daily_matrix d 
        left join payments p on p.period_start_date <= d.day
    group by 1,2,3,4,5
)
--group daily status of all subs so we have one row per day that counts how many subs are in important cohorts
select
    day,
    count(distinct subscription_id) as all_subs,
    count(distinct case when days_since_sub_start < 30 then subscription_id end) as active_subs,
    count(distinct case when days_since_sub_start < 30 and is_first_period then subscription_id end) as new_active_subs,
    count(distinct case when days_since_sub_start < 30 and not is_first_period then subscription_id end) as returning_active_subs,
    count(distinct case when days_since_sub_start > 30 then subscription_id end) as inactive_subs
from daily_status
group by 1 
order by 1 