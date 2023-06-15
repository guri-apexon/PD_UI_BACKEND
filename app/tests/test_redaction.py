import logging
import pytest
from app import config
from app.db.session import SessionLocal
from app.main import app
from app.utilities.redact import redactor
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")

# Init
sample_text = ": Efficacy and safety of GSK3196165 versus placebo and sarilumab in participants with moderately to severely active rheumatoid arthritis who have an inadequate response to biological DMARDs and/or Janus Kinase inhibitors. sarilumab(new compound) is beneficial"
sample_font_info = {'IsBold': False, 'font_size': -1, 'font_style': '', 'entity': [{'start_idx': 25, 'end_idx': 34, 'subcategory': 'Molecule', 'confidence': 75.0, 'text': 'GSK3196165', 'debug_redact_text': 'GSK3196165', 'debug_redact_text_match_flg': True}, {'start_idx': 55, 'end_idx': 63, 'subcategory': 'Molecule', 'confidence': 75.0, 'text': 'sarilumab', 'debug_redact_text': 'sarilumab', 'debug_redact_text_match_flg': True}, {'start_idx': 0, 'end_idx': 0, 'subcategory': 'Molecule', 'confidence': 75.0, 'text': 'sarilumab(new'}], 'Bold': False, 'Caps': False, 'ColorRGB': 0, 'DStrike': False, 'Emboss': False, 'Highlight': '', 'Imprint': False, 'Italics': False, 'Outline': False, 'rFonts': '', 'rStyle': '', 'Shadow': False, 'Size': -1, 'SmallCaps': False, 'Strike': False, 'Underline': '', 'Vanish': False, 'VertAlign': ''}
_, _, profile_1_entities = redactor.get_current_redact_profile(current_db=db, profile_name='primary', genre=config.GENRE_ENTITY_NAME)
_, _, profile_0_entities = redactor.get_current_redact_profile(current_db=db, profile_name='secondary', genre=config.GENRE_ENTITY_NAME)


@pytest.mark.parametrize("user_id, protocol, user_role, expected_redact_profile, comments", [
    ("1034911", "SSR_1002-043", "secondary", config.USERROLE_REDACTPROFILE_MAP.get("secondary", ""), "secondary user's redact profile"),
    ("1034911", "SSR_1002-043", "primary", config.USERROLE_REDACTPROFILE_MAP.get("primary", ""), "primary user's redact profile"),
    ("1034911", "SSR_1002-043", "SSRXXX", config.USERROLE_REDACTPROFILE_MAP.get(config.FOLLOW_DEFAULT_ROLE, ""), "Invalid userRole's redact profile")
])
def test_current_redact_profile_name(new_token_on_headers, user_id, protocol, user_role, expected_redact_profile, comments):
    """
    Verify correct redact profile identified
    """
    logger.debug(f"Testing for {comments}")
    # Set user-role 
    follow_response = client.post("/api/follow_protocol/", json={"userId": user_id,  "protocol": protocol,
                                                                 "follow": True,  "userRole": user_role},
                                  headers=new_token_on_headers)
    assert follow_response.status_code == 200

    # By userid and protocol
    profile_name, profile, profile_genre = redactor.get_current_redact_profile(current_db=db, user_id=user_id, protocol=protocol)
    assert profile_name == expected_redact_profile
    assert len(profile) >= 2
    logger.debug(f"profile_name: {profile_name}; profile: {profile}; profile_genre: {profile_genre}")

    # By profile name
    profile_name, profile, profile_genre = redactor.get_current_redact_profile(current_db=db, profile_name = expected_redact_profile)
    assert profile_name == expected_redact_profile
    assert len(profile) >= 2
    logger.debug(f"profile_name: {profile_name}; profile: {profile}; profile_genre: {profile_genre}")
