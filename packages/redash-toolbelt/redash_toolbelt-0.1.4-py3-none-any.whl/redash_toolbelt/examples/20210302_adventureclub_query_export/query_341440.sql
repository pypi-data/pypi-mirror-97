/*
Name: Tax Report
Data source: 30635
Created By: Jake Peterson
Last Update At: 2020-03-03T20:21:37.510Z
*/
select 
  ch.created as charged_at, 
  ch.amount/100.00 as amount,
  ch.amount_refunded/100.00 as amount_refunded,
  ca.address_city, 
  ca.address_zip, 
  ca.address_state, 
  cu.email, 
  ch.invoice_id, 
  ch.id as charge_id,
  ch.paid
from stripe.charges as ch 
  inner join stripe.cards as ca 
    on ch.card_id = ca.id
  inner join stripe.customers as cu 
    on cu.id = ch.customer_id
where ch.created::date between '{{ from_date }}' and '{{ to_date }}'
  and ch.paid = true
order by ch.created