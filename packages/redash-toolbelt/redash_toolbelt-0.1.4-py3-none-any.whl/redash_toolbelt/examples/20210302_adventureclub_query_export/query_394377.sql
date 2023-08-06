/*
Name: Account Owners
Data source: 39530
Created By: Jeremy Bueler
Last Update At: 2020-11-03T17:17:30.974Z
*/
-- ORIGINAL QUERY - OLD Redshift Cluster
-- with account_owners as 
--     (
--         SELECT 
--             users.id as user_id,
--             users.role_id,
--             profiles.first_name,
--             profiles.last_name,
--             profiles.email,
--             payment_customer.external_id stripe_customer_id
--         FROM accounts_service.users users
--         LEFT JOIN accounts_service.profiles profiles on profiles.user_id = users.id
--         LEFT JOIN accounts_service.payment_customers payment_customer on payment_customer.account_id = users.account_id
--     )
-- select * FROM account_owners where role_id = 3 ORDER BY user_id DESC;

with account_owners as 
    (
        SELECT 
            users.id as user_id,
            users.role_id,
            profiles.first_name,
            profiles.last_name,
            profiles.email,
            payment_customer.external_id stripe_customer_id
        FROM "accounts-service".users users
        LEFT JOIN "accounts-service".payment_customers payment_customer on payment_customer.account_id = users.account_id
        LEFT JOIN "accounts-service".profiles profiles on profiles.user_id = users.id
    )
select * FROM account_owners where role_id = 3 ORDER BY user_id DESC;