/*
Name: Average Age per Plan ID
Data source: 30635
Created By: Jeremy Bueler
Last Update At: 2020-05-27T21:04:34.693Z
*/
with members as (
    SELECT
        profiles.dob,
        profiles.user_id,
        DATEDIFF(year, profiles.dob, '{{ current_date }}'::DATE) as age
    FROM accounts_service.users users
    LEFT JOIN accounts_service.profiles profiles ON profiles.user_id = users.id
    WHERE users.role_id = 4
),
subs as (
    SELECT * FROM accounts_service.subscriptions subscriptions where subscriptions.completed_at is null
)

SELECT subs.plan_id, AVG(members.age) as average_age FROM subs, members WHERE subs.user_id = members.user_id GROUP BY subs.plan_id;