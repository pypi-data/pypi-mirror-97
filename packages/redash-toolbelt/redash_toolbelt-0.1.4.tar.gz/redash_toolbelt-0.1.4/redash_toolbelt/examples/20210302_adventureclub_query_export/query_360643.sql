/*
Name: Monthly MRR, Custs, Subs (by Subscription Start Date)
Data source: 30635
Created By: Jake Peterson
Last Update At: 2020-03-23T22:23:22.994Z
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
        c.amount as charge_amount,
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
        --and il.plan_id = 'pathfinder'
)

select 
    date_trunc('month', period_start_date)::date as month,
    sum(line_amount/100.00) as sum_invoice_line_amount,
    sum(charge_amount/100.00) as sum_charge_amount,
    sum(invoice_total/100.00) as sum_invoice_total,
    count(distinct customer_id) as active_customers,
    count(distinct subscription_id) as active_subscriptions,
    1.00*count(distinct subscription_id)/count(distinct customer_id) as subs_per_cust
from payments
where plan_id is not null
group by 1
order by 1