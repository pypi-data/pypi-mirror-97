/*
Name: stripe payments by customer
Data source: 39530
Created By: Jeremy Bueler
Last Update At: 2020-12-16T16:08:21.049Z
*/
WITH stripe_payments as (
    SELECT
    	id as charge_id,
    	created as created_at,
    	captured,
    	invoice_id,
    	status,
    	amount,
    	amount_refunded,
    	customer_id
    FROM
    	stripe.charges charges
    WHERE charges.customer_id is not null
    
    UNION
    
    SELECT 
    	exported_charges.charge_id,
    	exported_charges.created_at,
    	'true' as captured,
    	exported_charges.invoice_id,
    	'exported' as status,
    	(exported_charges.paid_amount * 100) as amount,
    	(exported_charges.refunded_amount * 100) as amount_refunded,
    	exported_charges.customer_id	
    FROM 
    	stripe_payments.charges exported_charges
    	
    WHERE exported_charges.charge_id NOT IN (
    	SELECT
    		id as charge_id
    	FROM
    		stripe.charges
    )
)

-- SELECT * FROM stripe_payments

SELECT 
	customer_id,
	pc.account_id as account_id,
	'https://dashboard.nikeadventureclub.com/accounts/' || pc.account_id AS dashboard_url,
	SUM(amount) / 100 as amount_paid, 
	SUM(amount_refunded) / 100 as refunded_amount,
	(amount_paid - refunded_amount) as net_amount_paid,
	MIN(stripe_payments.created_at) as first_payment_at,
	MAX(stripe_payments.created_at) as last_payment_at,
	'x' as control

FROM stripe_payments

LEFT JOIN
	"accounts-service".payment_customers pc ON pc.external_id = customer_id

WHERE
    captured = 'true'
	
GROUP BY 
	customer_id,
	account_id,
	dashboard_url

ORDER BY net_amount_paid DESC

;