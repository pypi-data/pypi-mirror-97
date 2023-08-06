/*
Name: Prepaid Card Query
Data source: 30635
Created By: Jeremy Bueler
Last Update At: 2020-05-15T19:42:39.230Z
*/
SELECT * FROM stripe.cards WHERE stripe.cards.funding = 'prepaid' ORDER BY uuid_ts DESC;