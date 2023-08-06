/*
Name: Subscription Summaries
Data source: 39530
Created By: Jeremy Bueler
Last Update At: 2021-01-20T18:56:56.423Z
*/
with accounts_with_valid_subs AS (
    SELECT 
        u.account_id
    FROM 
        "accounts-service".subscriptions s
    LEFT JOIN 
        "accounts-service".users u on u.id = s.user_id
    WHERE s.status in ('active','unpaid','trialing','past_due','paused')
    GROUP BY u.account_id
),

subs AS (
    SELECT 
        s.id,
        s.created_at as created_at,
        s.user_id,
        s.external_id,
        json_extract_path_text(s.plan, 'name', TRUE) AS plan,
        CAST(('0' || COALESCE(json_extract_path_text(s.plan, 'quantityLimitIntervalCount'), '0')) AS INTEGER) as quantityLimitIntervalCount,
        (CASE WHEN quantityLimitIntervalCount = 0 THEN 30 ELSE quantityLimitIntervalCount END) as quantity_limit_interval_count,
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
    WHERE u.account_id in (
        SELECT * FROM accounts_with_valid_subs
    )
    -- AND quantityLimitIntervalCount is not null
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
        count(o.id) as order_count_per_user,
        o.user_id 
    from "orders-service".orders o 
    where 
    o.created_at >= '2019-07-29'::Date
    and o.type in ('interval', 'final', 'replacement')
    -- and o.status in ('ordered', 'in_transit','active','out_for_delivery','delivered','delayed','recouped','fulfilled')
    and o.status not in ('returned','exchanged','exchange_started','exchange_pending','return_delayed','Returned','Cancelled ','tracer','cancelled','return_pending','user_cancelled','rejected')
    or o.status is null
    group by o.user_id
),

legacy_orders as (
    select 
        count(o.id) as order_count_per_user,
        o.user_id 
    from "orders-service".orders o 
    where 
    o.created_at < '2019-07-29'::Date
    and o.type in ('interval', 'final', 'replacement')
    -- and o.status in ('ordered', 'in_transit','active','out_for_delivery','delivered','delayed','recouped','fulfilled')
    and o.status not in ('returned','exchanged','exchange_started','exchange_pending','return_delayed','Returned','Cancelled ','tracer','cancelled','return_pending','user_cancelled','rejected')
    or o.status is null
    group by o.user_id
),

override_orders as (
    select 
        count(o.id) as order_count_per_user, o.user_id 
    from "orders-service".orders o 
    where o.type in ('override')
    and o.created_at >= '2019-07-29'::Date
    group by o.user_id
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

-- SELECT * FROM accounts_with_valid_subs

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
    newest_orders.created_at::timestamp as last_order_at,
    subs.monthly_cost,
    subs.quantity_limit_interval_count,
    (CASE WHEN subscription_changes.subscription_count_per_user IS NULL THEN 0 ELSE subscription_changes.subscription_count_per_user END) as subscription_count,
    (CASE WHEN subscription_orders.order_count_per_user IS NULL THEN 0 ELSE subscription_orders.order_count_per_user::integer END) as order_count,
    (CASE WHEN legacy_orders.order_count_per_user IS NULL THEN 0 ELSE legacy_orders.order_count_per_user::integer END) as legacy_order_count,
    (CASE WHEN override_orders.order_count_per_user IS NULL THEN 0 ELSE override_orders.order_count_per_user::integer END) as override_order_count,
    ROUND(subs.cost_per_interval) * order_count as expected_amount_paid
    -- (order_count * billed_per_pair) as accrued_order_total

FROM subs

LEFT JOIN account_owners on subs.account_id = account_owners.account_id 
LEFT JOIN subscription_changes on subscription_changes.user_id = subs.user_id
LEFT JOIN subscription_orders on subscription_orders.user_id = subs.user_id
LEFT JOIN legacy_orders on legacy_orders.user_id = subs.user_id
LEFT JOIN override_orders on override_orders.user_id = subs.user_id
LEFT JOIN newest_orders on newest_orders.user_id = subs.user_id
;

