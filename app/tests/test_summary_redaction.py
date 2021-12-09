import pytest
from mock import patch
from app import config
from app.utilities.redaction.summary_redaction import SummaryRedaction


@pytest.mark.parametrize("summary, redacted_attributes, redact_flag, redacted_placeholder, redacted_text", [
    ([['protocol_number', 'TAK-861-1001', 'Protocol Number']], ["sponsor"], True, "~REDACTED~",
     [['protocol_number', 'TAK-861-1001', 'Protocol Number']]),

    ([['approval_date', '20210316', 'Approval Date']], ["approval_date"], True, "~REDACTED~",
     [['approval_date', '~REDACTED~', 'Approval Date']]),

    ([['protocol_title', 'A Randomized, Double-blind, Placebo-Controlled Study to Assess the Safety, Tolerability, '
                         'Pharmacokinetics, and Pharmacodynamics of Single and Multiple Doses of TAK-861 in '
                         'Healthy Adult and Elderly Subjects and Subjects With Narcolepsy Type 1',
       'Protocol Title']], ["sponsor"], True, "~REDACTED~",
     [['protocol_title', 'A Randomized, Double-blind, Placebo-Controlled Study to Assess the Safety, Tolerability, '
                         'Pharmacokinetics, and Pharmacodynamics of Single and Multiple Doses of ~REDACTED~ in Healthy '
                         'Adult and Elderly Subjects and Subjects With Narcolepsy Type 1', 'Protocol Title']]),

    ([['sponsor', 'redaction', 'Sponsor']], ["sponsor"], False, "~REDACTED~", [['sponsor', 'redaction', 'Sponsor']])
])
def test_summary_redaction(summary, redacted_attributes, redact_flag, redacted_placeholder, redacted_text):
    test_profile = {
        config.GENRE_ATTRIBUTE_ENTITY: ["protocol_title"],
        config.GENRE_ENTITY_NAME: ["Molecule"]
    }
    entities = {
        "ProtocolTitle": [{"standard_entity_name": "Molecule",
                           "subcategory": "Molecule",
                           "confidence": 100.0,
                           "text": "TAK-861",
                           "start_idx": 10,
                           "end_idx": 17}]
    }
    with patch("app.crud.pd_protocol_summary_entities.get_protocol_summary_entities") as mock_entities:
        mock_entities.return_value = entities
        result = SummaryRedaction(summary_data=summary,
                                  redacted_attributes=redacted_attributes,
                                  redact_flag=redact_flag,
                                  redacted_placeholder=redacted_placeholder,
                                  current_profile=test_profile,
                                  aidoc_id="XXXX").redact_summary_pipeline()
        assert result == redacted_text
