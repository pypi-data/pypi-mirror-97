from .schema_components import (personal_facts_schema,
                                marketing_descriptors_schema,
                                privacy_schema,
                                last_submission_schema,
                                sfdc_lead_id_schema,
                                sfdc_contact_id_schema,
                                tombstone_schema)

tracking_ids_schema = {
    "name": "tracking_ids",
    "type": "record",
    "fields": [
        {"name": "eloqua_contact_id", "type": "string", "default": ""},
        {"name": "sfdc_lead_ids", "type": {"type": "array", "items": sfdc_lead_id_schema, "default": []}},
        {"name": "sfdc_contact_ids", "type": {"type": "array", "items": sfdc_contact_id_schema, "default": []}},
    ]
}


person_schema = {
    "name": "person",
    "type": "record",
    "fields": [
        {"name": "personal_facts", "type": personal_facts_schema},
        {"name": "marketing_descriptors", "type": marketing_descriptors_schema},
        {"name": "privacy", "type": privacy_schema},
        {"name": "last_submission", "type": last_submission_schema},
        {"name": "tracking_ids", "type": tracking_ids_schema},
        {"name": "tombstone", "type": tombstone_schema},
        {"name": "last_evaluated_by_dwm", "type": "string", "default": ""}
    ]
}
