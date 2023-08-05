campaign_response = {
    "name": "CampaignResponse",
    "type": "record",
    "fields": [
        {"name": "email_address", "type": "string", "default": ""},
        {"name": "ext_tactic_id", "type": "string", "default": ""},
        {"name": "int_tactic_id", "type": "string", "default": ""},
        {"name": "offer_id", "type": "string", "default": ""},
        {"name": "offer_consumption_timestamp", "type": "string", "default": ""}
    ]
}

tracking_ids = {
    "name": "TrackingIds",
    "type": "record",
    "fields": [
        {"name": "eloqua_contacts_inquiries_id", "type": "string", "default": ""},
        {"name": "sfdc_contact_id", "type": "string", "default": ""},
        {"name": "sfdc_lead_id", "type": "string", "default": ""},
        {"name": "sfdc_ext_tactic_lead_id", "type": "string", "default": ""},
        {"name": "sfdc_int_tactic_lead_id", "type": "string", "default": ""},
        {"name": "sfdc_offer_lead_id", "type": "string", "default": ""},
        {"name": "sfdc_ext_tactic_contact_id", "type": "string", "default": ""},
        {"name": "sfdc_int_tactic_contact_id", "type": "string", "default": ""},
        {"name": "sfdc_offer_contact_id", "type": "string", "default": ""}
    ]
}

salesforce_campaign_member = {
    "name": "SalesforceCampaignMember",
    "type": "record",
    "fields": [
        {"name": "campaign_membership_id", "type": "string", "default": ""},
        {"name": "campaign_id", "type": "string", "default": ""},
        {"name": "related_campaign_id", "type": "string", "default": ""},
        {"name": "sfdc_contact_id", "type": "string", "default": ""},
        {"name": "sfdc_lead_id", "type": "string", "default": ""},
        {"name": "true_response_date", "type": "string", "default": ""},
        {"name": "status", "type": "string", "default": ""},
        {"name": "campaign_member_type", "type": "string", "default": ""}
    ]
}