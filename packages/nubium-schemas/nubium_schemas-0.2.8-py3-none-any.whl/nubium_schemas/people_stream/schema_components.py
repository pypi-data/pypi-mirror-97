address_schema = {
    "name": "address",
    "type": "record",
    "fields": [
        {"name": "country_name", "type": "string", "default": ""},
        {"name": "country_code", "type": "string", "default": ""},
        {"name": "address_street_1", "type": "string", "default": ""},
        {"name": "address_street_2", "type": "string", "default": ""},
        {"name": "address_street_3", "type": "string", "default": ""},
        {"name": "address_city", "type": "string", "default": ""},
        {"name": "address_state_province", "type": "string", "default": ""},
        {"name": "address_postal_code", "type": "string", "default": ""},
        {"name": "core_based_statistical_area", "type": "string", "default": ""},
        {"name": "combined_statistical_area", "type": "string", "default": ""}
    ]
}

job_schema = {
    "name": "job",
    "type": "record",
    "fields": [
        {"name": "company", "type": "string", "default": ""},
        {"name": "business_phone", "type": "string", "default": ""},
        {"name": "job_title", "type": "string", "default": ""},
        {"name": "department", "type": "string", "default": ""},
        {"name": "job_role", "type": "string", "default": ""},
        {"name": "job_level", "type": "string", "default": ""},
        {"name": "job_function", "type": "string", "default": ""},
        {"name": "industry", "type": "string", "default": ""},
        {"name": "annual_revenue", "type": "string", "default": ""},
        {"name": "company_size", "type": "string", "default": ""}
    ]
}

personal_facts_schema = {
    "name": "personal_facts",
    "type": "record",
    "fields": [
        {"name": "email_address", "type": "string"},
        {"name": "salutation", "type": "string", "default": ""},
        {"name": "first_name", "type": "string", "default": ""},
        {"name": "last_name", "type": "string", "default": ""},
        {"name": "mobile_phone", "type": "string", "default": ""},
        {"name": "language_preference", "type": "string", "default": ""},
        {"name": "address", "type": address_schema},
        {"name": "job", "type": job_schema}
    ]
}

mlsm_schema = {
    "name": "mlsm",
    "type": "record",
    "fields": [
        {"name": "lead_ranking", "type": "string", "default": ""},
        {"name": "lead_rating", "type": "string", "default": ""},
        {"name": "interest_level", "type": "string", "default": ""},
        {"name": "qualification_level", "type": "string", "default": ""},
        {"name": "all_scores", "type": "string", "default": ""}
    ]
}

lead_score_schema = {
    "name": "lead_score",
    "type": "record",
    "fields": [
        {"name": "mlsm", "type":  mlsm_schema}
    ]
}

marketing_descriptors_schema = {
    "name": "marketing_descriptors",
    "type": "record",
    "fields": [
        {"name": "persona", "type": "string", "default": ""},
        {"name": "super_region", "type": "string", "default": ""},
        {"name": "sub_region", "type": "string", "default": ""},
        {"name": "penalty_box_reason", "type": "string", "default": ""},
        {"name": "penalty_box_expiration", "type": "string", "default": ""},
        {"name": "lead_score", "type": lead_score_schema}
    ]
}

privacy_schema = {
    "name": "privacy",
    "type": "record",
    "fields": [
        {"name": "consent_email_marketing", "type": "string", "default": ""},
        {"name": "consent_email_marketing_timestamp", "type": "string", "default": ""},
        {"name": "consent_email_marketing_source", "type": "string", "default": ""},
        {"name": "consent_share_to_partner", "type": "string", "default": ""},
        {"name": "consent_share_to_partner_timestamp", "type": "string", "default": ""},
        {"name": "consent_share_to_partner_source", "type": "string", "default": ""},
        {"name": "consent_phone_marketing", "type": "string", "default": ""},
        {"name": "consent_phone_marketing_timestamp", "type": "string", "default": ""},
        {"name": "consent_phone_marketing_source", "type": "string", "default": ""}
    ]
}

opt_in_schema = {
    "name": "opt_in",
    "type": "record",
    "fields": [
        {"name": "f_formdata_optin", "type": "string", "default": ""},
        {"name": "f_formdata_optin_phone", "type": "string", "default": ""},
        {"name": "f_formdata_sharetopartner", "type": "string", "default": ""}
    ]
}

location_schema = {
    "name": "location",
    "type": "record",
    "fields": [
        {"name": "city_from_ip", "type": "string", "default": ""},
        {"name": "state_province_from_ip", "type": "string", "default": ""},
        {"name": "postal_code_from_ip", "type": "string", "default": ""},
        {"name": "country_from_ip", "type": "string", "default": ""},
        {"name": "country_from_dns", "type": "string", "default": ""}
    ]
}

last_submission_schema = {
    "name": "last_submission",
    "type": "record",
    "fields": [
        {"name": "submission_date", "type": "string", "default": ""},
        {"name": "submission_source", "type": "string", "default": ""},
        {"name": "opt_in", "type": opt_in_schema},
        {"name": "location", "type": location_schema}
    ]
}

sfdc_lead_id_schema = {
    "name": "sfdc_lead_id",
    "type": "record",
    "fields": [
        {"name": "lead_id", "type": "string", "default": ""},
        {"name": "record_status", "type": "string", "default": ""}
    ]
}

sfdc_contact_id_schema = {
    "name": "sfdc_contact_id",
    "type": "record",
    "fields": [
        {"name": "contact_id", "type": "string", "default": ""},
        {"name": "account_id", "type": "string", "default": ""},
        {"name": "record_status", "type": "string", "default": ""}
    ]
}

tracking_ids_schema = {
    "name": "tracking_ids",
    "type": "record",
    "fields": [
        {"name": "eloqua_contact_id", "type": "string", "default": ""},
        {"name": "sfdc_lead_ids", "type": {"type": "array", "items": sfdc_lead_id_schema, "default": []}},
        {"name": "sfdc_contact_ids", "type": {"type": "array", "items": sfdc_contact_id_schema, "default": []}},
    ]
}

tombstone_schema = {
    "name": "tombstone",
    "type": "record",
    "fields": [
        {"name": "is_tombstoned", "type": "string", "default": ""},
        {"name": "tombstone_timestamp", "type": "string", "default": ""},
        {"name": "tombstone_source", "type": "string", "default": ""},
        {"name": "delete_all_data", "type": "string", "default": ""}
    ]
}
