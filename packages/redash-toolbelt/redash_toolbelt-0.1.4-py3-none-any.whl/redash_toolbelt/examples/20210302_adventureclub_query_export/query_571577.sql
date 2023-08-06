/*
Name: Members per Account
Data source: 39530
Created By: Jeremy Bueler
Last Update At: 2020-12-15T19:26:49.043Z
*/
WITH member_counts as (
    SELECT 
        account_id,
        COUNT(*) as member_count
    FROM "accounts-service".users
    WHERE role_id = 4
    GROUP BY account_id
),
account_owners as (
    SELECT 
        account_id,
        id as account_owner_id
    FROM "accounts-service".users
    WHERE role_id = 3
    GROUP BY account_id, account_owner_id
)


SELECT 
    account_owners.*,
    coalesce(member_counts.member_count, 0) as member_qty
FROM 
    account_owners 
LEFT JOIN 
    member_counts on member_counts.account_id = account_owners.account_id
ORDER BY member_qty DESC
;
