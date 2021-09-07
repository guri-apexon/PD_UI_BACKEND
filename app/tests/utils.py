import json
import logging

from app.main import app
from app.utilities.config import settings
from fastapi import status
from fastapi.testclient import TestClient

client = TestClient(app)
logger = logging.getLogger(settings.LOGGER_NAME)

def get_token():
    token_header = dict()
    header_str = {'Content-Type': 'application/x-www-form-urlencoded'}
    data_str = f'grant_type=&username={settings.UNIT_TEST_CRED[0]}&password={settings.UNIT_TEST_CRED[1]}'
    response_token = client.post("/api/token/form_data", headers = header_str, data=data_str)
    logger.debug(f"Generated new token for test headers")
    try:
        if response_token.status_code == status.HTTP_200_OK:
            response_token_dict = json.loads(response_token.text)
            token_header = {'Authorization': f'Bearer {response_token_dict.get("access_token")}'}
    except Exception as exc:
        logger.warning(f"test utils: get_token() exception: {str(exc)}")

    return token_header
