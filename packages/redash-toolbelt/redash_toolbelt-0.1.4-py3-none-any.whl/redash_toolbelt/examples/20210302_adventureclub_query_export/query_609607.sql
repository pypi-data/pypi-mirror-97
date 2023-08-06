/*
Name: Validate Refund Charges
Data source: 41734
Created By: Jeremy Bueler
Last Update At: 2021-01-21T21:14:15.219Z
*/
with customer_expected_refunds as (
    SELECT customer_id, refund_amount, SUM(refund_for_charge) as total_expected_refund FROM query_597566 GROUP BY customer_id, refund_amount
)
SELECT * FROM customer_expected_refunds where refund_amount != total_expected_refund;