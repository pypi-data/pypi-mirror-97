/*
Name: Subscription Summaries - with email filter
Data source: 41734
Created By: Jeremy Bueler
Last Update At: 2020-12-18T23:51:08.433Z
*/
WITH subs as (
    SELECT * 
    FROM query_572350
    WHERE email = '{{ email }}'
)

SELECT * FROM subs;