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

@pytest.mark.parametrize("expected_profiles", [
    (set(config.USERROLE_REDACTPROFILE_MAP.values()))
])
def test_get_all_redact_profile_names(expected_profiles):
    """
    Verify all configured profiles extracted
    """
    all_profiles = redactor.get_profiles()
    assert expected_profiles == set(all_profiles.keys())
    logger.debug(f"all_profiles: {all_profiles}")


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


@pytest.mark.parametrize("redact_profile, genre, max_genre_count, comments", [
    (config.USERROLE_REDACTPROFILE_MAP.get("primary", ""), config.GENRE_ENTITY_NAME, 0 ,"primary user's redact profile for genre entity"),
    (config.USERROLE_REDACTPROFILE_MAP.get("primary", ""), config.GENRE_ATTRIBUTE_NAME, 0 ,"primary user's redact profile for genre attribute"),
    (config.USERROLE_REDACTPROFILE_MAP.get("primary", ""), config.GENRE_ACTION_NAME, 0 ,"primary user's redact profile for genre action"),
    (config.USERROLE_REDACTPROFILE_MAP.get("primary", ""), config.GENRE_SECTION_NAME, 0 ,"primary user's redact profile for genre section"),
    (config.USERROLE_REDACTPROFILE_MAP.get("secondary", ""), config.GENRE_ENTITY_NAME, 60 ,"secondary user's redact profile for genre entity"),
    (config.USERROLE_REDACTPROFILE_MAP.get("secondary", ""), config.GENRE_ATTRIBUTE_NAME, 60 ,"secondary user's redact profile for genre attribute"),
    (config.USERROLE_REDACTPROFILE_MAP.get("secondary", ""), config.GENRE_ACTION_NAME, 2 ,"secondary user's redact profile for genre action"),
    (config.USERROLE_REDACTPROFILE_MAP.get("secondary", ""), config.GENRE_SECTION_NAME, 3 ,"secondary user's redact profile for genre section")
])
def test_current_redact_genre(redact_profile, genre, max_genre_count, comments):
    """
    Verify correct genre details extracted based on profile
    """
    logger.debug(f"Testing for {comments}")

    # Validate redact genre
    profile_name, profile, profile_genre = redactor.get_current_redact_profile(current_db=db, profile_name=redact_profile, genre=genre)
    assert profile_name == redact_profile
    assert len(profile_genre) <= max_genre_count
    assert len(profile.get(genre)) <= max_genre_count
    logger.debug(f"profile_name: {profile_name}; profile_genre: {profile_genre}")
