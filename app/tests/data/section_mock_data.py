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
