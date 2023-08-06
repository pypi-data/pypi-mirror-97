/*
Name: Klaviyo Contacts & Account Owners
Data source: 30635
Created By: Jeremy Bueler
Last Update At: 2020-06-04T22:04:28.336Z
*/
WITH contacts AS
  (SELECT * FROM klaviyo.contacts contacts),

accounts AS
  (
    SELECT * FROM accounts_service.accounts accounts, contacts
    WHERE accounts.referral_code = contacts.referralcode
  ),
 
account_owners as (
	SELECT 
		profiles.email,
	    accounts.klaviyo_id,
	    profiles.first_name,
	    profiles.last_name,
	    accounts.organization,
	    accounts.title,
	    profiles.phone as phone_number,
	    accounts.address,
	    accounts.address_2,
	    accounts.city,
	    accounts.state_region,
	    accounts.country,
	    accounts.zip_code,
	    accounts.latitude,
	    accounts.longitude,
	    accounts.source,
	    accounts.consent,
	    accounts.first_active,
	    accounts.last_active,
	    accounts.profile_created_on,
	    accounts.date_added,
	    accounts.last_open,
	    accounts.last_click,
	    accounts.timezone,
	    accounts.adventure,
	    accounts.external_id,
	    profiles.user_id,
	    accounts.initial_referring_domain,
	    accounts.initial_source,
	    accounts.last_referring_domain,
	    accounts.last_search_engine,
	    accounts.last_search_keyword,
	    accounts.last_source,
	    accounts.mailinglistsignup,
	    accounts.purchasefrequency,
	    accounts.referralcode,
	    accounts.referralother,
	    accounts.referralsource,
	    accounts.search_engine,
	    accounts.search_keyword,
	    accounts.segments,
	    accounts.unsubscribe,
	    accounts.utm_campaign_1,
	    accounts.utm_content,
	    accounts.utm_medium,
	    accounts.utm_source,
	    accounts.utm_term,
	    accounts.utm_campaign,
	    accounts.zip
	FROM accounts_service.users users
	INNER JOIN accounts on accounts.id = users.account_id
	LEFT JOIN accounts_service.profiles profiles ON profiles.user_id = users.id
	WHERE users.role_id = 3
)
SELECT * FROM account_owners;