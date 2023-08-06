/*
Name: Orders by status and type
Data source: 39530
Created By: Jeremy Bueler
Last Update At: 2020-12-07T23:48:30.082Z
*/
SELECT 
    count(*), 
    orders.type, 
    orders.status
FROM "orders-service".orders
GROUP BY 2, 3
ORDER BY count DESC
;