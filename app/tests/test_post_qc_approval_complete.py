from app.main import app
import requests
from fastapi.testclient import TestClient
from app.utilities.config import settings

client = TestClient(app)


def test_management_health():
    response = requests.get(settings.MANAGEMENT_SERVICE_HEALTH_URL)
    assert response.status_code == 200
    assert response.text == "F5-UP"


def test_post_qc_complete_management_url():
    response = requests.post(settings.MANAGEMENT_SERVICE_URL + "pd_qc_check_update",
                             json={'aidoc_id': 'c8278f9e-abf2-464c-a1b3-9ea674d22d8f', 'qcApprovedBy': 'ut_id4', 'parent_path': '//quintiles.net/enterprise/Services/protdigtest/pilot_iqvxml/c8278f9e-abf2-464c-a1b3-9ea674d22d8f'}, headers = settings.MGMT_CRED_HEADERS)
    assert response.status_code == 200
