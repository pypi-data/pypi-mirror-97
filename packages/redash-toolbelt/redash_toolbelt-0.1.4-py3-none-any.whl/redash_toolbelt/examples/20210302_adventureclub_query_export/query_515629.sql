/*
Name: UPDATED - Subscriptions without recent orders
Data source: 39530
Created By: Nolan Miller
Last Update At: 2020-11-11T19:15:22.207Z
*/
WITH subs AS (
    SELECT 
    subscriptions.id,
    users.account_id,
    subscriptions.user_id,
    subscriptions.external_id as stripe_subscription_id,
    json_extract_path_text(subscriptions.plan, 'name', TRUE) AS plan,
    'https://dashboard.nikeadventureclub.com/accounts/' || users.account_id AS dashboard_url
   FROM "accounts-service"."subscriptions" subscriptions
   LEFT JOIN "accounts-service"."users" users on subscriptions.user_id = users.id
   WHERE status in ({{ statuses }})
),

orders AS (
    SELECT orders.user_id,
          orders.created_at
   FROM "orders-service"."orders" orders
   WHERE orders.created_at > CURRENT_DATE - interval '{{ Number of days }} days' 
),
   
newest_order AS (
    SELECT 
        o.id as order_id,
        o.created_at as created_at,
        o.user_id
    FROM (
        SELECT user_id, MAX(created_at) as created_at FROM orders_service.orders GROUP BY user_id
    ) as latest_order
    INNER JOIN 
        "orders-service"."orders" as o
    ON
        o.user_id = latest_order.user_id AND
        o.created_at = latest_order.created_at
    WHERE o.user_id IN (select user_id from subs)
 ),
 
 unused_subs AS (
    SELECT 
        subs.*,
        newest_order.order_id as most_recent_order_id,
        newest_order.created_at as most_recent_order_date
    FROM subs
    LEFT JOIN newest_order on subs.user_id = newest_order.user_id
    WHERE subs.user_id NOT IN
        (SELECT user_id
         FROM orders)
    ORDER BY most_recent_order_date ASC
 ),
 
 account_owners AS (
    SELECT 
        unused_subs.account_id,
        users.id as account_owner_id,
        profiles.email
    FROM
        unused_subs
    LEFT JOIN
        accounts_service.users on users.account_id = unused_subs.account_id
    LEFT JOIN
        accounts_service.profiles on users.id = profiles.user_id
    WHERE
        users.account_id = unused_subs.account_id
        AND users.role_id = 3
        AND profiles.user_id = users.id
    GROUP BY 1, 2, 3
 )
 
SELECT 
    unused_subs.account_id,
    unused_subs.user_id,
    unused_subs.stripe_subscription_id,
    unused_subs.plan,
    unused_subs.dashboard_url,
    unused_subs.most_recent_order_date,
    account_owners.email,
    count(invoices.id) as number_of_invoices_since_last_order,
    sum(invoices.amount_paid) * .01 as amount_paid_since_last_order
FROM 
    unused_subs
JOIN
    account_owners on unused_subs.account_id = account_owners.account_id
LEFT JOIN 
    "accounts-service"."invoices" invoices on unused_subs.id = invoices.subscription_id where invoices.created_at > unused_subs.most_recent_order_date
GROUP BY 1, 2, 3, 4, 5, 6, 7
ORDER BY amount_paid_since_last_order DESC
;