/*
Name: Stripe Charges with customer_id filter
Data source: 41734
Created By: Jeremy Bueler
Last Update At: 2020-12-21T20:06:30.876Z
*/
with charges as (
    select * FROM query_571713
    where customer_id = '{{ stripe_customer_id }}'
)

select * FROM charges;