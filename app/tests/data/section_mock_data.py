# Section data is the Mock of get_section_data API endpoint
section_data = [
    {
        "content": "area under the plasma concentration-time curve from time 0 to the 12-hour time point",
        "font_info": {
            "roi_id": {
                "para": "ae61a162-cf74-4b5d-8a3a-5e9180461a0f",
                "childbox": "61746dba-8c45-4c18-9714-652c49b134e3",
                "subtext": "9be2fbf6-8d53-4e5b-9f9e-cc1731433af3"
            },
            "doc_id": "4c7ea27b-8a6b-4bf0-a8ed-2c1e49bbdc8c",
            "id": "11848360-a7cc-443b-b465-69c0afc4794f",
            "link_id": "46bac1b7-9197-11ed-b507-005056ab6469",
            "parent_id": "9be2fbf6-8d53-4e5b-9f9e-cc1731433af3"
        },
        "level_1_CPT_section": "Unmapped",
        "file_section": "ABBREVIATIONS",
        "line_id": "ae61a162-cf74-4b5d-8a3a-5e9180461a0f61746dba-8c45-4c18-9714-652c49b134e39be2fbf6-8d53-4e5b-9f9e-cc1731433af3",
        "aidocid": "4c7ea27b-8a6b-4bf0-a8ed-2c1e49bbdc8c",
    }, ]

# Enriched data is the mock of enriched API endpoint
enriched_data = [
  {
    "doc_id": "4c7ea27b-8a6b-4bf0-a8ed-2c1e49bbdc8c",
    "link_id": "46bac1b7-9197-11ed-b507-005056ab6469",
    "parent_id": "ae61a162-cf74-4b5d-8a3a-5e9180461a0f",
    "text": "plasma",
    "preferred_term": "plasma1",
    "ontology": "MedDRA",
    "synonyms": "hemoglobin,vital fluid",
    "medical_term": "",
    "classification": "plasma_class1"
  }]

# Expected values after append the clinical terms into section data
clinical_values = {
      "plasma": {
        "preferred_term": "plasma1",
        "ontology": "MedDRA",
        "synonyms": "hemoglobin,vital fluid",
        "medical_term": "",
        "classification": "plasma_class1"
      }
    }

# added for configuration api data
configuration_api_data = [
    
    ("5c784c05-fbd3-4786-b0e4-3afa0d1c61ac", "1", "", "1034911",
     "SSRUT_GEN_001","","", 200, "doc id and without link id"),
    ("1698be28-1cf3-466e-8f56-5fc920029056", "1", "", "1036048",
     "FEED_TEST4","","", 200, "doc id changes"),
    ("21552918-f506-43d8-8879-4fe532631ba7", "", "8f8e70a7-cb76-4257-b595-80a2564a8aa2", "Dig2_Batch_Tester",
     "BI.Obesity.91af1307-5fc5-40cd-9671-b82771a42b2f","","", 200, "doc id and link id present"),
    ("00d9456f-b5d3-4045-b76f-3bdecbe99775","","","1150903","005", "clinical_terms,time_points,preferred_terms,redaction_attributes,references,properties", "" ,200,"all configration variables"),
    ("00d9456f-b5d3-4045-b76f-3bdecbe99775","","","1150903","005",
     "clinical_terms,time_points,preferred_terms,redaction_attributes,references","Protocol H9X-MC-GBGJ (a)",200,"all configration variables with section text"),
    ("00d9456f-b5d3-4045-b76f-3bdecbe99775","","a1b79393-a1b7-11ed-b15c-005056ab6469","1150903","005",
     "clinical_terms,preferred_terms,redaction_attributes,references,properties,time_points","",200,"all configration variables with link id"),
    ("00d9456f-b5d3-4045-b76f-3bdecbe99775","","a1b79393-a1b7-11ed-b15c-005056ab6469","1150903","005",
     "clinical_terms,preferred_terms,redaction_attributes,references,properties,time_points","test",200,"all configration variables with link id"),
    ("5c784c05-fbd3-4786-b0e4", "1", "", "1034911",
     "SSRUT_GEN_001","","", 404, "This document is not available in our database"),
    ("00d9456f-b5d3-4045-b76f-3bdecbe99775", "1", "", "1034911",
     "SSRUT_GEN_001","clinical_terms,preferred_terms,redaction_attributes,references,properties","", 200, "NO_TIME_POINT_DATA"),
    ("00d9456f-b5d3-4045-b76f-3bdecbe99775", "1", "", "1034911",
     "SSRUT_GEN_001","clinical_terms,preferred_terms,redaction_attributes,time_points,properties","", 200, "NO_REFERENCE_DATA"),

]