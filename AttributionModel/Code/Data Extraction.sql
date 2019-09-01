with step_1 as (select distinct ts_hour || anonymous_id || coalesce(referrer_url, '') || coalesce(url, '') as uniques,
                                anonymous_id,
                                user_id,
                                ts,
                                url,
                                path,
                                referrer_domain,
                                utm_campaign,
                                utm_content,
                                utm_medium,
                                utm_source,
                                user_agent
                from periscope_views.pages
                where ts > current_date - interval '2 years'
),
     step_2 as (
         select *,
                row_number()
                over (partition by anonymous_id,user_id order by ts) as rank
         from step_1
         where url not similar to '%portal%'
     )
select uniques,
       anonymous_id,
       user_id,
       ts,
       url,
       path,
       referrer_domain,
       utm_campaign,
       utm_content,
       utm_medium,
       utm_source,
       user_agent,
       rank,
       case when path in ('/za/signup/v1/step/businessDetails/','/za/signup/v1/step/BusinessDetails','/za/signup/v1/step/','/create-account/v1',
                         '/za/signup/v1/','/za/signup/v1/ec/') then 'lead'
                when path similar to '%continue%'
                 or path in ('/za/signup/v1/step/userDetails/','/za/signup/v1/step/userDetails','/za/v2/','/za/signup/v2/','/sign-up/cart','/za/signup/v1/step/consumerAgreement/',
                            '/za/signup/v1/step/shopHardware/','/za/signup/v1/step/secureCheckout/','/za/signup/v1/retail/','/checkout/creditCard','/sign-up/consumer-agreement',
                            '/za/signup/v1/step/retailSerial/') then 'opportunity'
                when path in ('/za/signup/v1/step/complete/','/complete','/signup/v1/step/complete','/checkout/') then 'complete' else 'Session' end as state
from step_2





