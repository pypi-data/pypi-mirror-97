/*
Name: Refund Results - with customer_id filter
Data source: 41734
Created By: Jeremy Bueler
Last Update At: 2021-01-28T21:39:09.846Z
*/
select * FROM cached_query_613831 where customer_id = '{{ stripe_customer_id }}'