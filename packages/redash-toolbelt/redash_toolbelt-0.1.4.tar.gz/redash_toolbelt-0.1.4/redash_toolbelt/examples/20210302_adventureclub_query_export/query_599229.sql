/*
Name: Accounts Reviewed
Data source: 39530
Created By: Jeremy Bueler
Last Update At: 2021-01-26T22:22:46.265Z
*/
SELECT 
stripe_customer_id,
confirmed_refund_amount
FROM stripe_payments.refunds_reviewed
GROUP BY 1, 2