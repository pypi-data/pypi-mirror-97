/*
Name: UPDATED - Gifts Purchased - Date Range
Data source: 39530
Created By: Nolan Miller
Last Update At: 2020-11-11T19:16:00.213Z
*/
WITH gifts AS
  (SELECT gifts.id,
          profiles.first_name,
          profiles.last_name,
          profiles.email,
          accounts.type AS purchase_account_type,
          gifts.redeemed_at,
          gifts.updated_at,
          gifts.amount / 100 AS amount,
          gifts.desired_delivery_date,
          gifts.payment_id,
          gifts.created_at,
          gifts.recipient_account_id
   FROM "accounts-service"."gifts" gifts
   LEFT JOIN "accounts-service"."users" users ON gifts.account_id = users.account_id
   AND users.role_id = 3
   LEFT JOIN "accounts-service"."profiles" profiles ON profiles.user_id = users.id
   LEFT JOIN "accounts-service"."accounts" accounts ON accounts.id = gifts.account_id
   WHERE gifts.created_at::date BETWEEN '{{ gift_created.start }}' AND '{{ gift_created.end }}'
     AND gifts.cancelled_at IS NULL),

recipients AS
  (SELECT gifts.id AS gift_id,
          gifts.recipient_account_id,
          recipient_users.role_id,
          profiles.first_name,
          profiles.last_name,
          profiles.email
   FROM gifts
   LEFT JOIN "accounts-service"."users" recipient_users ON recipient_users.account_id = gifts.recipient_account_id
   AND recipient_users.role_id = 3
   LEFT JOIN "accounts-service"."profiles" profiles ON profiles.user_id = recipient_users.id)

SELECT 
    gifts.id,
    gifts.first_name as sender_first_name,
    gifts.last_name as sender_last_name,
    gifts.email as sender_email,
    gifts.amount as gift_amount,
    gifts.desired_delivery_date,
    gifts.redeemed_at,
    gifts.created_at,
    recipients.first_name as recipient_first_name,
    recipients.last_name as recipient_last_name,
    recipients.email as recipient_email,
    gift_created.received_at as email_sent_at
FROM gifts
LEFT JOIN recipients ON recipients.gift_id = gifts.id
LEFT JOIN nac_production.gift_created gift_created ON gifts.id = gift_created.gift_id;
