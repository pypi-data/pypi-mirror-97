/*
Name: Account Summaries
Data source: 41734
Created By: Jeremy Bueler
Last Update At: 2021-01-26T19:56:53.855Z
*/
WITH subs_per_customer as (
    SELECT 
        SUM(subscription_count) as total_subscription_count,
        SUM(override_order_count) as total_override_count,
        SUM(order_count) as total_order_count,
        SUM(legacy_order_count) as total_legacy_order_count,
        SUM(expected_amount_paid) as expected_amount_paid,
        MAX(last_order_at) as last_ordered_at,
        MIN(subscribed_at) as first_joined_at,
        COUNT(DISTINCT user_id) as subscriber_count,
        stripe_customer_id, 
        account_id,
        email,
        'https://dashboard.nikeadventureclub.com/accounts/' || account_id AS dashboard_url
        
    FROM query_572350
    GROUP BY stripe_customer_id, account_id, email
),
charges as (
    SELECT 
        customer_id,
        (SUM(amount) / 100) as amount_paid,
        (SUM(amount_refunded) / 100) as refund_amount,
        MAX(created_at) as last_charged_at,
        MIN(created_at) as first_charged_at
    FROM
        query_571713
    WHERE
        status in ('succeeded', 'exported')
    GROUP BY customer_id
),
accounts_reviewed as (
    SELECT * FROM query_599229
),
customers_with_inactive_cards as (
    SELECT id FROM query_608630
),
excluded_customers as (
    SELECT email from query_612836
)

SELECT 
    *,
    ((amount_paid - expected_amount_paid) - refund_amount ) as estimated_remaining_refund,
    (
        CASE WHEN customers_with_inactive_cards.id IS NOT NULL THEN 'TRUE'
        END
    ) as has_inactive_card
FROM 
    subs_per_customer, charges

LEFT JOIN 
    accounts_reviewed on accounts_reviewed.stripe_customer_id = charges.customer_id

LEFT JOIN 
    customers_with_inactive_cards on customers_with_inactive_cards.id = charges.customer_id

WHERE 
    charges.customer_id = subs_per_customer.stripe_customer_id
    and estimated_remaining_refund > 20
    and subs_per_customer.email NOT IN (SELECT * FROM excluded_customers)
ORDER BY estimated_remaining_refund DESC
;
    