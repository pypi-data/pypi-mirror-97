/*
Name: Final Report - NAC Subs, Order Count, Amount Paid and Estimated Refund
Data source: 39530
Created By: Jeremy Bueler
Last Update At: 2020-12-11T21:06:52.486Z
*/
with subs AS (
    SELECT 
        s.id,
        s.created_at as created_at,
        s.user_id,
        s.external_id,
        json_extract_path_text(s.plan, 'name', TRUE) AS plan,
        json_extract_path_text(s.plan, 'quantityLimitIntervalCount', TRUE) AS quantityLimitIntervalCount,
        json_extract_path_text(s.plan, 'amount', TRUE) AS monthly_cost,
        ((monthly_cost / 30) * quantityLimitIntervalCount) as cost_per_interval,
        s.status,
        u.account_id,
        u.subscribed_at,
        s.final_order_at
    FROM (
        SELECT user_id, MAX(created_at) as created_at FROM "accounts-service".subscriptions GROUP BY user_id
    ) as latest_sub
    INNER JOIN 
        "accounts-service".subscriptions as s
    ON
        s.user_id = latest_sub.user_id AND
        s.created_at = latest_sub.created_at
    LEFT JOIN "accounts-service".users u on u.id = s.user_id
    WHERE s.status in ({{ statuses }})
        AND u.subscribed_at::Date >= '{{ subscription_start_after }}'::Date
),

account_owners AS (
    SELECT 
        subs.account_id,
        users.id as account_owner_id,
        profiles.email,
        pc.external_id as stripe_customer_id
    FROM
        subs
    LEFT JOIN
        "accounts-service".users on users.account_id = subs.account_id
    LEFT JOIN
        "accounts-service".profiles on users.id = profiles.user_id
    LEFT JOIN 
        "accounts-service".payment_customers pc on pc.account_id = subs.account_id
    WHERE
        users.account_id = subs.account_id
        AND users.role_id = 3
        AND profiles.user_id = users.id
    GROUP BY 1, 2, 3, 4
 ),

payment_customers as (
    SELECT * FROM "accounts-service".payment_customers pc where pc.account_id in (select account_id from subs)
),

subscription_changes as (
    select count(s.external_id) as subscription_count_per_user, s.user_id from "accounts-service".subscriptions s group by user_id order by subscription_count_per_user desc
),

subscription_orders as (
    select 
        count(o.id) as order_count_per_user, o.user_id 
    from "orders-service".orders o 
    where o.type in ('interval', 'final', 'replacement')
    and o.status not in ({{ excluded_order_status }})
    group by o.user_id
),

override_orders as (
    select 
        count(o.id) as order_count_per_user, o.user_id 
    from "orders-service".orders o 
    where o.type in ('override')
    group by o.user_id
),

refunds as (
    select r.customer_id, count(*) as count, sum(r.amount_refunded) as total_refunded from stripe_payments.refunds r where status = 'Refunded' group by r.customer_id
),

paid_invoices as (
    select count(*) as count, sum(i.amount_paid) * .01 as amount_paid, i.user_id  from "accounts-service".invoices i where i.status = 'paid' group by i.user_id
),

unpaid_invoices as (
    select count(*) as count, sum(i.amount_due) * .01 as amount_due, i.user_id  from "accounts-service".invoices i where i.amount_due > 0 group by i.user_id
),

newest_orders AS (
    SELECT 
        o.id as order_id,
        o.created_at as created_at,
        o.user_id
    FROM (
        SELECT user_id, MAX(created_at) as created_at FROM "orders-service".orders GROUP BY user_id
    ) as latest_order
    INNER JOIN 
        "orders-service".orders as o
    ON
        o.user_id = latest_order.user_id AND
        o.created_at = latest_order.created_at
    WHERE o.user_id IN (select user_id from subs)
)

-- SELECT COUNT(*) from subs

-- SELECT * FROM newest_orders

SELECT 
    account_owners.email,
    account_owners.stripe_customer_id,
    'https://dashboard.nikeadventureclub.com/accounts/' || subs.account_id || '/members/' || subs.user_id  AS dashboard_url,    
    subs.id as subscription_id,
    subs.account_id,
    subs.subscribed_at,
    'https://dashboard.stripe.com/subscriptions/' || subs.external_id AS stripe_subscription_url,
    subs.plan as current_plan,
    subs.user_id,
    subs.final_order_at,
    subs.status current_status,
    newest_orders.created_at as last_order_at,
    (CASE WHEN subscription_changes.subscription_count_per_user IS NULL THEN 0 ELSE subscription_changes.subscription_count_per_user END) as subscription_count,
    (CASE WHEN subscription_orders.order_count_per_user IS NULL THEN 0 ELSE subscription_orders.order_count_per_user::integer END) as order_count,
    (CASE WHEN override_orders.order_count_per_user IS NULL THEN 0 ELSE override_orders.order_count_per_user::integer END) as override_order_count,
    (CASE WHEN paid_invoices.count IS NULL THEN 0 ELSE paid_invoices.count::integer END) as paid_invoices,
    (CASE WHEN paid_invoices.amount_paid IS NULL THEN 0 ELSE paid_invoices.amount_paid END) as amount_paid,
    (CASE WHEN unpaid_invoices.count IS NULL THEN 0 ELSE unpaid_invoices.count END) as unpaid_invoices,
    (CASE WHEN unpaid_invoices.amount_due IS NULL THEN 0 ELSE unpaid_invoices.amount_due END) as amount_due,
    (CASE WHEN (COALESCE(amount_paid,0) - COALESCE(amount_due,0)) IS NULL THEN NULL ELSE (COALESCE(amount_paid,0) - COALESCE(amount_due,0)) END) as payment_difference,
    (CASE WHEN (amount_paid / NULLIF(order_count,0)) IS NULL THEN payment_difference ELSE (amount_paid / NULLIF(order_count,0)) END) as dollar_per_order,
    ROUND(subs.cost_per_interval) as billed_per_pair,
    (order_count * billed_per_pair) as accrued_order_total,
    refunds.total_refunded as refunds_already_recieved,
    ((amount_paid - accrued_order_total) - COALESCE(refunds_already_recieved::integer,0)) as estimated_refund
FROM subs

LEFT JOIN account_owners on subs.account_id = account_owners.account_id 
LEFT JOIN subscription_changes on subscription_changes.user_id = subs.user_id
LEFT JOIN subscription_orders on subscription_orders.user_id = subs.user_id
LEFT JOIN override_orders on override_orders.user_id = subs.user_id
LEFT JOIN paid_invoices on paid_invoices.user_id = subs.user_id
LEFT JOIN unpaid_invoices on unpaid_invoices.user_id = subs.user_id
LEFT JOIN newest_orders on newest_orders.user_id = subs.user_id
LEFT JOIN refunds on refunds.customer_id = account_owners.stripe_customer_id

-- WHERE account_owners.email = 'ckvictorian@yahoo.com'

ORDER BY 
    dollar_per_order DESC,
    order_count DESC
;