/*
Name: Member Data
Data source: 30635
Created By: Jeremy Bueler
Last Update At: 2020-05-19T22:43:03.169Z
*/
SELECT users.account_id,
       users.id AS member_id,
       subscriptions.external_id as subscription_id,
       account_owners.id as user_id,
       profiles.email
FROM accounts_service.users users
INNER JOIN accounts_service.users account_owners on account_owners.account_id = users.account_id AND account_owners.role_id = 3
LEFT JOIN accounts_service.subscriptions subscriptions on subscriptions.user_id = users.id AND subscriptions.deleted_at IS NULL
LEFT JOIN accounts_service.profiles profiles on profiles.user_id = account_owners.id
WHERE users.role_id = 4
ORDER BY account_owners.id DESC;