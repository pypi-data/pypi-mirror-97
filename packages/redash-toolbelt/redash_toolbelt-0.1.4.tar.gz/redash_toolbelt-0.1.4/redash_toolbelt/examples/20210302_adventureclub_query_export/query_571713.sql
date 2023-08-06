/*
Name: Stripe Charges
Data source: 39530
Created By: Jeremy Bueler
Last Update At: 2021-01-07T18:21:49.496Z
*/
with c as (SELECT
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
WHERE charges.status = 'succeeded'

UNION

SELECT 
	exported_charges.charge_id,
	exported_charges.created_at,
	TRUE as captured,
	exported_charges.invoice_id,
	'succeeded' as status,
	(exported_charges.paid_amount * 100) as amount,
	(exported_charges.refund_amount * 100) as amount_refunded,
	exported_charges.customer_id	
FROM 
	stripe_payments.charges exported_charges
	
WHERE exported_charges.charge_id NOT IN (
	SELECT
		id as charge_id
	FROM
		stripe.charges
))


SELECT * FROM c WHERE c.created_at::Date > '2019-07-29'::Date;