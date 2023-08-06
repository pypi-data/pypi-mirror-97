/*
Name: Bulk Refund Report
Data source: 41734
Created By: Jeremy Bueler
Last Update At: 2021-01-27T23:13:27.408Z
*/
-- SUB QUERIES
with initial_refunds as (
    SELECT customer_id, refund_amount, SUM(refund_for_charge) as expected_refund_amount from cached_query_597566 GROUP BY customer_id, refund_amount
),
customers as (
    SELECT stripe_customer_id, email FROM cached_query_576443
),
successful_refunds as (
    SELECT customer_id, SUM(refund_for_charge) as amount_refunded FROM cached_query_613831 WHERE status = 'success' GROUP BY customer_id
),
failed_refunds as (
    SELECT customer_id, SUM(refund_for_charge) as amount_failed FROM cached_query_613831 WHERE status != 'success' GROUP BY customer_id
)

-- QUERY
SELECT 
    customers.*,
    initial_refunds.refund_amount as confirmed_refund_amount,
    initial_refunds.expected_refund_amount,
    successful_refunds.amount_refunded,
    failed_refunds.amount_failed
FROM customers
LEFT JOIN successful_refunds on successful_refunds.customer_id = customers.stripe_customer_id
LEFT JOIN failed_refunds on failed_refunds.customer_id = customers.stripe_customer_id
LEFT JOIN initial_refunds on initial_refunds.customer_id = customers.stripe_customer_id

WHERE confirmed_refund_amount is not null

-- END QUERY
;