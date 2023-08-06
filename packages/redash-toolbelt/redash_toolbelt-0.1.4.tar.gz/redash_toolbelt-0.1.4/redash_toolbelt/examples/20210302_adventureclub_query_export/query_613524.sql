/*
Name: New Query
Data source: 41734
Created By: Jeremy Bueler
Last Update At: 2021-01-27T15:08:51.753Z
*/
SELECT 
    charge_id, 
    count(*) as dupe_row 
from 
    query_597566 
group by charge_id 
having dupe_row > 1 
order by dupe_row desc;
