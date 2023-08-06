/*
Name: Active Subs (Stripe vs Accounts Service)
Data source: 30635
Created By: Jeremy Bueler
Last Update At: 2020-09-08T16:43:42.869Z
*/
WITH stripe_subs AS
  (SELECT id, status as stripe_status, metadata_account_id as adventure_club_account_id
   FROM stripe.subscriptions
   WHERE status = 'active' ),
     subscriptions AS
  (SELECT subs.external_id, subs.status as adventure_club_status
   FROM accounts_service.subscriptions subs
   WHERE subs.status = 'active' OR subs.status = 'unpaid' OR subs.status = 'past_due'OR subs.status = 'inactive' )
SELECT *
FROM stripe_subs
LEFT JOIN subscriptions ON subscriptions.external_id = stripe_subs.id
where stripe_status != adventure_club_status OR external_id is null;

