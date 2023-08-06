/*
Name: Active subscribers by plan by cohort
Data source: 30635
Created By: Jeremy Bueler
Last Update At: 2020-08-20T22:17:26.509Z
*/
with 
    oldest_sub as (
        SELECT 
            convert_timezone('US/Pacific', subs.created_at)::date as created_at,
            subs.user_id,
            subs.plan
        FROM (
            SELECT user_id, MIN(created_at) as created_at FROM accounts_service.subscriptions GROUP BY user_id
        ) as first_subs
        INNER JOIN 
            accounts_service.subscriptions as subs
        ON
            subs.user_id = first_subs.user_id AND
            subs.created_at = first_subs.created_at
    ),
 
    newest_sub as (
        SELECT 
            subs.*
        FROM (
            SELECT user_id, MAX(created_at) as created_at FROM accounts_service.subscriptions GROUP BY user_id
        ) as last_subs
        INNER JOIN 
            accounts_service.subscriptions as subs
        ON
            subs.user_id = last_subs.user_id AND
            subs.created_at = last_subs.created_at
    )

SELECT 
    date_trunc('month', oldest_sub.created_at) as subscription_started_at,
    newest_sub.user_id,
    newest_sub.status,
    1 as count,
    json_extract_path_text(newest_sub.plan, 'name', TRUE) AS current_plan_name
FROM 
    oldest_sub
INNER JOIN 
    newest_sub on newest_sub.user_id = oldest_sub.user_id
;