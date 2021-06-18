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
(True, "1034911", "SSR_J4_1002-043", 0, 1, "Recent alert"),
(True, "1034911", "SSR_J4_1002-043", -46, 0, "Old alert"),
(False, "XXX1034911", "SSR_J4_1002-043", 0, 0, "No alert")
])
def test_user_alert(test_setup_flg, user_id, protocol, adjust_alert_created_time, expected_num_alert, comments):
    logger.debug(f"test_user_alert: Testing for {comments}")
    current_timestamp = datetime.utcnow()
    
    # Manipulate the alert creation time
    if test_setup_flg:
        new_alert_created_time = current_timestamp + timedelta(days = adjust_alert_created_time)

        test_user_alerts = pd_user_alert.get_by_userid(db, user_id = user_id)
        test_user_alert_list = [alert for alert in test_user_alerts if alert.protocol == protocol]

        if len(test_user_alert_list) == 0:
            assert False

        test_user_alert_list[0].timeCreated = new_alert_created_time
        test_user_alert_list[0].timeUpdated = new_alert_created_time
        db.add(test_user_alert_list[0])
        db.commit()

  
    user_alerts = client.get("/api/user_alert/", params={"userId": user_id})
    assert user_alerts.status_code == 200

    all_alerts = json.loads(user_alerts.content)
    assert len(all_alerts) == expected_num_alert

    # Revert back the alert creation time for next iteration
    if test_setup_flg:
        test_user_alert_list[0].timeCreated = current_timestamp
        test_user_alert_list[0].timeUpdated = current_timestamp
        db.add(test_user_alert_list[0])
        db.commit()
