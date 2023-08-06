/*
Name: Unpaid Invoices
Data source: 39530
Created By: Nolan Miller
Last Update At: 2020-12-08T17:18:19.415Z
*/
SELECT
	subscriptions.external_id as subscription_id,
	subscriptions.status AS subscription_status,
	invoices.external_id AS invoice_id,
	invoices.next_attempt_date,
	invoices.amount_due,
	invoices.failure_reason,
	invoices.status AS invoice_status
FROM
	"accounts-service"."invoices"
	JOIN "accounts-service"."subscriptions" ON invoices.subscription_id = subscriptions.id
WHERE
	next_attempt_date IS NOT NULL
AND invoices.status = 'open'
ORDER BY
	next_attempt_date ASC;