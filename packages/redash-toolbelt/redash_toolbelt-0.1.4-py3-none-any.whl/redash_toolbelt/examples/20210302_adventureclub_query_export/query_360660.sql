/*
Name: New Query
Data source: 30635
Created By: Jake Peterson
Last Update At: 2020-03-23T20:51:32.974Z
*/
with t as (
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
),
subs as (
    select 
        subscription_id, 
        plan_id,
        min(period_start_date) as first_start_date,
        sum(line_amount) as ltv
    from t 
    group by 1,2
)

select 
    first_start_date as subscription_started,
    plan_id as plan,
    count(1) as subscriptions,
    sum(ltv) as sum_ltv,
    avg(ltv) as avg_ltv
from subs
group by 1,2
order by 1,2