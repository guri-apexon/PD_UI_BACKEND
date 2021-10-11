import pytest
from app.utilities.redaction.footnotes_redaction import RedactFootNotes


@pytest.mark.parametrize("attachments, redact_flag, redacted_placeholder, redacted_text, redact_profile_entities", [
    ([{'Text': 'Administrative Procedures Informed consent X',
       'Key': '',
       'entities': []
       }], True, "REDACT_VAR",
     {'FootnoteText_0': 'Administrative Procedures Informed consent X'}, list()),

    ([{'Text': 'of the assessments (eg. C-SSRS, alcohol, and drug screen) can be done at check-in time.',
       'Key': '1.',
       'entities': [{'start_idx': 32, 'end_idx': 38, 'standard_entity_name': 'Molecule', 'subcategory': 'Molecule',
                     'confidence': 75.0, 'text': 'alcohol'}]
       }], True, "REDACT_VAR",
     {'FootnoteText_0': '1. of the assessments (eg. C-SSRS, REDACT_VAR, and drug screen) can be done at check-in time.'}, ['Molecule']),

    ([{'Text': 'of the assessments (eg. C-SSRS, alcohol, and drug screen) can be done at check-in time.',
       'Key': '',
       'entities': [{'start_idx': 32, 'end_idx': 38, 'standard_entity_name': 'Molecule', 'subcategory': 'Molecule',
                     'confidence': 75.0, 'text': 'alcohol'}]
       }], False, "REDACT_VAR",
     {'FootnoteText_0': 'of the assessments (eg. C-SSRS, alcohol, and drug screen) can be done at check-in time.'}, ['Molecule']),

    ([], True, "REDACT_VAR", {}, list())
])
def test_footnotes_redaction(attachments, redact_flag, redacted_placeholder, redacted_text, redact_profile_entities):
    result = RedactFootNotes(attachments=attachments,
                             redact_flag=redact_flag,
                             redacted_placeholder=redacted_placeholder,
                             redact_profile_entities = redact_profile_entities).redact_footnotes_pipeline()
    assert result == redacted_text
