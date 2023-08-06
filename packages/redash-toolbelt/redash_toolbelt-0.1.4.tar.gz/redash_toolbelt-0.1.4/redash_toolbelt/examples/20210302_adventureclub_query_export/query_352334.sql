/*
Name: Subscription Started QA
Data source: 30635
Created By: Jake Peterson
Last Update At: 2020-03-09T18:36:02.166Z
*/
/*
    nac_production.account_created
    nac_production.account_created_success
    nac_production.payment_failed
    nac_production.payment_refunded
    nac_production.subscription_cancelled
    nac_production.subscription_created_success
    nac_production.subscription_upgraded
*/

with seg as (
    select 
        id,
        received_at,
        email,
        plan_name,
        user_id,
        account_id,
        plan_id,
        plan_price,
        member_id
    from nac_production.subscription_started
    where received_at::date between '2020-03-01' and '2020-03-07'
), 

str as (
    select 
        start,
        current_period_start,
        id,
        plan_id,
        metadata_user_id,
        metadata_account_id
    from stripe.subscriptions
    where start::date between '2020-03-01' and '2020-03-07'
)

select
    count(distinct str.id) as stripe_subs_started,
    count(distinct seg.id) as seg_events
from str 
    left join seg on seg.account_id = metadata_account_id