/*
Name: West Coast Subs
Data source: 30635
Created By: Jeremy Bueler
Last Update At: 2020-09-15T06:57:43.420Z
*/
with stripe_subs as (
    SELECT subs.*,
    cards.address_state,
    customers.email
    FROM stripe.subscriptions subs
    LEFT JOIN 
        stripe.customers customers on subs.customer_id = customers.id
    LEFT JOIN 
        stripe.cards cards on customers.default_source = cards.id
    WHERE subs.status = 'active'
),

account_owners as  (
    SELECT 
        users.id as user_id,
        users.account_id,
        users.role_id,
        profiles.first_name,
        profiles.last_name,
        profiles.email,
        payment_customer.external_id stripe_customer_id
    FROM accounts_service.users users
    LEFT JOIN accounts_service.profiles profiles on profiles.user_id = users.id
    LEFT JOIN accounts_service.payment_customers payment_customer on payment_customer.account_id = users.account_id
    WHERE users.role_id = 3
),

addresses as (
    SELECT state, account_id from accounts_service.addresses a GROUP BY 1, 2
)



SELECT 
    id as stripe_subscription_id,
    status,
    address_state as billing_state,
    addresses.state as shipping_state,
    account_owners.email,
    account_owners.account_id,
    account_owners.first_name,
    account_owners.last_name,
    account_owners.user_id,
    account_owners.stripe_customer_id
FROM stripe_subs
LEFT JOIN account_owners ON account_owners.stripe_customer_id = stripe_subs.customer_id
LEFT JOIN addresses on addresses.account_id = account_owners.account_id
WHERE address_state in ('OR', 'CA', 'WA');