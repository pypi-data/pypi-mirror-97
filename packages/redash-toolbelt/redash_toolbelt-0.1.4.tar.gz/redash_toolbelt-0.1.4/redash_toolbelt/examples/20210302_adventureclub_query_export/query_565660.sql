/*
Name: Final Order Statistics
Data source: 39530
Created By: Jeremy Bueler
Last Update At: 2020-12-07T19:23:54.562Z
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
)

SELECT count(*), 'total_subs'as category FROM subs

UNION

SELECT 
    count(*), 'final_orders_placed' as category
FROM subs WHERE final_order_at is not null

UNION

SELECT count(*), 'final_orders_remaining'as category FROM subs where final_order_at is null

ORDER BY count DESC
;
