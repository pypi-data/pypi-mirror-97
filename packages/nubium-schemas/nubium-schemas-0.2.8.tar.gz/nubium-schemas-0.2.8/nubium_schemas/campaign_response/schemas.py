from .schema_components import campaign_response, tracking_ids, salesforce_campaign_member

canon = {
    "name": "Canon",
    "type": "record",
    "fields": [
        {"name": "campaign_response", "type": campaign_response},
        {"name": "tracking_ids", "type": tracking_ids},
        {"name": "raw_formdata", "type": {"type": "map", "values": "string"}, "default": "{}"}
     ]
}

campaign_members_create = {
    "name": "CampaignMembersCreate",
    "type": "record",
    "fields": [
        {"name": "campaign_members_to_create", "type": {"type": "array", "items": salesforce_campaign_member}},
        {"name": "campaign_response", "type": campaign_response},
        {"name": "tracking_ids", "type": tracking_ids}
    ]
}

campaign_members_update = {
    "name": "CampaignMembersUpdate",
    "type": "record",
    "fields": [
        {"name": "campaign_members_to_update", "type": {"type": "array", "items": salesforce_campaign_member}}
    ]
}
