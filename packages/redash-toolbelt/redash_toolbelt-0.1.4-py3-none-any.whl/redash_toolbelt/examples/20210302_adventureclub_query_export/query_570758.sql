/*
Name: Orders  - by status after date
Data source: 39530
Created By: Jeremy Bueler
Last Update At: 2020-12-15T16:15:20.932Z
*/
-- SELECT status from "orders-service".orders GROUP BY status;

SELECT 
    -- orders.id,
    orders.order_number,
    orders.created_at,
    orders.status,
    orders.approved,
    orders.approved_at,
    orders.sent_to_fulfillment_at,
    orders.delivered_at,
    orders.type

FROM 
    "orders-service".orders orders

WHERE 
    created_at::DATE >= '{{ created_after }}'::DATE
    AND approved = 'true'
    -- AND sent_to_fulfillment_at is not null
    AND status in ({{ include_order_statuses }})

ORDER BY created_at DESC

;

