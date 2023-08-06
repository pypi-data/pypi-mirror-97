/*
Name: Cumulative Charges
Data source: 41734
Created By: Jeremy Bueler
Last Update At: 2021-01-27T01:38:47.353Z
*/
with customers as (
    SELECT 
        stripe_customer_id, 
        estimated_remaining_refund,
        (CASE WHEN confirmed_refund_amount is null THEN estimated_remaining_refund ELSE confirmed_refund_amount END) as refund_amount 
    from query_576443
),

stripe_charges as (
    SELECT 
        * 
    FROM 
        (SELECT 
            customer_id,
            charge_id,
            created_at,
            (amount / 100) as paid_amount , SUM((amount / 100)) OVER (PARTITION BY customer_id ORDER BY created_at DESC) as cum_charges
        FROM query_609647
        WHERE customer_id is not null
        )
    ORDER BY customer_id DESC
),

charges as (
    SELECT customer_id,
    created_at,
    charge_id,
    cum_charges,
    paid_amount as amount,
    LAG(cum_charges,1,0) OVER (
        PARTITION BY customer_id
        ORDER BY created_at DESC
    ) previous_cumulative_charge
    FROM stripe_charges
)


-- SELECT stripe_customer_id, count(*) as dupe_customers FROM customers group by stripe_customer_id having dupe_customers > 1

SELECT 
    customers.refund_amount,
    charges.*,
    (refund_amount - previous_cumulative_charge) as remaining_refund_amount,
    ( CASE
    
        WHEN (refund_amount - previous_cumulative_charge) > 0 AND (refund_amount - previous_cumulative_charge) >= amount THEN amount
        WHEN (refund_amount - previous_cumulative_charge) > 0 AND (refund_amount - previous_cumulative_charge) < amount THEN (refund_amount - previous_cumulative_charge)
        ELSE
            0
        END
        
    ) as refund_for_charge
    
FROM customers
LEFT JOIN charges on customers.stripe_customer_id = charges.customer_id
WHERE 
    -- charges.customer_id = 'cus_FsYbc0FiKCMaMw'
    -- AND 
    refund_for_charge > 0
ORDER BY customer_id, refund_amount, created_at DESC

;