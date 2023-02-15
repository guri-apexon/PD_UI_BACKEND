import json
import logging
from datetime import datetime

import pytest
from app import config
from app.db.session import SessionLocal
from app.main import app
from app.models.pd_protocol_metadata import PD_Protocol_Metadata
from app.models.pd_protocol_qc_summary_data import PDProtocolQCSummaryData
from fastapi import status
from fastapi.testclient import TestClient
from app.utilities.pd_table_redaction import TableRedaction
from app.utilities.redact import redactor
from app import crud
import pandas as pd

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("user_id, protocol, aidocid, redact_flag, hide_table_json_flag, return_refreshed_table_html, comments",
                         [
                            #  ("1061485", "TAK-861-1001", "1fd2c7c3-394c-4ce3-9ed9-6ef0c92a836d", True, False, True, "Readacted HTML and does not contain properties"),
                            #  ("1061485", "TAK-861-1001", "1fd2c7c3-394c-4ce3-9ed9-6ef0c92a836d", True, True, True, "Readacted HTML and contains the properties"),
                            #  ("1061485", "TAK-861-1001", "1fd2c7c3-394c-4ce3-9ed9-6ef0c92a836d", False, True, True, "Unreadacted HTML and contains the properties"),
                            #  ("1061485", "TAK-861-1001", "1fd2c7c3-394c-4ce3-9ed9-6ef0c92a836d", False, False, True, "Unreadacted HTML and does not contain properties"),
                             # ("1061485", "TAK-861-1001", "1fd2c7c3-394c-4ce3-9ed9-6ef0c92a836d", )
                         ])
def test_table_redaction(new_token_on_headers, user_id, protocol, aidocid, redact_flag, hide_table_json_flag,
                         return_refreshed_table_html, comments):

    user_protocol = crud.pd_user_protocols.get_by_userid_protocol(db, user_id, protocol)
    original_redact_profile = user_protocol.redactProfile
    if redact_flag and original_redact_profile != 'profile_0':
        user_protocol.redactProfile = 'profile_0'
        db.add(user_protocol)
        db.commit()
        db.refresh(user_protocol)

    valid_profile_name, profile, profile_genre = redactor.get_current_redact_profile(current_db=db,
                                                                                     user_id=user_id,
                                                                                     protocol=protocol,
                                                                                     profile_name=None,
                                                                                     genre=config.GENRE_ENTITY_NAME)
    table_redaction = TableRedaction(redact_flag = redact_flag,
                                     hide_table_json_flag = hide_table_json_flag,
                                     return_refreshed_table_html = return_refreshed_table_html,
                                     redact_profile_entities = profile_genre)

    protocol_data = crud.pd_protocol_data.get(db, aidocid, user='normal')

    tables_list = [i for i in enumerate(json.loads(json.loads(protocol_data.iqvdataToc))['data']) if
                   i[1][2] == 'table']
    # soa_table_lists = json.loads(json.loads(protocol_data.iqvdataSoa))
    #
    # protocol_data_iqvdataToc = json.loads(json.loads(protocol_data.iqvdataToc))

    table_dictionaries = list()

    for table in tables_list:
        table_dictonary = table_redaction.redact_table(table[1][3])
        table_dictionaries.append(table_dictonary)

    if redact_flag:
        redact_flag_bool_list = [config.REDACT_PARAGRAPH_STR in table_dictonary.get('Table', '') for table_dictonary in
                                 table_dictionaries if table_dictonary and type(table_dictonary) == dict]
        assert any(redact_flag_bool_list)

    if not hide_table_json_flag:
        table_properties_bool_list = ['TableProperties' in table_dictonary for table_dictonary in table_dictionaries if
                                      table_dictonary and type(table_dictonary) == dict]

        attachment_properties_bool_list = list()
        for table_dictonary in table_dictionaries:
            if table_dictonary and type(table_dictonary) == dict:
                for key in table_dictonary:
                    if key.startswith('FootnoteText') and 'AttachmentListProperties' in table_dictonary:
                        attachment_properties_bool_list.append(True)
                    elif key.startswith('FootnoteText') and 'AttachmentListProperties' not in table_dictonary:
                        attachment_properties_bool_list.append(False)

        assert all(table_properties_bool_list) and all(attachment_properties_bool_list)

