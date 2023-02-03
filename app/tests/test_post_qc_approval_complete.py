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
                             json={'aidoc_id': '5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a', 'qcApprovedBy': 'ut_id4', 'parent_path': '//quintiles.net/enterprise/Services/protdigtest/pilot_iqvxml/5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a'}, headers = settings.MGMT_CRED_HEADERS)
    assert response.status_code == 200
