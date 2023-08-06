/*
Name: Cumulative Charges by Customer ID
Data source: 41734
Created By: Jeremy Bueler
Last Update At: 2021-01-07T19:58:10.131Z
*/
SELECT
    * 
FROM 
    query_597566 
WHERE 
    customer_id = '{{ customer_id }}'
;