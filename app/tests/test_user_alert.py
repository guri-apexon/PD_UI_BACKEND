import json
import logging
from datetime import datetime, timedelta

import pytest
from app.crud.pd_user_alert import pd_user_alert
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("test_setup_flg, user_id, protocol, adjust_alert_created_time, expected_num_alert, comments", [
    (True, "1012525", "Alert-Test", 0, 2, "Recent alert"),
    (True, "1012525", "Alert-Test", -120, 0, "Old alert"),
    (False, "XXX1034911", "SSR_J4_1002-043", 0, 0, "No alert")
])
def test_user_alert(new_token_on_headers, test_setup_flg, user_id, protocol, adjust_alert_created_time,
                    expected_num_alert, comments):
    logger.debug(f"test_user_alert: Testing for {comments}")
    current_timestamp = datetime.utcnow()

    # Manipulate the alert creation time
    if test_setup_flg:
        new_alert_created_time = current_timestamp + timedelta(days=adjust_alert_created_time)

        test_user_alerts = pd_user_alert.get_by_userid(db, user_id=user_id, alert_from_days=-3650)
        test_user_alert_list = [alert for alert in test_user_alerts if alert.protocol == protocol]

        if len(test_user_alert_list) == 0:
            assert False

        for test_user_alert in test_user_alert_list:
            test_user_alert.timeCreated = new_alert_created_time
            test_user_alert.timeUpdated = new_alert_created_time
            db.add(test_user_alert)
        db.commit()

    user_alerts = client.get("/api/user_alert/", params={"userId": user_id}, headers=new_token_on_headers)
    assert user_alerts.status_code == 200

    all_alerts = json.loads(user_alerts.content)
    interested_alert = [protocol for alert in all_alerts if alert.get('protocol') == protocol]
    assert len(interested_alert) == expected_num_alert

