/*
Name: Unpaid Customers (as of Today)
Data source: 30635
Created By: Jake Peterson
Last Update At: 2020-03-23T20:17:34.198Z
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
        s.status as sub_status,
        s.metadata_user_id as user_id,
        s.metadata_account_id as account_id
    from stripe.invoices i 
        left join stripe.invoice_lines il on il.invoice_id = i.id 
        left join stripe.subscriptions s on s.id = il.subscription_id
    where il.period_start::date <= current_date
        and il.period_end::date >= current_date
)

select *
from payments 
where sub_status='unpaid'
