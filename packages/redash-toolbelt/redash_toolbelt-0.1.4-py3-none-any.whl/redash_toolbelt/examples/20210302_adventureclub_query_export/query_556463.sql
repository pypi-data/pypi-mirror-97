/*
Name: Account Owner emails for subs created between dates
Data source: 39530
Created By: Jeremy Bueler
Last Update At: 2020-12-01T19:55:26.487Z
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
        u.subscribed_at
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
        AND u.subscribed_at::date BETWEEN '{{ subscription_started.start }}' AND '{{ subscription_started.end }}'
),

account_owners AS (
    SELECT 
        subs.account_id,
        users.id as account_owner_id,
        profiles.email,
        pc.external_id as stripe_customer_id,
        profiles.first_name,
        profiles.last_name
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
    GROUP BY 1, 2, 3, 4, 5, 6
 )
 
 SELECT 
    account_owners.account_id,
    account_owners.account_owner_id as user_id,
    account_owners.email, 
    account_owners.first_name, 
    account_owners.last_name
    
FROM 
    account_owners 

GROUP BY 1, 2, 3, 4, 5;