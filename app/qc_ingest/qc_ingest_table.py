from .model import *
import uuid
import json
from .document import *
from .db_utils import *
import logging
from app.utilities.config import settings


logger = logging.getLogger(settings.LOGGER_NAME)

table_dict = TableType.table_dict

link_level_dict = Linklevel.link_level_dict


def get_roi_ids_dict(value):
    """getting roi ids dict"""
    try:
        roi_id_dict = {'text': [], 'table': [], 'subtext': []}
        datacell_roi_id = value['roi_id']['datacell_roi_id']
        roi_id = get_ids_from_parent_id(datacell_roi_id, 'table')
        (roi_id_dict['table']).append(datacell_roi_id)
        (roi_id_dict['table']).append(roi_id)
        (roi_id_dict['text']).append(roi_id)
        roi_id1 = get_ids_from_parent_id(roi_id, 'subtext')
        (roi_id_dict['subtext']).append(roi_id1)
        return roi_id_dict
    except Exception as exc:
        error_string = f"Exception received in get_roi_ids_dict: {exc}"
        logger.exception(error_string)
        raise Exception(error_string)


def get_action_dict(table_properties):
    """getting action dict for table"""
    try:
        action_dict = {'add': [], 'modify': [], 'delete': []}
        for data in table_properties:
            for key, value in data.items():
                if type(value) == dict:
                    action = value.get('qc_change_type')
                    if action == 'add':
                        pass
                    elif action == 'modify' or action == 'delete':
                        roi_id_dict = get_roi_ids_dict(value)
                        (action_dict[action]).append(
                            {'roi_id_dict': roi_id_dict, 'content': value.get('content')})

        return action_dict
    except Exception as exc:
        error_string = f"Exception received in get_action_dict for table: {exc}"
        logger.exception(error_string)
        raise Exception(error_string)


def process_table(data: dict):
    """processing table data"""
    try:
        table_properties = None
        if data.get('type') == 'table' and data.get('qc_change_type') != '' and type(data.get('content')) == dict:
            content = data.get('content')
            table_properties = content.get('TableProperties')
            if table_properties != '':
                table_properties = json.loads(table_properties)
        if table_properties is not None:
            action_dict = get_action_dict(table_properties)
            for key, val in action_dict.items():
                if key == 'add' and len(val) > 0:
                    pass
                if key == 'modify' and len(val) > 0:
                    db_update_table(val)
                if key == 'delete' and len(val) > 0:
                    db_delete_table(val)
    except Exception as exc:
        error_string = f"Exception received in processing table data: {exc}"
        logger.exception(error_string)
        raise Exception(error_string)
