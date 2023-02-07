from .model import *
import uuid
from .document import *
from .db_utils import *
import logging
from app.utilities.config import settings


logger = logging.getLogger(settings.LOGGER_NAME)

table_dict = TableType.table_dict

link_level_dict = Linklevel.link_level_dict


def get_roi_ids_dict(value):
    roi_id_dict = {'text' : [], 'table': [], 'subtext': []}
    datacell_roi_id = value['roi_id']['datacell_roi_id']
    roi_id = get_ids_from_parent_id(datacell_roi_id,'table')
    (roi_id_dict['table']).append(datacell_roi_id)
    (roi_id_dict['table']).append(roi_id)
    (roi_id_dict['text']).append(roi_id)
    roi_id1 = get_ids_from_parent_id(roi_id,'subtext')
    (roi_id_dict['subtext']).append(roi_id1)
    return roi_id_dict

def get_action_dict(table_properties):
    action_dict = {'modify': [], 'delete': [], 'add': []}
    for data in table_properties:
        for key, value in data.items():
            if type(value) == dict:
                action = value.get('qc_change_type')
                if action == 'add':
                    new_para_line_dict, new_childbox_line_dict = get_add_content_info(
                        data)
                    (action_dict[action]).append(
                            {data.get('type'): [new_para_line_dict, new_childbox_line_dict]})
                elif action == 'modify' or action == 'delete':
                    roi_id_dict = get_roi_ids_dict(value)
                    (action_dict[action]).append(
                            {'roi_id_dict': roi_id_dict, 'content': value.get('content')})

    return action_dict

def process(payload):
    table_properties = None
    for data in payload:
        if data.get('type') == 'table' and data.get('qc_change_type') != '' and type(data.get('content')) == dict:
            content = data.get('content')
            table_properties = content.get('TableProperties')
            if table_properties != '':
                table_properties = json.loads(table_properties)
    if table_properties is not None:
        action_dict = get_action_dict(table_properties)
        for key, val in action_dict.items():
            if key == 'modify' and len(val)>0:
                db_update_table(val)
            if key == 'delete' and len(val) > 0:
                db_delete_image(val)
            if key == 'add' and len(val) > 0:
                db_add_image(val)