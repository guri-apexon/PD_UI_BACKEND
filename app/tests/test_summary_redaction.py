import pytest
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
                         'Pharmacokinetics, and Pharmacodynamics of Single and Multiple Doses of TAK-861 in Healthy '
                         'Adult and Elderly Subjects and Subjects With Narcolepsy Type 1', 'Protocol Title']]),

    ([['sponsor', 'redaction', 'Sponsor']], ["sponsor"], False, "~REDACTED~", [['sponsor', 'redaction', 'Sponsor']])
])
def test_summary_redaction(summary, redacted_attributes, redact_flag, redacted_placeholder, redacted_text):
    result = SummaryRedaction(summary_data=summary,
                              redacted_attributes=redacted_attributes,
                              redact_flag=redact_flag,
                              redacted_placeholder=redacted_placeholder).redact_summary_pipeline()
    assert result == redacted_text
