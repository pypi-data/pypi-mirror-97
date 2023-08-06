/*
Name: Monthly Subscription Metrics
Data source: 30635
Created By: Jake Peterson
Last Update At: 2020-03-23T23:00:38.309Z
*/
with 

payments as (
    select 
        i.id as invoice_id,
        il.plan_id,
        il.type,
        il.currency,
        date_trunc('month', il.period_start::date) as period_start_month,
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
    where il.period_start::date >= '2019-08-01'
        and i.paid = true 
        and il.plan_id = 'pathfinder'
),

subs as (
    select 
        subscription_id,
        min(period_start_month) as first_period_start_month,
        max(period_start_month) as last_period_start_month
    from payments 
    group by 1 
),

cal as (

    select period_start_month as mth
    from payments
    group by 1 

),

daily_matrix as (
--cross join subscription with days so we get one row per day that a subscription is active or recently churned
    select
        cal.mth,
        subs.subscription_id,
        case when cal.mth = subs.first_period_start_month then true else false end as is_first_period,
        subs.first_period_start_month,
        subs.last_period_start_month
    from cal
        cross join subs
    where cal.mth >= subs.first_period_start_month --only add rows for subs starting on their first active day
),

monthly_status as (

    select
        d.mth,
        d.subscription_id,
        d.is_first_period,
        d.first_period_start_month,
        d.last_period_start_month,
        min(datediff(month, d.first_period_start_month, d.mth)) as months_since_sub_start,
        min(datediff(month, p.period_start_month, d.mth)) as months_since_period_start
    from daily_matrix d 
        left join payments p 
            on p.period_start_month <= d.mth
    group by 1,2,3,4,5

)

select
    mth,
    count(distinct subscription_id) as all_subs,
    count(distinct case when months_since_period_start = 0 then subscription_id end) as active_subs,
    count(distinct case when months_since_period_start = 0 and is_first_period then subscription_id end) as new_active_subs,
    count(distinct case when months_since_period_start = 0 and not is_first_period then subscription_id end) as returning_active_subs,
    count(distinct case when months_since_period_start > 0 then subscription_id end) as inactive_subs
from monthly_status
group by 1 
order by 1 
